"""通用消息机器人"""

import time

import pyautogui
import pyperclip


class Bot:
    """通用消息机器人"""

    def __init__(self) -> None:
        self.i_x=0.0
        self.i_y=0.0
        self.o_x=0.0
        self.o_y=0.0

    def log(self, task_name, msg):
        """日志输出"""
        # 日志发送群,便于调试
        log_msg = f"log {time.strftime('%H:%M')} {task_name} - {msg}"
        pyautogui.click(self.i_x, self.i_y)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.25)
        pyperclip.copy(log_msg)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.25)
        pyautogui.hotkey("enter")
        time.sleep(0.25)
        pyautogui.hotkey("enter")  # 确保发送

    def execute(self, cmd_type, cmd) -> str:
        """按命令类型向机器人发送/接收/监听指令"""
        if cmd_type == 'recv':
            return self.receive(cmd)
        if cmd_type == "send":
            self.send(cmd)
            return ""
        if cmd_type == 'listen':
            return self.listen()
        raise Exception("Bot: 无效的命令类型")

    def send(self, msg):
        """仅向机器人发送指令"""
        pyautogui.click(self.i_x, self.i_y)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.25)
        pyperclip.copy(msg)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.50)
        pyperclip.copy("@小小")
        pyautogui.hotkey("ctrl", "v")
        time.sleep(2.50)
        pyautogui.hotkey("enter")
        time.sleep(0.25)
        pyautogui.hotkey("enter")  # 确保发送

    def receive(self, msg):
        """向机器人发送指令并等待回应"""
        resend = 1
        while resend > 0:
            self.send(msg)
            resp = self.listen()
            if resp != "":
                return resp
            resend -= 1
        # 重发3次,重收10次都不行,可能是服务器问题
        return ""

    def listen(self):
        """向机器人发送指令并等待回应"""
        retry = 10
        while retry > 0:
            time.sleep(2)
            pyperclip.copy("")  # 清空剪贴板
            pyautogui.click(self.o_x, self.o_y)
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.25)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.25)
            resp = pyperclip.paste()
            if resp != "":
                return resp
            retry -= 1
        # 重发3次,重收10次都不行,可能是服务器问题
        return ""

    def set_bot_data(self, bot_data):
        """向机器人更新配置数据"""
        self.__dict__.update(bot_data)

    def get_bot_data(self):
        """导出机器人配置数据"""
        return {"i_x": self.i_x, "i_y": self.i_y, "o_x": self.o_x, "o_y": self.o_y}
