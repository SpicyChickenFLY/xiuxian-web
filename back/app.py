"""自动化任务管理配置服务"""

import webbrowser
import time
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_restful import Api

import pyautogui
from mgr import TaskMgr

taskMgr = TaskMgr()

app = Flask(__name__, static_folder="./static/assets/", template_folder="./static/")
CORS(app)
api = Api(app)


@app.route("/", methods=["GET"])
def index():
    """打开前端页面"""
    return render_template("index.html")


@app.route("/api/moveCursor", methods=["POST"])
def move_cursor():
    """移动鼠标到指定位置"""
    coord = request.json
    if coord is not None:
        pyautogui.moveTo(coord["x"], coord["y"])
        return jsonify({}), 200
    return jsonify({}), 500


@app.route("/api/recordCursor", methods=["POST"])
def record_cursor():
    """8秒后记录鼠标位置"""
    time.sleep(8)
    x, y = pyautogui.position()
    return jsonify({"x": x, "y": y}), 200


@app.route("/api/taskMgr/status", methods=["GET"])
def get_task_mgr_status():
    """启动任务管理"""
    return jsonify({"result": taskMgr.is_running()}), 200


@app.route("/api/taskMgr/start", methods=["POST"])
def start_task_mgr():
    """启动任务管理"""
    taskMgr.start()
    return jsonify(), 200


@app.route("/api/taskMgr/stop", methods=["POST"])
def stop_task_mgr():
    """停止定任务管理"""
    taskMgr.stop()
    return jsonify(), 200


@app.route("/api/task/setBot/<string:task_name>", methods=["POST"])
def set_task_bot(task_name):
    """列出所有管理任务"""
    return jsonify(taskMgr.set_task_bot_location(task_name, request.json)), 200


@app.route("/api/task/list", methods=["GET"])
def list_tasks():
    """列出所有管理任务"""
    return jsonify(taskMgr.list_tasks()), 200


@app.route("/api/task/save/<string:name>", methods=["POST"])
def save_task(name):
    """删除指定管理任务"""
    result = taskMgr.save_task(name)
    return jsonify({"result": result}), 200


@app.route("/api/task/create/<string:task_name>", methods=["POST"])
def create_task(task_name):
    taskMgr.create_task(task_name, request.form)
    return jsonify({"result": "成功"}), 200


@app.route("/api/task/delete/<string:name>", methods=["POST"])
def delete_task(name):
    """删除指定管理任务"""
    result = taskMgr.delete_task(name)
    return jsonify({"result": result}), 200


@app.route("/api/task/enable/<string:name>", methods=["POST"])
def enable_task(name):
    """启用指定管理任务"""
    result = taskMgr.enable_task(name)
    return jsonify({"result": result}), 200


@app.route("/api/task/disable/<string:name>", methods=["POST"])
def disable_task(name):
    """禁用指定管理任务"""
    result = taskMgr.disable_task(name)
    return jsonify({"result": result}), 200


@app.route(
    "/api/module/enable/<string:task_name>/<string:module_name>", methods=["POST"]
)
def enable_module(task_name, module_name):
    """查询指定管理任务的模块信息"""
    return jsonify(taskMgr.enable_module(task_name, module_name)), 200


@app.route(
    "/api/module/disable/<string:task_name>/<string:module_name>", methods=["POST"]
)
def disable_module(task_name, module_name):
    """查询指定管理任务的模块信息"""
    return jsonify(taskMgr.disable_module(task_name, module_name)), 200


@app.route(
    "/api/module/<string:task_name>/<string:module_name>/setNext/<string:next_trigger>",
    methods=["POST"],
)
def set_module_next(task_name, module_name, next_trigger):
    """查询指定管理任务的模块信息"""
    return jsonify(taskMgr.set_module_next(task_name, module_name, next_trigger)), 200


if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:8010/")
    app.run(host="0.0.0.0", port=8010)
