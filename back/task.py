"""自动化机器人"""

import re
import time
import threading

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
        bot_config = profile['bot'] if 'bot' in profile else {}
        Bot.__init__(self, name, bot_config)

        self._running = False
        self._thread = None
        self._module_wait_map = {}
        self._code_module_map = {
            "lt": LingTian,
            "bc": BuChang,
            "qd": QianDao,
            "dy": DanYao,
            "sx": ShuangXiu,
            "zm": ZongMenRenWu,
            "xsl": XuanShangLing,
            "mj": MiJing,
            "xl": XiuLian,
            "fs": FangShi,
        }
        self.modules = {}
        module_profile = profile['module'] if 'module_config' in profile else {}
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

    def module_list(self):
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

class TaskMgr():
    """修仙机器人任务管理器"""

    def __init__(self) -> None:
        self._running = False
        self._thread = None
        self._task_map = {}

        # 浏览本地profile

    def _run(self):
        """自动化程序启动"""
        while True:
            for task in self._task_map:
                if not self._running:
                    return
                task.run()

    def is_running(self):
        """获取机器人启停状态"""
        return self._running

    def start(self):
        """启动自动化任务"""
        self._running = True
        self._thread = threading.Thread(target=self._run)

    def stop(self):
        """停止自动化任务"""
        self._running = False
        if self._thread:
            self._thread.join()

    def list_tasks(self):
        """返回自动化任务列表"""
        task_list = []
        for name, task in self._task_map.items():
            task_list.append({ "name": name, "modules": task.module_list() })
        return task_list

    def get_task(self, task_id):
        """返回自动化任务详情"""
        self._task_map[task_id].export()

    def create_task(self, task_profile):
        """创建新的自动化任务"""
        self.stop()
        self._task_map[""] = Task("", task_profile)
        self.start()
        return ""

    def update_task(self, task_id, task_profile):
        """创建新的自动化任务"""
        self.stop()
        self._task_map[task_id].update(task_profile)
        self.start()
        return ""

    def delete_task(self, task_id):
        """创建新的自动化任务"""
        self.stop()
        self._task_map.pop(task_id)
        self.start()
        return ""
