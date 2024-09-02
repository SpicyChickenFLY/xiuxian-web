"""自动化功能模块基类"""

import time
import datetime
import re
import copy

from utils import FuncUtil


class Module:
    """自动化功能模块基类"""

    def __init__(self, profile, data) -> None:
        self.progress_profiles = profile["progress_profile"]

        self.name = ""
        self.enable = False
        self.prev = 0.0
        self.next = 0.0
        self.progress = ""
        self.log = ""
        self.__dict__.update(data)
        self.wait = "" # 等待状态每次都需要重置，避免死锁

        # 给异常状态附上默认值
        if self.progress == "" or self.progress not in profile:
            self.progress = profile["default_cmd"]

    def record_prev(self):
        """记录本次触发发生时间"""
        self.prev = time.time()

    def set_delay(self, duration, unit):
        """设置下次触发时间为定长的延迟"""
        scale = {"s": 1, "min": 60, "h": 60 * 60, "d": 24 * 60 * 60}
        self.next = time.time() + duration * scale[unit]
        self.log += f" cd {duration}{unit}"

    def set_next_period(self, hour, minute, second):
        """设置下次触发时间为指定的时间点"""
        now = datetime.datetime.now()
        curr_period = now.replace(hour=hour, minute=minute, second=second + 5)
        days = 0
        while curr_period < now:
            curr_period += datetime.timedelta(days=1)
            days += 1
        self.next = time.mktime(curr_period.timetuple())
        if days > 0:
            self.log += f" cd  {days}日后{hour}:{minute}:{second}"
        else:
            self.log += f" cd  今日{hour}:{minute}:{second}"

    def set_next_timestamp(self, timestamp):
        """直接设置下次触发时间的时间戳"""
        self.next = timestamp

    def is_runnable(self):
        """判断模块是否达到触发条件"""
        return self.enable and self.wait == "" and time.time() > self.next

    def run(self, resp):
        """运行模块功能"""
        progress_profile = {}
        for progress_regex in self.progress_profiles:
            if len(re.findall(progress_regex, self.progress)) > 0:
                progress_profile = self.progress_profiles[progress_regex]
                break
        else:
            self.log = f"{self.progress} 获取状态配置异常"
        run_data = copy.deepcopy(progress_profile)
        if progress_profile["type"] == "recv":
            if resp == "":
                self.log = f"{self.progress} 无返回"
                self.set_delay(15, "min")
                return
            # 尝试匹配回复消息
            for resp_regex, _run_data in progress_profile["resp"].items():
                if len(re.findall(resp_regex, resp)) > 0:
                    run_data = copy.deepcopy(_run_data)
                    break
            else:
                self.log = f"{self.progress} 返回异常{resp}"
                self.set_delay(1, "min")
                return

        # 预处理数据
        if "pre" in run_data:
            for data_key, func_info in run_data["pre"].items():
                func_info["args"]["resp"] = resp
                func_info["args"]["progress"] = self.progress
                run_data[data_key] = getattr(FuncUtil(), func_info["func_name"])(
                    func_info["args"]
                )

        # 更新模块数据
        self.log = f"{self.progress} {run_data['result']}"
        if "next_type" in run_data:
            if run_data["next_type"] == "delay":
                self.set_delay(run_data["next_duration"], run_data["next_unit"])
            else:
                self.set_next_period(
                    run_data["next_hour"],
                    run_data["next_minute"],
                    run_data["next_second"],
                )
        if "wait" in run_data:
            self.wait = run_data["wait"]
        if "progress" in run_data:
            self.progress = run_data["progress"]

    def get_cmd_type(self):
        """命令接口"""
        for resp_regex, progress_profile in self.progress_profiles.items():
            if len(re.findall(resp_regex, self.progress)) > 0:
                cmd_type = progress_profile["type"]
                return cmd_type

    def get_module_base_detail(self):
        """组装任务各个模块信息"""
        return {
            "name": self.name,
            "enable": self.enable,
            "prev": self.prev,
            "next": self.next,
            "progress": self.progress,
            "wait": self.wait,
        }
