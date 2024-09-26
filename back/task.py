"""自动化机器人"""

import time
import json
from typing import Dict

from bot import Bot
from module import Module


class Task:
    """自动化任务"""

    def __init__(self, task_name, task_data, plugins, path) -> None:
        self.bot = Bot()

        self._path = path
        self.name = task_name
        self.enable = False
        self.modules: Dict[str, Module] = {}
        modules = task_data["modules"] if "modules" in task_data else {}
        self._init_modules(plugins, modules)
        self.update_task(task_data)

    def _init_modules(self, plugins, modules_data):
        # 根据插件配置创建任务模块
        for code, plugin_data in plugins.items():
            self.modules[code] = Module(code, plugin_data, {}, self._path)

        # 根据任务配置填充模块数据
        for module_data in modules_data:
            module_name = module_data["name"]
            if module_name in self.modules:
                self.modules[module_name].update_module(module_data)

    def save(self):
        """保存任务信息到本地"""
        file_path = self._path["task"]
        with open(f"{file_path}/{self.name}.json", "w", encoding="utf-8") as fw:
            fw.write(json.dumps(self.get_task_data(), ensure_ascii=False, indent=4))

    def get_task_data(self):
        """获取任务信息"""
        module_data = []
        for _, module in self.modules.items():
            module_data.append(module.get_module_data())
        return {
            "name": self.name,
            "enable": self.enable,
            "bot": self.bot.get_bot_data(),
            "modules": module_data,
        }

    def update_task(self, task_data):
        """更新任务信息(启停/模块信息)"""
        if "enable" in task_data:
            self.enable = task_data["enable"]
        if "bot" in task_data:
            self.bot.set_bot_data(task_data["bot"])

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
        # 筛选启用且待触发的模块
        filtered_module = [
            m for m in self.modules.values() if m.enable and m.next < now
        ]
        # 根据优先级排序，优先执行级别高的任务
        sorted_module = sorted(filtered_module, key=lambda m: -m.priority)

        for module in sorted_module:

            try:
                next_cmd, cmd_type = module.get_next_cmd_and_cmd_type()
                resp = self.bot.execute(cmd_type, next_cmd)
                wait, log = module.run(resp, now)
                if wait != "":
                    if self.modules[wait].enable:
                        module.set_next_timestamp(self.modules[wait].next + 300)
                    else:
                        module.set_delay("5", "min")
                if log != "":
                    self.bot.log(self.name, log)
                self.save()
            except Exception as e:
                print(f"插件{module.name}运行出错 {type(e)}")
                raise e

            break  # 一次循环至多执行一个模块
        else:
            time.sleep(1)  # 没有可执行模块
