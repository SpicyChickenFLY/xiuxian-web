"""灵田模块"""

import re

from utils import Module


class LingTian(Module):
    """灵田模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)

    def get_cmd(self):
        return "灵田收取"

    def run(self, resp):
        if "道友成功收取药材" in resp:
            cd = self.set_delay(48, "h")
            self.log = "info 灵田收取 成功 {cd}"
        elif "道友的灵田还不能收取，下次收取时间为" in resp:
            hours = float(re.findall(r"(\d+\.?\d*)小时", resp)[0])
            cd = self.set_delay(hours, "h")
            self.log = "info 灵田收取 进行中 {cd}"
        else:
            cd = self.set_delay(15, "min")
            self.log = f"warn 灵田收取 返回异常{resp} {cd}"
