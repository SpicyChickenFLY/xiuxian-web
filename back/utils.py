"""工具算法"""

import os
import re
import json
import time


class FuncUtil:
    """工具算法"""

    def find_one_int(self, args):
        """正则匹配一个整数"""
        regex = args["regex"]
        resp = args["resp"]
        return int(re.findall(regex, resp)[0])

    def find_one_float(self, args):
        """正则匹配一个浮点数"""
        regex = args["regex"]
        resp = args["resp"]
        return float(re.findall(regex, resp)[0])

    def xsl_choose_task(self, args):
        """悬赏令选取任务算法"""
        resp = args["resp"]
        # 加载奖励价值表
        reward_map = {}
        try:
            with open("data/rewards_value_map.json", "r", encoding="utf-8") as rf:
                reward_map = json.load(rf)
        except json.JSONDecodeError as e:
            print(f"解析奖励价值配置文件(data/rewards_value_map.json)失败 {e}")
        except Exception as e:
            print(
                f"加载奖励价值配置文件(data/rewards_value_map.json)失败 {type(e)} {e}"
            )

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

    def fs_save_price(self, args):
        progress = args["progress"]
        resp = args["resp"]

        fs_type_list = []
        fs_page_map = {}
        try:
            with open("data/fs_type_page_map.json", "r", encoding="utf-8") as rf:
                fs_type_page_map = json.load(rf)
                fs_type_list = fs_type_page_map["fs_type_list"]
                fs_page_map = fs_type_page_map["fs_page_map"]
        except json.JSONDecodeError as e:
            print(f"解析坊市类别页数配置文件(data/fs_type_page_map.json)失败 {e}")
        except Exception as e:
            print(
                f"加载坊市类别页数配置文件(data/fs_type_page_map.json)失败 {type(e)} {e}"
            )

        fs_type_name, fs_page_str = re.findall(r"坊市查看([^\d]+)(\d+)", progress)[0]
        fs_page = int(fs_page_str)
        fs_type = fs_type_list.index(fs_type_name)

        prices = re.findall(r"价格:(\d+\.?\d*)([万|亿]) (.*)", resp)

        data_dir = "data/prices"
        os.makedirs(f"{data_dir}", exist_ok=True)
        with open(
            f"{data_dir}/{fs_type_name}-{fs_page}-{time.strftime('%y%m%d-%H:%M')}.json",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(prices, ensure_ascii=False, indent=4))

        fs_page += 1
        if fs_page > fs_page_map[fs_type_list[fs_type]]:
            fs_type += 1
            fs_page = 1
        if fs_type == len(fs_type_list):
            fs_type = 0

        return f"坊市查看{fs_type_list[fs_type]}{fs_page}"

    def fs_next_duration(self, args):
        """判断坊市要不要歇会"""
        progress = args["progress"]
        fs_type_name, fs_page_str = re.findall(r"坊市查看([^\d]+)(\d+)", progress)[0]
        if fs_type_name == '技能' and fs_page_str == '1':
            return 15
        return 1

    def fs_next_unit(self, args):
        """判断坊市要不要歇会"""
        progress = args["progress"]
        fs_type_name, fs_page_str = re.findall(r"坊市查看([^\d]+)(\d+)", progress)[0]
        if fs_type_name == '技能' and fs_page_str == '1':
            return 'min'
        return 's'
