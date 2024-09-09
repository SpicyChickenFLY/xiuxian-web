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
        self.tasks: Dict[str, Task] = {}

        # 读取本地任务信息
        for root, _, files in os.walk("data/tasks"):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        task_data = json.load(rf)
                        self.create_task(task_data["name"], task_data)
                except json.JSONDecodeError as e:
                    print(f"解析任务配置文件{file_path}失败 {e}")
                except Exception as e:
                    print(f"加载任务配置文件{file_path}失败 {type(e)} {e}")

    def _run(self):
        """自动化程序启动"""
        while True:
            for _, task in self.tasks.items():
                if not self.is_running:
                    return
                try:
                    task.run()
                except Exception as e:
                    print(f"任务运行出错 {type(e)} {e}")
            if not self.is_running:
                return

    def _start(self):
        """启动自动化任务"""
        if self.is_running:
            print("already started")
            return
        self.is_running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()
        print("started")

    def _stop(self):
        """停止自动化任务"""
        if not self.is_running:
            print("already stopped")
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

    def create_task(self, task_name, task_profile):
        """创建新的自动化任务"""
        was_run = self.is_running
        self._stop()
        self.tasks[task_name] = Task(task_name, task_profile)
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
        os.remove(f"data/tasks/{task_name}.json")
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

    def get_config(self):
        """获取模块配置文件"""
        _support_modules = {}
        try:
            with open("data/modules.json", "r", encoding="utf-8") as rf:
                _support_modules = json.load(rf)
        except json.JSONDecodeError as e:
            print(f"解析模块配置文件data/modules.json失败 {e}")
        except Exception as e:
            print(f"加载模块配置文件data/modules.json失败 {type(e)} {e}")
        return _support_modules

    def update_config(self, config_data):
        """更新模块配置文件"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/modules.json", "w", encoding="utf-8") as fw:
                fw.write(json.dumps(config_data, ensure_ascii=False, indent=4))
        except Exception as e:
            print(f"写入模块配置文件data/modules.json失败 {type(e)} {e}")

    def get_funcs(self):
        # 读取本地任务信息
        funcs = {}
        for root, _, files in os.walk("data/func"):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        funcs[file] = rf.read()
                except json.JSONDecodeError as e:
                    print(f"解析自定义方法文件{file_path}失败 {e}")
                except Exception as e:
                    print(f"加载自定义方法文件{file_path}失败 {type(e)} {e}")
        return funcs

    def get_misc(self):
        # 读取本地任务信息
        funcs = {}
        for root, _, files in os.walk("data/misc"):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        funcs[file] = json.load(rf)
                except json.JSONDecodeError as e:
                    print(f"解析自定义数据文件{file_path}失败 {e}")
                except Exception as e:
                    print(f"加载自定义数据文件{file_path}失败 {type(e)} {e}")
        return funcs
