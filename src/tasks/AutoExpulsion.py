from qfluentwidgets import FluentIcon
import time
import random

from ok import Logger, TaskDisabledException
from src.tasks.DNAOneTimeTask import DNAOneTimeTask
from src.tasks.BaseCombatTask import BaseCombatTask
from src.tasks.CommissionsTask import CommissionsTask, Mission

logger = Logger.get_logger(__name__)


class AutoExpulsion(DNAOneTimeTask, CommissionsTask, BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = FluentIcon.FLAG
        self.name = "自动驱离"
        self.description = "全自动"
        self.group_name = "全自动"
        self.group_icon = FluentIcon.CAFE

        self.default_config.update({
            "随机游走": False,
            "刷几次": 999,
            "挂机模式": "开局重置角色位置",
            "开局向前走": 0.0
        })

        self.setup_commission_config()
        keys_to_remove = ["启用自动穿引共鸣"]
        for key in keys_to_remove:
            self.default_config.pop(key, None)

        self.config_description.update({
            "随机游走": "是否在任务中随机移动",
            "开局向前走": "开局向前走几秒"
        })
        self.config_type["挂机模式"] = {
            "type": "drop_down",
            "options": ["开局重置角色位置", "开局向前走"],
        }

        self.default_config.pop("启用自动穿引共鸣", None)
        self.action_timeout = 10

    def run(self):
        DNAOneTimeTask.run(self)
        self.move_mouse_to_safe_position()
        self.set_check_monthly_card()
        try:
            return self.do_run()
        except TaskDisabledException as e:
            pass
        except Exception as e:
            logger.error("AutoExpulsion error", e)
            raise

    def do_run(self):
        self.init_all()
        self.load_char()
        self.count = 0
        while True:
            if self.in_team():
                self.handle_in_mission()

            _status = self.handle_mission_interface(stop_func=self.stop_func)
            if _status == Mission.START:
                self.wait_until(self.in_team, time_out=30)
                self.sleep(2)
                self.init_all()
                self.handle_mission_start()
            elif _status == Mission.STOP:
                pass
            elif _status == Mission.CONTINUE:
                pass

            self.sleep(0.1)

    def init_all(self):
        self.init_for_next_round()
        self.current_round = -1

    def init_for_next_round(self):
        self.init_runtime_state()

    def init_runtime_state(self):
        self.runtime_state = {"start_time": 0, "skill_time": 0, "random_walk_time": 0}

    def handle_in_mission(self):
        if self.runtime_state["start_time"] == 0:
            self.move_on_begin()
            self.runtime_state["start_time"] = time.time()
            self.count += 1

        if time.time() - self.runtime_state["start_time"] >= self.config.get("超时时间", 120):
            logger.info("已经超时，重开任务...")
            self.give_up_mission()
            self.wait_until(lambda: not self.in_team(), time_out=30, settle_time=1)

        self.runtime_state["skill_time"] = self.use_skill(self.runtime_state["skill_time"])
        self.runtime_state["random_walk_time"] = self.random_walk(self.runtime_state["random_walk_time"])

    def handle_mission_start(self):
        if self.count >= self.config.get("刷几次", 999):
            self.sleep(1)
            self.open_in_mission_menu()
            self.log_info_notify("任务终止")
            self.soundBeep()
            return
        self.log_info("任务开始")
    
    def stop_func(self):
        pass

    def move_on_begin(self):
        if self.config.get("挂机模式") == "开局重置角色位置":
            # 复位方案
            self.reset_and_transport()
            # 防卡墙
            self.send_key("w", down_time=0.5)
        elif self.config.get("挂机模式") == "开局向前走":
            if (walk_sec := self.config.get("开局向前走", 0)) > 0:
                self.send_key("w", down_time=walk_sec)

    def random_walk(self, last_time):
        duration = 1
        interval = 3
        if self.config.get("随机游走", False):
            if time.time() - last_time >= interval:
                direction = random.choice(["w", "a", "s", "d"])
                self.send_key(direction, down_time=duration)
                return time.time()
        return last_time
