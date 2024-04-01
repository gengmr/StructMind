# -*- coding: utf-8 -*-
import json
import pyperclip


def print_json_contents(file_path):
    """
    读取指定路径的JSON文件，并根据提供的模板打印其内容。

    :param file_path: JSON文件的路径
    :param template: 用于打印的模板字符串
    """
    with open(file_path, 'r', encoding='utf8') as file:
        data = json.load(file)
    template = """
作为专家级提示工程师，你的任务是参照标准prompt模版及相关字段字典（json形式）修改给定json文件内容(参数格式化部分格式保持一致)。请仅返回修改后的json（确保语言专业、准确）。其中UsageDescription字段尽可能简洁。
标准prompt模版及相关字段字典如下：
```
{
  "IsVisible": true,
  "Icon": "pen",
  "UsageDescription": "按照通用文本撰写要求和特定用户要求生成文本。",
  "PromptTemplate": "作为一名专业的文本编辑和创作专家，你的任务是根据客户提供的详细信息进行专业、全面、具体、有逻辑性的文本创作与编辑服务。请根据以下步骤操作：\n请仔细审阅以下信息\n```\n文章类型：\n{***}\n写作目的和读者对象：\n{***}\n详细写作要求和指导：\n{***}\n```\n根据以上信息，开始你的创作或编辑工作。请确保最终文本：\n- 紧密围绕写作目的和读者对象展开\n- 详细且逻辑清晰地反映所有的写作要求和指导\n- 完成写作后，请检查并确认以下内容是否满足要求：\n  - 是否包含所有要求的元素\n  - 文本结构是否清晰、逻辑性是否强\n  - 语言风格和内容是否适合目标读者",
  "Inputs": [
    {
      "InputPlaceholder": "请输入您的撰写文章类型（例如：科研文章、商业计划书、博客、社交媒体帖子等）。",
      "InputLabel": "文章类型"
    },
    {
      "InputPlaceholder": "描述您的写作目的和读者对象（例如：发表于学术期刊、企业内部沟通、公众阅读等）。",
      "InputLabel": "目的与对象"
    },
    {
      "InputPlaceholder": "提供具体、详细写作要求和指导（例如：主题、字数、关键词、格式要求、截止日期、语言风格等）。",
      "InputLabel": "具体要求"
    }
  ]
}
```

需要修改的json如下：
```
{}
```
    """
    template = template.replace('{}', json.dumps(data, ensure_ascii=False, indent=2))
    print(template)
    pyperclip.copy(template)


if __name__ == '__main__':
    # 指定你的JSON文件路径
    json_file_path = 'config/菜单配置/8. 探索模式/1. 编程【仅测试】/01. 思路分析【仅测试】.json'
    # # 调用函数
    # print_json_contents(json_file_path)


