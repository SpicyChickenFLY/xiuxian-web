"""正则匹配回复中的灵石数,并准备存放"""

import re
import json


def sell_dy_or_not(args) -> str:
    """正则匹配回复中的灵石数,并准备存放"""

    resp = args["resp"]
    dy_list = re.findall("名字：(\\w+)\n物品功效拥有数量:(\\d+)---", resp)
    if len(dy_list) == 0:
        return "宗门丹药领取"

    dy_useless_list = []
    file_name = "misc/dy_useless_list.json"
    try:
        with open(file_name, "r", encoding="utf-8") as rf:
            dy_useless_list = json.load(rf)
    except json.JSONDecodeError as e:
        print(f"解析无用丹药列表文件({file_name})失败 {e}")
    except Exception as e:
        print(
            f"加载无用丹药列表文件({file_name})失败 {type(e)} {e}"
        )
        raise e

    for (dy_name, dy_num) in dy_list:
        if dy_name in dy_useless_list:
            return f"炼金{dy_name} {dy_num}"

    return "宗门丹药领取"

# args = {
#         "resp": "名字：冰心丹\n物品功效拥有数量:3---炼金\n名字：培元丹\n物品功效拥有数量:3---炼金",
#         }
# print(sell_dy_or_not(args))
