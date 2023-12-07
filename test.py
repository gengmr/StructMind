import re

def escape_latex_special_chars(text):
    """
    转义 LaTeX 中的特殊字符，对 \alert{...} 结构内的内容除 \、{ 和 } 外的字符进行转义。

    参数:
    text (str): 需要转义的字符串。

    返回:
    str: 转义后的字符串。
    """

    # 定义 LaTeX 特殊字符及其转义形式
    special_chars = {
        '\\': '\\\\',
        '{': '\\{',
        '}': '\\}',
        '%': '\\%',
        '$': '\\$',
        '&': '\\&',
        '#': '\\#',
        '_': '\\_',
        '^': '\\^',
        '~': '\\~'
    }

    # 用于匹配 \alert{...} 结构的正则表达式
    alert_pattern = re.compile(r'(\\alert\{.*?\})')

    def escape_part(part):
        if alert_pattern.fullmatch(part):
            # 对于 \alert{...} 结构，只转义内部的特殊字符，除了 \、{ 和 }
            return re.sub(r'([%$&#_^~])', lambda m: special_chars[m.group()], part)
        else:
            # 对于其他文本，转义所有特殊字符
            return ''.join(special_chars.get(char, char) for char in part)

    # 分割文本并应用转义
    parts = alert_pattern.split(text)
    escaped_text = ''.join(escape_part(part) for part in parts)

    return escaped_text


examples = [
    "This is a test with no special characters.",
    "This is a test with special characters: %, $, &, #, _, ^, ~.",
    "This is a test with \\alert{special characters inside}.",
    "This is a test with \\alert{special characters %, $, &, #, _, ^, ~ inside}fds.",
    "This is a test with nested \\alert{\\alert{special characters inside}}.",
]
# 应用函数并输出结果
escaped_examples = [escape_latex_special_chars(text) for text in examples]
for escaped_example in escaped_examples:
    print(escaped_example)

