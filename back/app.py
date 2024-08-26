"""自动化任务管理器及配置服务"""

import threading
import os
import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api

from task import Task

class TaskMgr():
    """自动化任务管理器"""

    def __init__(self) -> None:
        self._running = False
        self._thread = None
        self._task_map = {}

        # 读取本地任务信息
        for root, _, files in os.walk('profiles'):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as rf:
                        print(file_path)
                        self.create_task(json.load(rf))
                except Exception as e:
                    print(f"根据配置文件{file_path}创建任务失败 {type(e)} {e}")

    def _run(self):
        """自动化程序启动"""
        while True:
            for _, task in self._task_map.items():
                if not self._running:
                    return
                task.run()

    def is_running(self):
        """获取自动化任务启停状态"""
        return self._running

    def start(self):
        """启动自动化任务"""
        if self._running:
            print('started')
            return
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        """停止自动化任务"""
        if not self._running:
            print('stopped')
            return
        self._running = False
        if self._thread:
            self._thread.join()

    def list_tasks(self):
        """返回自动化任务列表"""
        task_list = []
        for name, task in self._task_map.items():
            task_list.append({ "name": name, "modules": task.get_brief() })
        return task_list

    def get_task(self, task_id):
        """返回自动化任务详情"""
        self._task_map[task_id].export()

    def create_task(self, task_profile):
        """创建新的自动化任务"""
        if self._running:
            self.stop()
            name = task_profile['name']
            self._task_map[name] = Task(name, task_profile)
            self.start()
        else:
            name = task_profile['name']
            self._task_map[name] = Task(name, task_profile)
        return name

    def update_task(self, task_id, task_profile):
        """创建新的自动化任务"""
        if self._running:
            self.stop()
            self._task_map[task_id].update(task_profile)
            self.start()
        else:
            self._task_map[task_id].update(task_profile)
        return task_id

    def delete_task(self, task_id):
        """创建新的自动化任务"""
        if self._running:
            self.stop()
            self._task_map.pop(task_id)
            self.start()
        else:
            self._task_map.pop(task_id)
        return task_id
taskMgr = TaskMgr()


app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/task/list', methods=["GET"])
def list_tasks():
    """列出所有管理任务"""
    return jsonify(taskMgr.list_tasks()), 200

@app.route('/task/<string:name>', methods=["GET"])
def get_task(name):
    """查询指定管理任务"""
    return jsonify({"taskList": taskMgr.get_task(name)}), 200

@app.route('/task/create', methods=["POST"])
def create_task():
    """创建管理任务"""
    name = taskMgr.create_task(request.form)
    if name == "":
        return jsonify({"msg": "创建失败"}), 400
    return jsonify({"taskId": name}), 200

@app.route('/task/update', methods=["POST"])
def update_task(name):
    """创建管理任务"""
    result = taskMgr.update_task(name, request.form)
    return jsonify({"result": result}), 200

@app.route('/task/delete/<string:name>', methods=["POST"])
def delete_task(name):
    """删除指定管理任务"""
    result = taskMgr.delete_task(name)
    return jsonify({"result": result}), 200

@app.route('/taskMgr/start', methods=["POST"])
def start_task_mgr():
    """启动任务管理"""
    taskMgr.start()
    return jsonify(), 200

@app.route('/taskMgr/stop', methods=["POST"])
def stop_task_mgr():
    """停止定任务管理"""
    taskMgr.stop()
    return jsonify(), 200

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8010)
