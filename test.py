import re

folder = '1. 金融投资'
pattern = r'\d+\.\s*'
# 去除类似"1. xxx"中的"1. "
folder = re.sub(pattern, '', folder)
print(folder)