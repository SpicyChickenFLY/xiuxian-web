"""悬赏令模块"""

import re

from utils import Module


class XuanShangLing(Module):
    """悬赏令模块"""

    def __init__(self, profile) -> None:
        Module.__init__(self, profile)
        self._choice = 1

    def __assemble_resp_to_task(self, resp):
        """组装概率与奖励与时长"""
        reward_map = {
            "一品药材": 50,
            "人阶下品": 50,
            "人阶上品": 50,
            "二品药材": 100,
            "黄阶下品": 130,
            "三品药材": 140,
            "黄阶上品": 160,
            "四品药材": 170,
            "玄阶下品": 190,
            "五品药材": 200,
            "玄阶上品": 220,
            "六品药材": 230,
            "地阶下品": 250,
            "七品药材": 260,
            "地阶上品": 280,
            "八品药材": 290,
            "天阶下品": 310,
            "九品药材": 320,
            "天阶上品": 340,
            "十品药材": 350,
            "仙阶下品": 360,
            "仙阶上品": 360,
        }
        probailities = re.findall(r"完成几率(\d+)", resp)
        rewards = re.findall(r"可能额外获得：(.*):", resp)
        if len(probailities) == 0:
            return 1
        rewards_values = [reward_map[i] if i in reward_map else i for i in rewards]
        tasks = sorted(
            list(zip(probailities, rewards_values)),
            key=lambda x: x[1],
            reverse=True,
        )
        choice = 1
        while choice <= len(tasks) and int(tasks[choice - 1][0]) < 80:
            choice += 1
        if choice > len(tasks):
            choice = 1
        return choice

    def __shua_xin(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self.log = f"warn 悬赏刷新 无返回 {cd}"
        elif "进行中的" in resp:
            self.progress = "悬赏令结算"
        elif "的个人悬赏令" in resp:
            choice = self.__assemble_resp_to_task(resp)
            self.log = f"info 悬赏令刷新 选择{choice}"
            self.progress = f"悬赏令接取{choice}"
        elif "次数已用尽" in resp:
            cd = self.set_delay(8, "h")
            self.log = f"info 悬赏令刷新 跳过 {cd}"
        elif "秘境" in resp:
            self.wait = "mj"
            self.log = "info 悬赏令刷新 等待秘境"
        else:
            cd = self.set_delay(15, "min")
            self.log = f"warn 悬赏令刷新 返回异常{resp} {cd}"

    def __jie_qu(self, resp):
        if resp == "":
            cd = self.set_delay(15, "min")
            self.log = f"warn 悬赏接取 无返回 {cd}"
        elif "没有可以接取的" in resp:
            self.progress = ""
            self.log = "info 悬赏接取 回退"
        elif "成功" in resp:
            self.progress = "悬赏令结算"
            self.log = "info 悬赏接取 成功"
        else:
            cd = self.set_delay(15, "min")
            self.log = "warn 悬赏接取 返回异常{resp} {cd}"

    def __jie_suan(self, resp):
        if "悬赏令结算" in resp:
            self.progress = "悬赏令刷新"
            cd = self.set_delay(10, "s")
            self.log = f"info 悬赏令结算 完成 {cd}"
        elif "没有查到" in resp:
            self.progress = "悬赏令刷新"
            cd = self.set_delay(10, "s")
            self.log = f"info 悬赏令结算 回退 {cd}"
        elif "进行中的" in resp:
            minutes = float(re.findall(r"(\d+\.?\d*)分钟", resp)[0])
            cd = self.set_delay(minutes, "min")
            self.log = f"info 悬赏结算 进行中 {cd}"
        else:
            cd = self.set_delay(15, "min")
            self.log = "warn 悬赏结算 返回异常{resp} {cd}"

    def get_cmd(self):
        if self.progress == "悬赏令刷新":
            return ("悬赏令刷新",)
        if self.progress == "悬赏令接取":
            return (f"悬赏令接取{self._choice}",)
        if self.progress == "悬赏令结算":
            return "悬赏令结算"
        return "悬赏令刷新"

    def run(self, resp):
        if self.progress == "":
            self.__shua_xin(resp)
        elif "悬赏令接取" in self.progress:
            self.__jie_qu(resp)
        elif self.progress == "悬赏令结算":
            self.__jie_suan(resp)
