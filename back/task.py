"""自动化机器人"""

import time
import os
import json
from typing import Dict

from bot import Bot
from module import Module

class Task():
    """自动化任务"""

    def __init__(self, task_name, task_data) -> None:
        self.bot = Bot()

        self.task_name = task_name
        self.enable =  False
        self.modules: Dict[str, Module] = {}
        self._init_modules(task_data["modules"] if "modules" in task_data else {})
        self.update_task(task_data)

    def _init_modules(self, modules_data):
        # 模块前置等待表，因为是串行化操作，并且是先检查后创建，应该不会死锁
        self._support_modules: Dict[str, Module] = {}
        try:
            with open("data/modules.json", "r", encoding="utf-8") as rf:
                self._support_modules = json.load(rf)
        except json.JSONDecodeError as e:
            print(f"解析模块配置文件data/modules.json失败 {e}")
        except Exception as e:
            print(f"加载模块配置文件data/modules.json失败 {type(e)} {e}")
        for code, support_module in self._support_modules.items():
            module_data = modules_data[code] if code in modules_data else {}
            module_data["name"] = code
            self.modules[code] = Module(support_module, module_data)


    def save(self):
        """保存任务信息到本地"""
        data_dir = "data/tasks"
        os.makedirs(f"{data_dir}", exist_ok=True)
        with open(f"{data_dir}/{self.task_name}.json", "w", encoding="utf-8") as fw:
            fw.write(json.dumps(self.get_task_data(), ensure_ascii=False, indent=4))

    def get_task_data(self):
        """获取任务信息"""
        module_data = {}
        for code, module in self.modules.items():
            module_data[code] = module.get_module_data()
        return {
            "name": self.task_name,
            "enable": self.enable,
            "bot": self.bot.get_bot_data(),
            "modules": module_data,
        }

    def update_task(self, task_data):
        """更新任务信息(启停/模块信息)"""
        if "enable" in task_data:
            self.enable = task_data["enable"]
        if "bot" in task_data:
            self.bot.set_bot_data(task_data['bot'])

        self.save()

    def get_module_list(self):
        """获取任务模块简要信息"""
        module_list = []
        for _, module in self.modules.items():
            module_list.append(module.get_module_data())
        return module_list

    def run(self):
        """自动化任务运行一个时间片"""
        if not self.enable:
            return

        now = time.time()
        for _, module in self.modules.items():
            if not module.enable or now <= module.next:
                continue  # 不满足运行要求, 下一个

            next_cmd, cmd_type = module.get_next_cmd_and_cmd_type()
            resp = self.bot.receive(next_cmd) if cmd_type == 'recv' else ""
            if cmd_type == "send":
                self.bot.send(next_cmd)
            wait, log = module.run(resp, now)
            if wait != "":
                module.set_next_timestamp(self.modules[wait].next - 5)
            if log != "":
                self.bot.log(self.task_name, log)

            self.save()
            break  # 一次循环至多执行一个模块
        else:
            time.sleep(1)  # 没有可执行模块
