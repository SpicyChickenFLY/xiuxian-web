"""自动化任务管理配置服务"""

import webbrowser
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_restful import Api

from mgr import TaskMgr

taskMgr = TaskMgr()

app = Flask(__name__, static_folder="./static/assets/", template_folder="./static/")
CORS(app)
api = Api(app)


@app.route("/", methods=["GET"])
def index():
    """打开前端页面"""
    return render_template("index.html")


@app.route("/taskMgr/status", methods=["GET"])
def get_task_mgr_status():
    """启动任务管理"""
    return jsonify({"result": taskMgr.is_running()}), 200


@app.route("/taskMgr/start", methods=["POST"])
def start_task_mgr():
    """启动任务管理"""
    taskMgr.start()
    return jsonify(), 200


@app.route("/taskMgr/stop", methods=["POST"])
def stop_task_mgr():
    """停止定任务管理"""
    taskMgr.stop()
    return jsonify(), 200


@app.route("/taskMgr/moveCursor", methods=["POST"])
def move_cursor():
    """列出所有管理任务"""
    return jsonify(taskMgr.move_cursor(request.json)), 200


@app.route("/taskMgr/recordCursor", methods=["POST"])
def record_cursor():
    """列出所有管理任务"""
    return jsonify(taskMgr.record_cursor()), 200


@app.route("/task/setBot/<string:task_name>", methods=["POST"])
def set_task_bot(task_name):
    """列出所有管理任务"""
    return jsonify(taskMgr.set_task_bot_location(task_name, request.json)), 200


@app.route("/task/list", methods=["GET"])
def list_tasks():
    """列出所有管理任务"""
    return jsonify(taskMgr.list_tasks()), 200


@app.route("/task/save/<string:name>", methods=["POST"])
def save_task(name):
    """删除指定管理任务"""
    result = taskMgr.save_task(name)
    return jsonify({"result": result}), 200

@app.route("/task/create/<string:task_name>", methods=["POST"])
def create_task(task_name):
    """创建管理任务"""
    try:
        taskMgr.create_task(task_name, request.form)
        return jsonify({"result": "成功"}), 200
    except Exception as e:
        return jsonify({"result": "失败", "msg": f"{type(e)} - {e}"}), 500


@app.route("/task/delete/<string:name>", methods=["POST"])
def delete_task(name):
    """删除指定管理任务"""
    result = taskMgr.delete_task(name)
    return jsonify({"result": result}), 200


@app.route("/task/enable/<string:name>", methods=["POST"])
def enable_task(name):
    """启用指定管理任务"""
    result = taskMgr.enable_task(name)
    return jsonify({"result": result}), 200


@app.route("/task/disable/<string:name>", methods=["POST"])
def disable_task(name):
    """禁用指定管理任务"""
    result = taskMgr.disable_task(name)
    return jsonify({"result": result}), 200


@app.route("/module/enable/<string:task_name>/<string:module_name>", methods=["POST"])
def enable_module(task_name, module_name):
    """查询指定管理任务的模块信息"""
    return jsonify(taskMgr.enable_module(task_name, module_name)), 200


@app.route("/module/disable/<string:task_name>/<string:module_name>", methods=["POST"])
def disable_module(task_name, module_name):
    """查询指定管理任务的模块信息"""
    return jsonify(taskMgr.disable_module(task_name, module_name)), 200


@app.route(
    "/module/<string:task_name>/<string:module_name>/setNext/<string:next_trigger>",
    methods=["POST"],
)
def set_module_next(task_name, module_name, next_trigger):
    """查询指定管理任务的模块信息"""
    return jsonify(taskMgr.set_module_next(task_name, module_name, next_trigger)), 200


if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:8010/")
    app.run(host="0.0.0.0", port=8010)
