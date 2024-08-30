"""工具算法"""

import re
import json


class FuncUtil:
    """工具算法"""

    def find_one_int(self, args):
        """正则匹配一个整数"""
        regex = args['regex']
        resp = args['resp']
        return int(re.findall(regex, resp)[0])

    def find_one_float(self, args):
        """正则匹配一个浮点数"""
        regex = args['regex']
        resp = args['resp']
        return float(re.findall(regex, resp)[0])

    def xsl_choose_task(self, args):
        """悬赏令选取任务算法"""
        resp = args['resp']
        # 加载奖励价值表
        reward_map = {}
        try:
            with open("data/rewards_value_map.json", "r", encoding="utf-8") as rf:
                reward_map = json.load(rf)
        except Exception as e:
            print(f"加载奖励价值配置文件(data/rewards_value_map.json)失败 {type(e)} {e}")

        probailities = re.findall(r"完成几率(\d+)", resp)
        rewards = re.findall(r"可能额外获得：(.*):", resp)
        if len(probailities) == 0:
            return 1
        rewards_values = [
            reward_map[level] if level in reward_map else level for level in rewards
        ]
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
