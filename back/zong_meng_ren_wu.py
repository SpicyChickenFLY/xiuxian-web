"""宗门任务模块"""

import re
import unittest

from utils import Module


class ZongMenRenWu(Module):
    """宗门任务模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)

    def __jie_qu(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 宗门接取 无返回 {cd}"
        elif "今日无法再获取" in resp:
            cd = self.set_next_period(7, 0, 0)
            self._log = "info 宗门接取 跳过 {cd}"
        elif "除害" in resp:  # 查抄
            self.progress = "完成"
            self._log = "info 宗门接取 成功"
        else:
            self.progress = "刷新"
            self._log = "info 宗门接取 无效"

    def __shua_xin(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 宗门接取 无返回 {cd}"
        elif "除害" in resp:  # "查抄"
            self.progress = "完成"
            self._log = "info 宗门刷新 成功"
        elif "没有宗门任务" in resp:
            cd = self.set_delay(10, "s")
            self._log = f"info 宗门刷新 回退 {cd}"
            self.progress = ""
        elif "时间还没到" in resp:
            seconds = int(re.findall(r"(\d+)秒", resp)[0])
            cd = self.set_delay(seconds, "s")
            self._log = f"info 宗门刷新 进行中 {cd}"
        else:
            cd = self.set_delay(3, "min")
            self._log = f"info 宗门刷新 无效 {cd}"

    def __wan_cheng(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 宗门完成 无返回 {cd}"
        elif "冷静一下" in resp:
            seconds = int(re.findall(r"(\d+)秒", resp)[0])
            cd = self.set_delay(seconds, "s")
            self._log = "info 宗门结算 进行中 {cd}"
        elif "不扣你任务次数了" in resp:
            cd = self.set_delay(10, "min")
            self._log = "info 宗门结算 无效"
        elif "当前没有接取宗门任务" in resp:
            self.progress = ""
            cd = self.set_delay(10, "min")
            self._log = "info 宗门结算 回退 {cd}"
        elif "宗门贡献" in resp:
            self.progress = ""
            self._log = "info 宗门结算 完成 {cd}"

    def get_cmd(self):
        if self.progress == "宗门任务接取":
            return "宗门任务接取"
        if self.progress == "宗门任务刷新":
            return "宗门任务刷新"
        if self.progress == "宗门任务完成":
            return "宗门任务完成"
        return "宗门任务接取"

    def run(self, resp):
        if self.progress == "宗门任务接取":
            self.__jie_qu(resp)
        elif self.progress == "宗门任务刷新":
            self.__shua_xin(resp)
        elif self.progress == "宗门任务完成":
            self.__wan_cheng(resp)
        else:
            self.__jie_qu(resp)
