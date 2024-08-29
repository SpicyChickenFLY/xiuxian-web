import re

class FuncUtil():
    def find_one_int(self, resp, regex):
        return int(re.findall(regex, resp)[0])
    def find_one_float(self, resp, regex):
        return float(re.findall(regex, resp)[0])
    def chooseTask(self, resp):
        reward_map = {} # TODO: 加载奖励价值表
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

