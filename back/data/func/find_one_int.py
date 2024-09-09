"""正则匹配一个整数"""

import re

def find_one_int(args) -> int:
    """正则匹配一个整数"""
    regex = args["regex"]
    resp = args["resp"]
    return int(re.findall(regex, resp)[0])
