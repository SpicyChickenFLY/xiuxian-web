import re

from utils import Module


class XiuLian(Module):
    """修炼模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)

    def get_cmd(self):
        return "修炼"

    def run(self, resp):
        if "悬赏令" in resp:
            self.wait = "xsl"
            self.log = "info 普通修炼 等待悬赏"
        elif "秘境" in resp:
            self.wait = "mj"
            self.log = "info 普通修炼 等待秘境"
        elif "时间还没到" in resp:
            seconds = int(re.findall(r"有(\d+)秒", resp)[0])
            cd = self.set_delay(seconds, "s")
            self.log = f"info 普通修炼 进行中 {cd}"
        else:
            cd = self.set_delay(1, "min")
            self.log = f"info 普通修炼 成功 {cd}"
