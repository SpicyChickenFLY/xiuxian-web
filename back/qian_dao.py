"""签到模块"""

from utils import Module


class QianDao(Module):
    """签到模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)

    def get_cmd(self):
        return "修仙签到"

    def run(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 修仙签到 无返回 {cd}"
        else:
            cd = self.set_delay(8, "hour")
            self._log = f"info 修仙签到 成功 {cd}"
