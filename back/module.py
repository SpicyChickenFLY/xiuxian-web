import time
import datetime

class Module:
    """自动化功能模块基类"""

    def __init__(self, config) -> None:
        self.name = ""
        self.enable = False
        self.prev = 0.0
        self.next = 0.0
        self.progress = ""
        self.wait = ""

        self.log = ""

        self.__dict__.update(config)

    def record_prev(self):
        self.prev = time.time()

    def set_delay(self, duration, unit):
        """设置下次触发时间为定长的延迟"""
        scale = {"s": 1, "min": 60, "h": 60 * 60, "d": 24 * 60 * 60}
        self.next = time.time() + duration * scale[unit]
        return f"cd {duration}{unit}"

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
            return f"cd {days}日后{hour}:{minute}:{second}"
        return f"cd 今日{hour}:{minute}:{second}"

    def set_next_timestamp(self, timestamp):
        self.next = time.time()

    def _info(self, result, *extra):
        self.log = f"[I] {self.progress} {result} {"".join(extra)}"

    def run(self, resp):
        """运行接口"""
        raise NotImplementedError("模块未实现运行接口")

    def get_cmd(self):
        """命令接口"""
        raise NotImplementedError("模块未实现获取命令接口")

    def get_module_base_detail(self):
        return {
            "name": self.name,
            "enable": self.enable,
            "prev": self.prev,
            "next": self.next,
            "progress": self.progress,
            "wait": self.wait,
        }