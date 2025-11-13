from qfluentwidgets import FluentIcon
import time
import re
import cv2
from concurrent.futures import ThreadPoolExecutor

from ok import Logger, TaskDisabledException
from src.tasks.CommissionsTask import CommissionsTask, QuickMoveTask, Mission, _default_movement
from src.tasks.BaseCombatTask import BaseCombatTask
from src.tasks.DNAOneTimeTask import DNAOneTimeTask

logger = Logger.get_logger(__name__)


class AutoHedge(DNAOneTimeTask, CommissionsTask, BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = FluentIcon.FLAG
        self.name = "自动避险"
        self.description = "半自动"
        self.group_name = "半自动"
        self.group_icon = FluentIcon.VIEW

        # self.default_config.update({
        #     '轮次': 3,
        # })

        self.setup_commission_config()

        self.config_description.update({
            # '轮次': '打几个轮次',
            '超时时间': '超时后将发出提示',
        })

        self.action_timeout = 10
        self.quick_move_task = QuickMoveTask(self)
        self.external_movement = _default_movement
        self.skill_time = 0
        self.progressing = False
        self.track_point_pos = 0
        self.mission_complete = False
        self.ocr_executor = None
        self.ocr_future = None
        self.last_ocr_result = -1

    # def config_external_movement(self, func: callable, config: dict):
    #     if callable(func):
    #         self.external_movement = func
    #     else:
    #         self.external_movement = _default_movement
    #     self.config.update(config)

    def run(self):
        DNAOneTimeTask.run(self)
        self.move_mouse_to_safe_position()
        self.set_check_monthly_card()
        try:
            return self.do_run()
        except TaskDisabledException:
            pass
        except Exception as e:
            logger.error("AutoExploration error", e)
            raise

    def do_run(self):
        self.init_param()
        self.load_char()
        _wait_next_round = False
        _start_time = 0
        if self.external_movement is not _default_movement and self.in_team():
            self.open_in_mission_menu()
        while True:
            if self.in_team():
                self.update_mission_status()
                if self.progressing:
                    if _start_time == 0:
                        _start_time = time.time()
                        _wait_next_round = False
                        self.quick_move_task.reset()
                    self.skill_time = self.use_skill(self.skill_time)
                    if not _wait_next_round and time.time() - _start_time >= self.config.get("超时时间", 120):
                        if self.external_movement is not _default_movement:
                            self.log_info("任务超时")
                            self.open_in_mission_menu()
                        else:
                            self.log_info_notify("任务超时")
                            self.soundBeep()
                            _wait_next_round = True
                else:
                    if self.mission_complete and self.skill_time > 0:
                        self.skill_time = 0
                        self.log_info_notify("任务结束")
                        self.soundBeep()
                    self.quick_move_task.run()

            _status = self.handle_mission_interface()
            if _status == Mission.START:
                self.wait_until(self.in_team, time_out=30)
                self.sleep(2)
                self.init_param()
                if self.external_movement is not _default_movement:
                    self.update_mission_status()
                    self.log_info("任务开始")
                    self.external_movement()
                    time_out = 10
                    self.log_info(f"外部移动执行完毕，等待战斗开始，{time_out}秒后超时")
                    if not self.wait_until(self.progressing, post_action=self.update_mission_status, time_out=time_out):
                        self.log_info("超时重开")
                        self.open_in_mission_menu()
                    else:
                        self.log_info("战斗开始")
                else:
                    self.log_info_notify("任务开始")
                    self.soundBeep()
                _start_time = 0
            # elif _status == Mission.STOP:
            #     self.quit_mission()
            #     self.log_info("任务中止")
            # elif _status == Mission.CONTINUE:
            #     self.wait_until(self.in_team, time_out=30)
            #     self.log_info("任务继续")
            #     _start_time = 0

            self.next_frame()

    def init_param(self):
        self.skill_time = 0
        self.track_point_pos = 0
        self.progressing = False
        self.mission_complete = False
        if self.ocr_executor is not None:
            self.ocr_executor.shutdown(wait=False, cancel_futures=True)
        self.ocr_executor = ThreadPoolExecutor(max_workers=2)
        self.ocr_future = None
        self.last_ocr_result = -1

    # def stop_func(self):
    #     self.get_round_info()
    #     if self.current_round >= self.config.get("轮次", 3):
    #         return True

    # def find_serum(self):
    #     return bool(self.find_one("serum_icon"))

    def update_mission_status(self):
        if self.mission_complete:
            return
        percentage = self.get_serum_process_info()
        if percentage == 100:
            self.progressing = False
            self.mission_complete = True
        elif percentage > 0:
            self.progressing = True
        if not self.progressing and not self.mission_complete:
            _track_point = self.find_top_right_track_pos()
            if _track_point < 0:
                return
            if self.track_point_pos == 0:
                self.track_point_pos = _track_point
            elif (rpd := abs(_track_point - self.track_point_pos) / self.track_point_pos) > 0.02:
                self.log_debug(f"track point diff pct {rpd}")
                self.progressing = True

    def get_serum_process_info(self):
        if self.ocr_future and self.ocr_future.done():
            try:
                texts = self.ocr_future.result()
                if texts and "%" in texts[0].name:
                    name = texts[0].name.replace("%", "")
                    if name.isdigit():
                        pct = int(name)
                        if pct > self.last_ocr_result and pct <= 100:
                            self.last_ocr_result = pct
                            self.info_set("进度", f"{pct}%")
            except Exception as e:
                logger.error(f"OCR任务出错: {e}")
            finally:
                self.ocr_future = None
        if self.ocr_future is None:
            box = self.box_of_screen_scaled(2560, 1440, 115, 399, 217, 461, name="process_info", hcenter=True)
            self.ocr_future = self.ocr_executor.submit(self.ocr, box=box, match=re.compile(r"\d+%"))
        return self.last_ocr_result

    def find_top_right_track_pos(self):
        box = self.box_of_screen_scaled(2560, 1440, 2183, 82, 2414, 140, name="track_point", hcenter=True)
        template = cv2.resize(self.get_feature_by_name("track_point").mat, None, fx=0.79, fy=0.79,
                              interpolation=cv2.INTER_LINEAR)
        ret = -1
        box = self.find_track_point(box=box, template=template, filter_track_color=True)
        if box is not None:
            ret = box.x
        return ret
