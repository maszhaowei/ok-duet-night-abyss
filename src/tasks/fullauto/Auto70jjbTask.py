from qfluentwidgets import FluentIcon
import re
import time
import win32con
import win32gui
import cv2

from ok import Logger, TaskDisabledException, Box
from ok import find_boxes_by_name
from src.tasks.DNAOneTimeTask import DNAOneTimeTask
from src.tasks.CommissionsTask import CommissionsTask, Mission, QuickMoveTask
from src.tasks.BaseCombatTask import BaseCombatTask

logger = Logger.get_logger(__name__)


class Auto70jjbTask(DNAOneTimeTask, CommissionsTask, BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = FluentIcon.FLAG
        self.name = "自动70级皎皎币本"
        self.description = "全自动"
        self.group_name = "全自动"
        self.group_icon = FluentIcon.CAFE

        self.default_config.update({
            '轮次': 1,
        })

        self.setup_commission_config()
        keys_to_remove = ["启用自动穿引共鸣", "自动选择首个密函和密函奖励"]
        for key in keys_to_remove:
            self.default_config.pop(key, None)

        self.config_description.update({
            '轮次': '打几个轮次',
        })

        self.action_timeout = 10
        self.quick_move_task = QuickMoveTask(self)

    def run(self):
        DNAOneTimeTask.run(self)
        self.move_mouse_to_safe_position(save_current_pos=False)
        self.set_check_monthly_card()
        try:
            return self.do_run()
        except TaskDisabledException as e:
            pass
        except Exception as e:
            logger.error('AutoDefence error', e)
            raise

    def do_run(self):
        self.init_param()
        self.load_char()
        _wave = -1
        _wait_next_wave = False
        _wave_start = 0
        if self.in_team():
            self.open_in_mission_menu()
            self.sleep(0.5)
        while True:
            if self.in_team():
                self.get_wave_info()
                if self.current_wave != -1:
                    if self.current_wave != _wave:
                        _wave = self.current_wave
                        _wave_start = time.time()
                        _wait_next_wave = False
                    self.skill_time = self.use_skill(self.skill_time)
                    if not _wait_next_wave and time.time() - _wave_start >= self.config.get('超时时间', 120):
                        self.log_info('任务超时')
                        self.open_in_mission_menu()
                        self.sleep(0.5)
                        _wait_next_wave = True

            _status = self.handle_mission_interface(stop_func=self.stop_func)
            if _status == Mission.START or _status == Mission.STOP:
                if _status == Mission.STOP:
                    self.quit_mission()
                    self.log_info('任务中止')
                    self.init_param()
                    continue
                else:
                    self.log_info('任务完成')
                self.wait_until(self.in_team, time_out=30)
                self.init_param()
                self.send_key_down("lalt")
                self.sleep(2)
                self.walk_to_aim()
                self.send_key_up("lalt")
                _wave_start = time.time()

                self.current_wave = -1
                while self.current_wave == -1 and time.time() - _wave_start < 2:
                    self.get_wave_info()
                    self.sleep(0.2)
                if self.current_wave == -1:
                    self.log_info('未正确到达任务地点')
                    self.open_in_mission_menu()
                    self.sleep(0.5)
            elif _status == Mission.CONTINUE:
                self.log_info('任务继续')
                self.wait_until(self.in_team, time_out=30)
                self.current_wave = -1
            self.sleep(0.2)

    def init_param(self):
        self.stop_mission = False
        self.current_round = -1
        self.current_wave = -1
        self.skill_time = 0

    def stop_func(self):
        self.get_round_info()
        n = self.config.get('轮次', 3)
        if n == 1 or self.current_round >= n:
            return True
        
    def find_track_point(self, x1, y1, x2, y2) -> bool:
        box = self.box_of_screen_scaled(2560, 1440, 2560*x1, 1440*y1, 2560*x2, 1440*y2, name="find_track_point", hcenter=True)
        return super().find_track_point(threshold=0.7, box=box)
        
    def walk_to_aim(self):
        found_target = False
        if self.find_track_point(0.20,0.54,0.22,0.59):
            #70皎皎币-无电梯
            found_target = True
            self.send_key_down("lalt")
            self.sleep(0.05)
            self.send_key_down("w")
            self.sleep(0.1)
            self.send_key_down("a")
            self.sleep(0.1)
            self.send_key_down("lshift")
            self.sleep(2.2)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key_down("lshift")
            self.sleep(2.2)
            self.send_key_up("w")
            self.sleep(1)
            self.send_key("space", down_time=0.1)
            self.sleep(1)
            self.send_key_up("lshift")
            self.sleep(0.1)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key_down("lshift")
            self.sleep(1.8)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key_down("lshift")
            self.sleep(2.2)
            self.send_key_up("lshift")
            self.sleep(0.1)
            self.send_key_up("a")
            #分支1直接到达，未到达则进入分支2继续往前走
            start = time.time()
            self.current_wave = -1
            while self.current_wave == -1 and time.time() - start < 2:
                self.get_wave_info()
                self.sleep(0.2) 
            if self.current_wave == -1:
                self.send_key_down('a')
                self.sleep(0.2)
                self.send_key_down("lshift")
                self.sleep(1)
                self.send_key('space', down_time=0.2, after_sleep=1.8)
                self.send_key_up("lshift")
                self.sleep(0.1)
                self.send_key_up('a')
            self.send_key_up("lalt")
            return             

        if self.find_track_point(0.66,0.67,0.69,0.72):
            #70皎皎币-电梯右
            found_target = True
            self.reset_and_transport()
            self.send_key('s', down_time=0.2,after_sleep=0.2)
            self.middle_click(after_sleep=0.2)
            self.send_key_down("lalt")
            self.sleep(0.05)
            self.send_key_down('a')
            self.sleep(0.2)
            self.send_key_down("lshift")
            self.sleep(0.4)
            self.send_key_down('w')
            self.sleep(0.7)
            self.send_key_up('lshift')
            self.sleep(0.1)
            self.send_key_up("a")
            self.sleep(0.1)
            self.send_key('space',down_time=0.3,after_sleep=0.2)
            self.send_key('space',down_time=0.3,after_sleep=0.4)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key_down("lshift")
            self.sleep(2.2)
            self.send_key_down('d')
            self.sleep(0.1)
            self.send_key_up("lshift")
            self.sleep(0.2)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.1)
            self.send_key_up("w")
            self.sleep(0.7)
            self.send_key_down("lshift")
            self.sleep(0.5)
            self.send_key_down('w')
            self.sleep(1)
            self.send_key_up('d')
            self.sleep(0.7)
            self.send_key_up("lshift")
            self.sleep(0.1)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key_down("lshift")
            self.sleep(2.5)
            self.send_key_up("lshift")
            self.sleep(0.2)
            self.send_key_up('w')
            self.send_key_up("lalt")
            self.reset_and_transport()
            return            

        if self.find_track_point(0.32,0.67,0.35,0.73):
            #70皎皎币-电梯左
            found_target = True
            self.reset_and_transport()
            self.send_key_down("lalt")
            self.sleep(0.05)
            self.send_key_down('w')
            self.sleep(0.2)
            self.send_key_down("lshift")
            self.sleep(0.6)
            self.send_key_down("a")
            self.sleep(0.6)
            self.send_key_up('a')
            self.sleep(0.8)
            self.send_key_up("lshift")
            self.sleep(0.1)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key_down("lshift")
            self.sleep(2)
            self.send_key_down("d")
            self.sleep(1)
            self.send_key_up('d')
            self.sleep(0.8)
            self.send_key_up("lshift")
            self.sleep(0.1)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.8)
            self.send_key_down("lshift")
            self.sleep(1)
            self.send_key_down("d")
            self.sleep(0.5)
            self.send_key_up('d')
            self.sleep(3.6)
            self.send_key_up("lshift")
            self.sleep(0.2)
            self.send_key_up('w')
            self.send_key_up("lalt")
            self.reset_and_transport()
            return            

        if self.find_track_point(0.50,0.71,0.53,0.76):
            #70皎皎币-电梯中
            found_target = True
            self.reset_and_transport()
            self.send_key_down("lalt")
            self.sleep(0.05)
            self.send_key_down('w')
            self.sleep(0.2)
            self.send_key_down('d')
            self.sleep(0.2)
            self.send_key_down("lshift")
            self.sleep(0.7)
            self.send_key_up('w')
            self.sleep(1.2)
            self.send_key_up("lshift")
            self.sleep(0.2)
            self.send_key("lshift", down_time=0.2)
            self.sleep(0.4)
            self.send_key_down('s')
            self.sleep(0.3)
            self.send_key_down("lshift")
            self.sleep(0.4)
            self.send_key_up('s')
            self.sleep(1)
            self.send_key("lshift", down_time=0.2)
            self.sleep(2)
            self.send_key_up("lshift")
            self.sleep(0.1)
            self.send_key_up('d')
            self.send_key_up("lalt")
            self.reset_and_transport()
            return     