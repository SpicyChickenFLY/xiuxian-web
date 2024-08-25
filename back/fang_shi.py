"""坊市模块"""

import re
import json
import time

from utils import Module


class FangShi(Module):
    """坊市模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)
        self.fs_type_list = ["技能", "装备", "丹药", "药材"]
        self.fs_page_map = {
            "技能": 9,
            "装备": 3,
            "丹药": 3,
            "药材": 7,
        }
        self.type = 1
        self.page = 1
        self.data = {}

    def _next_page(self):
        self.page += 1
        if self.page > self.fs_page_map[self.fs_type_list[self.type]]:
            self.type += 1
            self.page = 1
        if self.type == len(self.fs_type_list):
            self.type = 1
            return True
        return False

    def get_cmd(self):
        if self.progress == "never":
            return ""
        return f"坊市查看{self.fs_type_list[self.type]}{self.page}"

    def run(self, resp):
        msg = f"坊市查看{self.fs_type_list[self.type]}{self.page}"
        if resp == "":
            cd = self.set_delay(15, "min")
            self._log = f"warn 秘境结算 {msg} 无返回 {cd}"
        elif "线下交易" in resp:
            prices = re.findall(r"价格:(\d+\.?\d*)([万|亿]) (.*)", resp)
            self.data[time.strftime("%m-%d %H:%M:%S")] = prices

            if self._next_page():
                cd = self.set_delay(15, "min")
                self._log = f"info {msg} 成功 {cd}"
                with open("price.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(self.data, ensure_ascii=False, indent=4))
            else:
                cd = self.set_delay(5, "s")
                self._log = f"info {msg} 成功 {cd}"
        else:
            cd = self.set_delay(15, "min")
            self._log = f"warn {msg} 返回异常{resp} {cd}"
