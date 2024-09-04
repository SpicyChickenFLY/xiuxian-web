"""自动化任务管理配置服务"""

import webbrowser
import time
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_restful import Api, Resource

import pyautogui
from mgr import TaskMgr

app = Flask(__name__, static_folder="./static/assets/", template_folder="./static/")
CORS(app)
api = Api(app)

taskMgr = TaskMgr()


@app.route("/", methods=["GET"])
def index():
    """打开前端页面"""
    return render_template("index.html")

class CursorApi(Resource):
    """光标API"""
    def get(self):
        """8秒后记录鼠标位置"""
        time.sleep(8)
        x, y = pyautogui.position()
        return {"x": x, "y": y}
    def put(self):
        """移动鼠标到指定位置"""
        coord = request.json
        if coord is None:
            return {"msg": "坐标信息不能为空"} , 400
        pyautogui.moveTo(coord["x"], coord["y"])
        return {}

class MgrApi(Resource):
    """管理器API"""
    def get(self):
        """获取管理器数据"""
        return {"data": taskMgr.get_mgr_info()}
    def put(self):
        """更新管理器状态"""
        return {"data": taskMgr.update_mgr(request.json)}

class TaskApi(Resource):
    """自动化任务API"""
    def post(self, task_name):
        """新建自动化任务"""
        return taskMgr.create_task(task_name, request.json)
    def put(self, task_name):
        """更新自动化任务"""
        return taskMgr.update_task(task_name, request.json)
    def delete(self, task_name):
        """删除自动化任务"""
        return taskMgr.delete_task(task_name)

class ModuleApi(Resource):
    """模块API"""
    def put(self, task_name, module_name):
        """更新自动化任务模块信息"""
        return taskMgr.update_module(task_name, module_name, request.json)

api.add_resource(CursorApi, '/api/cursor')
api.add_resource(MgrApi, '/api/mgr')
api.add_resource(TaskApi, '/api/mgr/task/<task_name>')
api.add_resource(ModuleApi, '/api/mgr/task/<task_name>/module/<module_name>')

if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:8010/")
    app.run(host="0.0.0.0", port=8010, debug=False)
