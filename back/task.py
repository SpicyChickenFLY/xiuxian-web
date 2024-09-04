"""自动化机器人"""

import time
import os
import json
import copy
from typing import Dict

from bot import Bot
from module import Module


# class OperateBot(threading.Thread):
class Task(Bot):
    """自动化任务"""

    def __init__(self, task_name, task_data) -> None:
        Bot.__init__(self)

        self.task_name = task_name
        self.enable = False
        self.modules: Dict[str, Module] = {}

        self.update_task(task_data)

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
        data_dir = "data/tasks"
        os.makedirs(f"{data_dir}", exist_ok=True)
        with open(f"{data_dir}/{self.task_name}.json", "w", encoding="utf-8") as fw:
            fw.write(json.dumps(data, ensure_ascii=False, indent=4))

    def update_task(self, task_data):
        self.enable = task_data["enable"] if "enable" in task_data else False
        self.modules: Dict[str, Module] = {}

        self._module_wait_map: Dict[str, str] = {}
        # 模块前置等待表，因为是串行化操作，并且是先检查后创建，应该不会死锁
        self._support_modules: Dict[str, Module] = {}
        try:
            with open("data/modules.json", "r", encoding="utf-8") as rf:
                self._support_modules = json.load(rf)
        except json.JSONDecodeError as e:
            print(f"解析模块配置文件data/modules.json失败 {e}")
        except Exception as e:
            print(f"加载模块配置文件data/modules.json失败 {type(e)} {e}")
        module_datas = task_data["modules"] if "modules" in task_data else {}
        for code, support_module in self._support_modules.items():
            module_data = module_datas[code] if code in module_datas else {}
            module_data["name"] = code
            self.modules[code] = Module(support_module, module_data)

        self.save()

    def get_bot_data(self):
        """可视化界面机器人配置返回"""
        bot_data = super()._get_bot_data()
        return bot_data

    def set_bot_data(self, bot_data):
        """可视化界面机器人配置设置"""
        super()._set_bot_data(bot_data)
        self.save()

    def get_module_list(self):
        """获取任务模块简要信息"""
        module_list = []
        for _, module in self.modules.items():
            module_list.append(module.get_module_base_detail())
        return module_list

    def toggle_enable(self, enable):
        self.enable = enable
        self.save()

    def run(self):
        """自动化任务运行一个时间片"""
        if not self.enable:
            return
        for module_code, module in self.modules.items():
            if not module.is_runnable():
                continue  # 不满足运行要求, 下一个

            module.record_prev()
            cmd_type = module.get_cmd_type()
            if cmd_type == "recv":
                module.run(self.receive(module.progress))
            elif cmd_type == "send":
                self.send(module.progress)
                module.run("")

            if module.wait != "":
                self._module_wait_map[module_code] = module.wait
            else:
                wait_map = copy.deepcopy(self._module_wait_map)
                for need, needed in wait_map.items():
                    if needed == module_code:
                        self.modules[need].wait = ""
                        self._module_wait_map.pop(need)

            if module.log != "":
                self.log(self.task_name, module.log)
                module.log = ""

            self.save()
            return  # 一次循环至多执行一个模块
        time.sleep(1)  # 没有可执行模块
