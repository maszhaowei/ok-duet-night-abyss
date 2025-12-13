from qfluentwidgets import FluentIcon

from ok import Logger
from src.tasks.BaseDNATask import BaseDNATask

logger = Logger.get_logger(__name__)

default_config = {
    "委托手册": "不使用",
    "委托手册指定轮次": "",
    "自动处理密函": True,
    "密函奖励偏好": "不使用",
    "自动穿引共鸣": True,
    "自动花弓": True,
}

config_description = {
    "委托手册指定轮次": "范例: 3,5,8",
    "自动处理密函": "自动完成密函的对话交互与默认奖励领取",
    "密函奖励偏好": "指定优先选择的奖励类型，需开启「自动处理密函」",
    "自动穿引共鸣": "在需要时启用触发任务的自动穿引共鸣",
    "自动花弓": "在需要时启用触发任务的自动花弓",
}

config_type = {
    "委托手册": {
        "type": "drop_down",
        "options": ["不使用", "100%", "200%", "800%", "2000%"],
    },
    "密函奖励偏好": {
        "type": "drop_down",
        "options": ["不使用", "持有数为0", "持有数最少", "持有数最多"],
    }
}

class CommissionConfig(BaseDNATask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = FluentIcon.SETTING
        self.name = "全局任务设定"
        self.description = "不需要按开始"
        self.default_config.update(default_config)
        self.config_description.update(config_description)
        self.config_type.update(config_type)
