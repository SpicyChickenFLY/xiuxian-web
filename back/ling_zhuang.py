"""灵庄模块"""

from utils import Module


class LingZhuang(Module):
    """灵庄模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)

    def get_cmd(self):
        return "灵庄结算"

    def run(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 灵庄结算 无返回 {cd}"
        else:
            cd = self.set_delay(1, "hour")
            self._log = f"info 灵庄结算 成功 {cd}"
