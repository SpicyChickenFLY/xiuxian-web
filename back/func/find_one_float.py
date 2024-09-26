"""正则匹配一个浮点数"""
import re

def find_one_float(args) -> float:
    """正则匹配一个浮点数"""
    regex = args["regex"]
    resp = args["resp"]
    return float(re.findall(regex, resp)[0])
