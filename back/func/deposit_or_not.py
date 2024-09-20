"""正则匹配回复中的灵石数,并准备存放"""

import re

def deposit_or_not(args) -> str:
    """正则匹配回复中的灵石数,并准备存放"""
    regex = args["regex"]
    resp = args["resp"]
    num = int(re.findall(regex, resp)[0])
    if num == 0:
        return "灵庄结算"
    return f"灵庄存灵石 {num}"
