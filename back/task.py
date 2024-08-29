"""自动化机器人"""

import time
import json

from utils import Bot
from module import Module
from typing import Dict

from fang_shi import FangShi
from xuan_shang_ling import XuanShangLing


# class OperateBot(threading.Thread):
class Task(Bot):
    """自动化任务"""

    def __init__(self, name, task_profile) -> None:
        bot_profile = task_profile["bot"] if "bot" in task_profile else {}
        Bot.__init__(self, bot_profile)

        self.task_name = name
        self.enable = False
        self._module_wait_map = {}
        self._support_modules: Dict[str, Module] = {}
        try:
            with open("data/modules.json", "r", encoding="utf-8") as rf:
                self._support_modules = json.load(rf)
        except Exception as e:
            print(f"加载模块配置文件data/modules.json失败 {type(e)} {e}")
        self.modules = {}
        module_profiles = task_profile["modules"] if "modules" in task_profile else {}
        for code, support_module in self._support_modules.items():
            module_profile = module_profile[code] if code in module_profiles else {}
            module_profile['name'] = code
            self.modules[code] = Module(support_module, module_profile)

    def save(self):
        """保存类成员参数"""
        module_profile = {}
        for code, module in self.modules.items():
            module_profile[code] = module.get_module_base_detail()
        profile = {
            "task_name": self.task_name,
            "enable": self.enable,
            "bot": self.get_bot_profile(),
            "modules": module_profile
        }
        with open(f"profiles/{self.task_name}.json", "w", encoding="utf-8") as fw:
            fw.write(json.dumps(profile, ensure_ascii=False, indent=4))

    def get_brief(self):
        """获取任务模块简要信息"""
        module_list = []
        for _, module in self.modules.items():
            module_list.append(module.get_module_base_detail())
        return module_list

    def run(self):
        """自动化任务运行一个时间片"""
        now = time.time()
        for module_code, module in self.modules.items():
            if module.enable and module.wait == "" and now > module.next:
                module.record_prev()
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
                    self.log(self.task_name, module.log)
                    module.log = ""
                return
        # 没有可执行模块
        time.sleep(1)
