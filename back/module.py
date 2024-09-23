"""自动化功能模块基类"""

import time
import datetime
import re
import copy
import importlib


class Module:
    """自动化功能模块基类"""

    def __init__(self, module_name, plugin, module_data, path) -> None:
        self._progress_profiles = plugin["progress_profile"]
        self._path = path

        self.priority = plugin["priority"]
        self.name = module_name
        self.enable = True
        self.prev = 0.0
        self.next = 0.0
        self.progress = ""
        self.log = ""
        self.wait = ""  # 等待状态每次都需要重置，避免死锁
        self.__dict__.update(module_data)

        # 给异常状态附上默认值
        if self.progress == "" or self.progress not in plugin:
            self.progress = plugin["default_cmd"]

    def get_module_data(self):
        """组装任务各个模块信息"""
        return {
            "name": self.name,
            "enable": self.enable,
            "prev": self.prev,
            "next": self.next,
            "progress": self.progress,
            "wait": self.wait,
            "log": self.log,
        }

    def update_module(self, module_data):
        """更新模块信息"""
        self.__dict__.update(module_data)

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
            self.log += f" cd {days}日后{hour}:{minute}:{second}"
        else:
            self.log += f" cd 今日{hour}:{minute}:{second}"

    def set_next_timestamp(self, timestamp):
        """直接设置下次触发时间的时间戳"""
        self.next = timestamp
        self.log += (
            f" cd {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}"
        )

    def _get_progress_profile(self):
        progress_profile = None
        for progress_regex in self._progress_profiles:
            if len(re.findall(progress_regex, self.progress)) > 0:
                progress_profile = self._progress_profiles[progress_regex]
                break
        return progress_profile

    def _get_run_data(self, resp, progress_profile):
        run_data = None
        if progress_profile["type"] == "send":
            run_data = copy.deepcopy(progress_profile)
        elif progress_profile["type"] == "recv":
            if resp == "":
                return None
            # 尝试匹配回复消息
            for _run_data in progress_profile["resp"]:
                if len(re.findall(_run_data["resp"], resp)) > 0:
                    run_data = copy.deepcopy(_run_data)
                    break
        return run_data

    def _pre_run(self, resp, run_data):
        if "pre" not in run_data:
            return run_data

        # 预处理数据
        for data_key, func_info in run_data["pre"].items():
            func_info["args"]["resp"] = resp
            func_info["args"]["progress"] = self.progress
            module = importlib.import_module(f'func.{func_info["func_name"]}')
            func = getattr(module, func_info["func_name"])
            run_data[data_key] = func(func_info["args"])
        return run_data

    def run(self, resp, trigger):
        """运行模块功能"""
        self.prev = trigger
        self.wait = ""

        progress_profile = self._get_progress_profile()
        if progress_profile is None:
            self.log = f"{self.progress} 获取状态配置异常"
            self.set_delay(15, "min")
            return self.wait, self.log

        run_data = self._get_run_data(resp, progress_profile)
        if run_data is None:
            self.log = f"{self.progress} 返回异常({resp})"
            self.set_delay(5, "min")
            return self.wait, self.log

        run_data = self._pre_run(resp, run_data)

        # 根据模块配置匹配填充返回数据
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
        return self.wait, self.log

    def get_next_cmd_and_cmd_type(self):
        """命令接口"""
        progress_profile = self._get_progress_profile()
        if progress_profile is None:
            return self.progress, "send"
        return self.progress, progress_profile["type"]
