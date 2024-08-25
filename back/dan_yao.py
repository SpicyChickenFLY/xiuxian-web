"""宗门丹药模块"""

from utils import Module


class DanYao(Module):
    """宗门丹药模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)

    def get_cmd(self):
        return "宗门丹药领取"

    def run(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 丹药领取 无返回 {cd}"
        else:
            cd = self.set_delay(8, "hour")
            self._log = f"info 丹药领取 成功 {cd}"
