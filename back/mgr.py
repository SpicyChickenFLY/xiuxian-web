"""自动化任务管理器"""

import threading
import os
import json
from typing import Dict

from task import Task


class TaskMgr:
    """自动化任务管理器"""

    def __init__(self) -> None:
        self.is_running = False
        self._thread = None
        # 路径需要是相对路径
        self.path = {
            'task': 'task',
            'plugin': 'plugin',
            'func': 'func',
            'misc': 'misc',
            'cmd': 'data'
        }

        # 把所有路径都创建好
        for _, path in self.path.items():
            os.makedirs(path, exist_ok=True)

        self.tasks: Dict[str, Task] = {}
        # 读取本地任务信息
        tasks_data = []
        for root, _, files in os.walk(self.path['task']):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        task_data = json.load(rf)
                        tasks_data.append(task_data)
                except json.JSONDecodeError as e:
                    print(f"解析任务配置文件{file_path}失败 {e}")
                except Exception as e:
                    print(f"加载任务配置文件{file_path}失败 {type(e)} {e}")
        for task_data in tasks_data:
            self.create_task(task_data["name"], task_data)

    def _run(self):
        """自动化程序启动"""
        while True:
            for _, task in self.tasks.items():
                if not self.is_running:
                    return
                try:
                    task.run()
                except Exception as e:
                    print(f"任务[{task.name}]执行失败 {type(e)}")
                    print(e)
            if not self.is_running:
                return

    def _start(self):
        """启动自动化任务"""
        if self.is_running:
            return
        self.is_running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()
        print("started")

    def _stop(self):
        """停止自动化任务"""
        if not self.is_running:
            return
        self.is_running = False
        if self._thread:
            self._thread.join()
        print("stopped")

    def get_mgr_info(self):
        """获取管理器信息"""
        task_list = []
        for _, task in self.tasks.items():
            task_list.append(task.get_task_data())
        return {"is_running": self.is_running, "tasks": task_list}

    def update_mgr(self, mgr_data):
        """更新管理器信息"""
        if "is_running" in mgr_data:
            if mgr_data["is_running"]:
                self._start()
            else:
                self._stop()

    def create_task(self, task_name, task_data):
        """创建新的自动化任务"""
        was_run = self.is_running
        self._stop()
        # 每次创建任务前需要重新加载最新的插件配置
        plugins = self.get_plugin_list()
        self.tasks[task_name] = Task(task_name, task_data, plugins, self.path)
        if was_run:
            self._start()
        return ""

    def update_task(self, task_name, task_data):
        """更新自动化任务信息"""
        was_run = self.is_running
        self._stop()
        self.tasks[task_name].update_task(task_data)
        if was_run:
            self._start()

    def delete_task(self, task_name):
        """创建新的自动化任务"""
        was_run = self.is_running
        self._stop()
        self.tasks.pop(task_name)
        os.remove(f"task/{task_name}.json")
        if was_run:
            self._start()
        return task_name

    def update_module(self, task_name, module_name, module_data):
        """启用自动化任务"""
        was_run = self.is_running
        self._stop()
        self.tasks[task_name].modules[module_name].update_module(module_data)
        if was_run:
            self._start()
        return module_name

    def get_plugin_list(self):
        """获取模块配置文件"""
        plugins_data = {}
        for root, _, files in os.walk(self.path['plugin']):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        plugin_name = os.path.splitext(file)[0]
                        plugin_data = json.load(rf)
                        plugins_data[plugin_name] = plugin_data
                except json.JSONDecodeError as e:
                    print(f"解析插件配置文件{file_path}JSON数据失败 {e}")
                except Exception as e:
                    print(f"加载插件配置文件{file_path}失败 {type(e)} {e}")
        return plugins_data

    def update_plugin(self, plugin_name, plugin_data):
        """更新模块配置文件"""
        file_path = f"{self.path['plugin']}/{plugin_name}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as fw:
                fw.write(json.dumps(plugin_data, ensure_ascii=False, indent=4))
        except Exception as e:
            print(f"写入插件配置文件{file_path}失败 {type(e)} {e}")
        # NOTE: 更新插件配置需要重启自动化任务

    def get_func_list(self):
        """获取自定义方法列表"""
        funcs = {}
        for root, _, files in os.walk(self.path['func']):
            if root == "func/__pycache__":
                continue
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        funcs[file] = rf.read()
                except Exception as e:
                    print(f"加载自定义方法文件{file_path}失败 {type(e)} {e}")
        return funcs

    def update_func(self, func_name, func_data):
        """更新自定义方法列表"""
        file_path = f"{self.path['func']}/{func_name}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as fw:
                fw.write(func_data)
        except Exception as e:
            print(f"写入模块配置文件{file_path}失败 {type(e)} {e}")
        # NOTE: 模块加载自定义方法通过导入的方式,不需要重新加载自动化任务

    def get_misc_list(self):
        """获取自定义数据列表"""
        funcs = {}
        for root, _, files in os.walk(self.path['misc']):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        funcs[file] = json.load(rf)
                except Exception as e:
                    print(f"加载自定义数据文件{file_path}失败 {type(e)} {e}")
        return funcs

    def update_misc(self, misc_name, misc_data):
        """更新自定义数据列表"""
        file_path = f"{self.path['misc']}/{misc_name}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as fw:
                fw.write(misc_data)
        except Exception as e:
            print(f"写入模块配置文件{file_path}失败 {type(e)} {e}")
        # NOTE: 模块加载自定义数据通过导入的方式,不需要重新加载自动化任务

    def exec_cmd(self, cmd_data):
        was_run = self.is_running
        self._stop()
        task_name = cmd_data['task']
        result = self.tasks[task_name].exec_cmd(cmd_data)
        self.update_cmd(cmd_data)
        if was_run:
            self._start()
        return result

    def get_cmd_list(self):
        """获取自定义数据列表"""
        cmd_map = {}
        file_path = f"{self.path['cmd']}/cmd.json"
        try:
            with open(file_path, "r", encoding="utf-8") as rf:
                cmd_map = json.load(rf)
        except Exception as e:
            print(f"加载命令历史文件{file_path}失败 {type(e)} {e}")
        return cmd_map

    def update_cmd(self, cmd_data):
        """更新自定义数据列表"""
        file_path = f"{self.path['cmd']}/cmd.json"
        try:
            cmd_map = {}
            with open(file_path, "r", encoding="utf-8") as rf:
                cmd_map = json.load(rf)
            cmd_map[cmd_data['cmd']] = cmd_data['type']
            with open(file_path, "w+", encoding="utf-8") as fw:
                fw.write(json.dumps(cmd_map, ensure_ascii=False, indent=4))
        except Exception as e:
            print(f"写入历史命令文件{file_path}失败 {type(e)} {e}")

    def delete_cmd(self, cmd_name):
        """更新自定义数据列表"""
        file_path = f"{self.path['cmd']}/cmd.json"
        try:
            cmd_map = {}
            with open(file_path, "r", encoding="utf-8") as rf:
                cmd_map = json.load(rf)
                if cmd_name in cmd_map:
                    cmd_map.pop(cmd_name)
            with open(file_path, "w+", encoding="utf-8") as fw:
                fw.write(json.dumps(cmd_map, ensure_ascii=False, indent=4))
        except Exception as e:
            print(f"写入历史命令文件{file_path}失败 {type(e)} {e}")
