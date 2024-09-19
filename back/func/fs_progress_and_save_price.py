"""坊市结果存文件选取下一步骤"""
import re
import json
import time
import os

def fs_progress_and_save_price(args) -> str:
    """坊市结果存文件选取下一步骤"""
    progress = args["progress"]
    resp = args["resp"]

    fs_type_list = []
    try:
        with open("misc/fs_type_list.json", "r", encoding="utf-8") as rf:
            fs_type_list = json.load(rf)
    except json.JSONDecodeError as e:
        print(f"解析坊市类别页数配置文件(misc/fs_type_page_map.json)失败 {e}")
    except Exception as e:
        print(
            f"加载坊市类别页数配置文件(misc/fs_type_page_map.json)失败 {type(e)} {e}"
        )

    fs_page_map = {}
    try:
        with open("misc/fs_page_map.json", "r", encoding="utf-8") as rf:
            fs_page_map = json.load(rf)
    except json.JSONDecodeError as e:
        print(f"解析坊市类别页数配置文件(misc/fs_type_page_map.json)失败 {e}")
    except Exception as e:
        print(
            f"加载坊市类别页数配置文件(misc/fs_type_page_map.json)失败 {type(e)} {e}"
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
