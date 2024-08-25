"""秘境模块"""

import re

from utils import Module


class MiJing(Module):
    """秘境模块"""

    def __tan_suo(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 探索秘境 无返回 {cd}"
        elif "正在秘境中" in resp or "进入秘境" in resp:
            self.progress = "秘境结算"
        elif "道友已经参加过本次秘境啦" in resp:
            cd = self.set_next_period(13, 0, 0)
            self._log = f"info 探索秘境 跳过 {cd}"
        elif "修炼" in resp:
            self.wait = "xl"
            self._log = "info 探索秘境 等待修炼"
        elif "悬赏令" in resp:
            self.wait = "xsl"
            self._log = "info 探索秘境 等待悬赏"
        else:
            cd = self.set_delay(15, "min")
            self._log = f"warn 探索秘境 无返回{resp} {cd}"

    def __jie_suan(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 秘境结算 无返回 {cd}"
        elif "进行中的" in resp:
            minutes = int(re.findall(r"预计(\d+)分钟", resp)[0])
            cd = self.set_delay(minutes, "min")
            self._log = f"warn 秘境结算 进行中 {cd}"
        else:
            self.progress = "探索秘境"
            cd = self.set_next_period(13, 0, 0)
            self._log = "info 秘境结算 完成 {cd}"

    def get_cmd(self):
        if self.progress == "探索秘境":
            return "探索秘境"
        if self.progress == "秘境结算":
            return "秘境结算"
        return "探索秘境"

    def run(self, resp):
        if self.progress == "探索秘境":
            self.__tan_suo(resp)
        elif self.progress == "秘境结算":
            self.__jie_suan(resp)
        else:
            self.__tan_suo(resp)
