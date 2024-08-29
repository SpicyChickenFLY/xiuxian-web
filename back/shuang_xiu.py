"""双修模块"""

from utils import Module


class ShuangXiu(Module):
    """双修模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)
        self.target = "北条惠古"

    def get_cmd(self):
        return f"双修 {self.target}"

    def run(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self.log = f"warn 双修 无返回 {cd}"
        elif "情投意合" in resp:
            cd = self.set_delay(5, "s")
            self.log = f"warn 双修 成功 {cd}"
        elif "到达上限" in resp:
            cd = self.set_delay(12, "h")
            self.log = f"warn 双修 跳过 {cd}"
        elif "无法与自己" in resp:
            cd = self.set_delay(12, "h")
            self.log = f"warn 双修 跳过 {cd}"
        else:
            cd = self.set_delay(15, "min")
            self.log = f"warn 双修 返回异常{resp} {cd}"
