"""补偿模块"""

from utils import Module

class BuChang(Module):
    """补偿模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)

    def get_cmd(self):
        return "补偿"

    def run(self, resp):
        cd = self.set_delay(12, "h")
        self.log = f"info 补偿 成功 {cd}"
