"""自动化机器人"""

import time
import json
from typing import Dict

from bot import Bot
from module import Module


# class OperateBot(threading.Thread):
class Task(Bot):
    """自动化任务"""

    def __init__(self, name, task_data) -> None:
        bot_data = task_data["bot"] if "bot" in task_data else {}
        Bot.__init__(self, bot_data)

        self.task_name = name
        self.enable = False
        self._module_wait_map: Dict[str, str] = {}
        self._support_modules: Dict[str, Module] = {}
        try:
            with open("data/modules.json", "r", encoding="utf-8") as rf:
                self._support_modules = json.load(rf)
        except Exception as e:
            print(f"加载模块配置文件data/modules.json失败 {type(e)} {e}")
        self.modules: Dict[str, Module] = {}
        module_datas = task_data["modules"] if "modules" in task_data else {}
        for code, support_module in self._support_modules.items():
            module_data = module_datas[code] if code in module_datas else {}
            module_data["name"] = code
            self.modules[code] = Module(support_module, module_data)

    def save(self):
        """保存类成员参数"""
        module_data = {}
        for code, module in self.modules.items():
            module_data[code] = module.get_module_base_detail()
        data = {
            "task_name": self.task_name,
            "enable": self.enable,
            "bot": self.get_bot_data(),
            "modules": module_data,
        }
        with open(f"profiles/{self.task_name}.json", "w", encoding="utf-8") as fw:
            fw.write(json.dumps(data, ensure_ascii=False, indent=4))

    def get_brief(self):
        """获取任务模块简要信息"""
        module_list = []
        for _, module in self.modules.items():
            module_list.append(module.get_module_base_detail())
        return module_list

    def run(self):
        """自动化任务运行一个时间片"""
        for module_code, module in self.modules.items():
            if not module.is_runnable():
                continue  # 不满足运行要求, 下一个

            module.record_prev()
            cmd, cmd_type = module.get_cmd_and_type()
            if cmd_type() == "recv":
                module.run(self.receive(cmd))
            elif cmd_type() == "send":
                self.send(module.progress)
                module.run("")

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

            return  # 一次循环至多执行一个模块
        time.sleep(1)  # 没有可执行模块
