import re

class FuncUtil():
    def find_one_int(self, resp, regex):
        return int(re.findall(r"(\d+)分钟", resp)[0])
    def find_one_float(self, resp, regex):
        return float(re.findall(r"(\d+\.?\d*)分钟", resp)[0])
    def find_all(self, resp, regex):
        pass

