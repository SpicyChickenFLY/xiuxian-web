"""判断坊市是否一圈需要延迟时长"""
import re

def fs_next_duration(args) -> int:
    """判断坊市是否一圈需要延迟时长"""
    progress = args["progress"]
    fs_type_name, fs_page_str = re.findall(r"坊市查看([^\d]+)(\d+)", progress)[0]
    if fs_type_name == '技能' and fs_page_str == '1':
        return 15
    return 1
