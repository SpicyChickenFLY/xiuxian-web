"""自动化功能模块基类"""

import time
import datetime
import re

import pyautogui
import pyperclip


class Bot:
    """通用消息机器人"""

    def __init__(self, config) -> None:
        self.bot_config = {"i_x": 0.0, "i_y": 0.0, "o_x": 0.0, "o_y": 0.0}
        self.__dict__.update(config)

    def log(self, task_name, msg):
        """日志输出"""
        # 日志发送群,便于调试
        log_msg = f"{time.strftime('%m-%d %H:%M')} {task_name} - {msg}"
        pyautogui.click(self.bot_config["i_x"], self.bot_config["i_y"])
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.25)
        pyperclip.copy(log_msg)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.25)
        pyautogui.hotkey("enter")
        time.sleep(0.25)
        pyautogui.hotkey("enter")  # 确保发送
        # 日志记录文件,便于回溯
        # print(log_msg)

    def send(self, msg):
        """仅向机器人发送指令"""
        pyautogui.click(self.bot_config["i_x"], self.bot_config["i_y"])
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.25)
        pyperclip.copy("@小小")
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.75)
        pyautogui.hotkey("enter")
        pyperclip.copy(msg)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.25)
        pyautogui.hotkey("enter")
        time.sleep(0.25)
        pyautogui.hotkey("enter")  # 确保发送

    def receive(self, msg):
        """向机器人发送指令并等待回应"""
        resend = 1
        while resend > 0:
            self.send(msg)
            retry = 10
            while retry > 0:
                time.sleep(2)
                pyperclip.copy("")  # 清空剪贴板
                pyautogui.click(self.bot_config["o_x"], self.bot_config["o_y"])
                pyautogui.hotkey("ctrl", "a")
                time.sleep(0.25)
                pyautogui.hotkey("ctrl", "c")
                time.sleep(0.25)
                resp = pyperclip.paste()
                if resp != "":
                    return resp
                retry -= 1
            resend -= 1
        # 重发3次,重收10次都不行,可能是服务器问题
        return ""

    def get_bot_detail(self):
        """可视化界面机器人配置返回"""
        return self.bot_config


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

class FuncUtil():
    def find_one_int(self, resp, regex):
        return int(re.findall(r"(\d+)分钟", resp)[0])
    def find_one_float(self, resp, regex):
        return float(re.findall(r"(\d+\.?\d*)分钟", resp)[0])
    def find_all(self, resp, regex):
        pass

