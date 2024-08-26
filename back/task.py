"""自动化机器人"""

import time

from utils import Bot

from bu_chang import BuChang
from dan_yao import DanYao
from fang_shi import FangShi
from ling_tian import LingTian
from mi_jing import MiJing
from qian_dao import QianDao
from shuang_xiu import ShuangXiu
from xiu_lian import XiuLian
from xuan_shang_ling import XuanShangLing
from zong_meng_ren_wu import ZongMenRenWu


# class OperateBot(threading.Thread):
class Task(Bot):
    """自动化任务"""

    def __init__(self, name, profile) -> None:
        bot_config = profile["bot"] if "bot" in profile else {}
        Bot.__init__(self, name, bot_config)

        self._module_wait_map = {}
        self._code_module_map = {
            "灵田": LingTian,
            "补偿": BuChang,
            "签到": QianDao,
            "宗门丹药": DanYao,
            "双修": ShuangXiu,
            "宗门任务": ZongMenRenWu,
            "悬赏令": XuanShangLing,
            "秘境": MiJing,
            "修炼": XiuLian,
            "坊市": FangShi,
        }
        self.modules = {}
        module_profile = profile["module"] if "module_config" in profile else {}
        for code, module in self._code_module_map.items():
            module_config = module_profile[code] if code in module_profile else {}
            self.modules[code] = module(module_config)

    def save(self):
        """保存类成员参数"""
        # return {
        #     "config": self.config,
        #     "next": self.next,
        #     "progress": self.progress,
        # }

    def get_brief(self):
        """获取任务模块简要信息"""
        module_map = {}
        for code, module in self.modules.items():
            module_map[code] = module.enable
        return module_map

    def run(self):
        """自动化任务运行一个时间片"""
        now = time.time()
        for module_code, module in self.modules.items():
            if module.enable and module.wait == "" and now > module.next:
                resp = self.receive(module.get_cmd())
                module.run(resp)
                if module.wait != "":
                    self._module_wait_map[module_code] = module.wait
                else:
                    for need, needed in self._module_wait_map.items():
                        if needed == module_code:
                            self.modules[need].wait = ""
                            self._module_wait_map.pop(need)
                if module.log != "":
                    self.log(module.log)
                    module.log = ""
                return
        # 没有可执行模块
        time.sleep(1)
