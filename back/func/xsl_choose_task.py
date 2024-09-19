"""悬赏令选取任务算法"""

import re
import json

def xsl_choose_task(args) -> str:
    """悬赏令选取任务算法"""
    resp = args["resp"]

    # 加载奖励价值表
    reward_map = {}
    try:
        with open("misc/reward_value_map.json", "r", encoding="utf-8") as rf:
            reward_map = json.load(rf)
    except json.JSONDecodeError as e:
        print(f"解析奖励价值配置文件(misc/reward_value_map.json)失败 {e}")
    except Exception as e:
        print(
            f"加载奖励价值配置文件(misc/reward_value_map.json)失败 {type(e)} {e}"
        )
        raise e

    # 拼装悬赏令任务信息
    probailities = re.findall(r"完成几率(\d+)", resp)
    rewards = re.findall(r"可能额外获得：(.*):", resp)
    if len(probailities) == 0:
        return "悬赏令接取1"
    rewards_values = [
        reward_map[level] if level in reward_map else level for level in rewards
    ]
    tasks = sorted(
        list(zip(probailities, rewards_values)),
        key=lambda x: x[1],
        reverse=True,
    )

    # 根据算法选择任务
    choice = 1
    while choice <= len(tasks) and int(tasks[choice - 1][0]) < 70:
        choice += 1
    if choice > len(tasks):
        choice = 1
    return f"悬赏令接取{choice}"
