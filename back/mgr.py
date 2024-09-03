"""自动化任务管理器"""

import time
import threading
import os
import json
from typing import Dict

from task import Task


class TaskMgr:
    """自动化任务管理器"""

    def __init__(self) -> None:
        self._running = False
        self._thread = None
        self._task_map: Dict[str, Task] = {}

        # 读取本地任务信息
        for root, _, files in os.walk("data/tasks"):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        profile = json.load(rf)
                        self.create_task(profile["task_name"], profile)
                except json.JSONDecodeError as e:
                    print(f"解析任务配置文件{file_path}失败 {e}")
                except Exception as e:
                    print(f"加载任务配置文件{file_path}失败 {type(e)} {e}")

    def _run(self):
        """自动化程序启动"""
        while True:
            for _, task in self._task_map.items():
                if not self._running:
                    return
                try:
                    task.run()
                except Exception as e:
                    print(f"任务运行出错 {type(e)} {e}")
            if not self._running:
                return

    def is_running(self):
        """获取自动化任务启停状态"""
        return self._running

    def start(self):
        """启动自动化任务"""
        if self._running:
            print("already started")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()
        print("started")

    def stop(self):
        """停止自动化任务"""
        if not self._running:
            print("already stopped")
            return
        self._running = False
        if self._thread:
            self._thread.join()
        print("stopped")

    def set_task_bot_location(self, task_id, bot_data):
        """设置机器人点击坐标"""
        self._task_map[task_id].set_bot_data(bot_data)

    def get_mgr_info(self):
        return {"is_running": self._running, "tasks": self.list_tasks()}

    def list_tasks(self):
        """返回自动化任务列表"""
        task_list = []
        for name, task in self._task_map.items():
            task_list.append(
                {
                    "name": name,
                    "enable": task.enable,
                    "bot": task.get_bot_data(),
                    "modules": task.get_module_list(),
                }
            )
        return task_list

    def save_task(self, task_id):
        """创建新的自动化任务"""
        if self._running:
            self.stop()
            self._task_map[task_id].save()
            self.start()
        else:
            self._task_map[task_id].save()
        return ""

    def create_task(self, task_id, task_profile):
        """创建新的自动化任务"""
        if self._running:
            self.stop()
            self._task_map[task_id] = Task(task_id, task_profile)
            self.start()
        else:
            self._task_map[task_id] = Task(task_id, task_profile)
        return ""

    def delete_task(self, task_id):
        """创建新的自动化任务"""
        if self._running:
            self.stop()
            self._task_map.pop(task_id)
            os.remove(f"data/tasks/{task_id}.json")
            self.start()
        else:
            self._task_map.pop(task_id)
            os.remove(f"data/tasks/{task_id}.json")
        return task_id

    def enable_task(self, task_id):
        """启用自动化任务"""
        if self._running:
            self.stop()
            self._task_map[task_id].toggle_enable(True)
            self.start()
        else:
            self._task_map[task_id].toggle_enable(True)
        return task_id

    def disable_task(self, task_id):
        """启用自动化任务"""
        if self._running:
            self.stop()
            self._task_map[task_id].toggle_enable(False)
            self.start()
        else:
            self._task_map[task_id].toggle_enable(False)
        return task_id

    def enable_module(self, task_id, module_name):
        """启用自动化任务"""
        if self._running:
            self.stop()
            self._task_map[task_id].modules[module_name].enable = True
            self._task_map[task_id].save()
            self.start()
        else:
            self._task_map[task_id].modules[module_name].enable = True
            self._task_map[task_id].save()
        return task_id

    def disable_module(self, task_id, module_name):
        """启用自动化任务"""
        if self._running:
            self.stop()
            self._task_map[task_id].modules[module_name].enable = False
            self._task_map[task_id].save()
            self.start()
        else:
            self._task_map[task_id].modules[module_name].enable = False
            self._task_map[task_id].save()
        return task_id

    def set_module_next(self, task_id, module_name, next_trigger):
        """启用自动化任务"""
        if self._running:
            self.stop()
            self._task_map[task_id].modules[module_name].next = float(next_trigger)
            self._task_map[task_id].save()
            self.start()
        else:
            self._task_map[task_id].modules[module_name].next = float(next_trigger)
            self._task_map[task_id].save()
        return task_id
