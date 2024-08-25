"""自动化机器人管理服务"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api

from task import TaskMgr

app = Flask(__name__)
CORS(app)
api = Api(app)

taskMgr = TaskMgr()

@app.route('/task/list', methods=["GET"])
def list_tasks():
    """列出所有管理任务"""
    return jsonify({"taskList": taskMgr.list_tasks()}), 200

@app.route('/task/<string: name>', methods=["GET"])
def get_task():
    """列出所有管理任务"""
    return jsonify({"taskList": taskMgr.list_tasks()}), 200

@app.route('/task/create', methods=["POST"])
def create_task():
    """创建管理任务"""
    name = taskMgr.create_task(request.form)
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
