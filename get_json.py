# -*- coding: utf-8 -*-
import json
import pyperclip


def modify_json_template(EnglishPromptTemplate):
    # Replace the placeholder in the EnglishPromptTemplate and strip any leading/trailing spaces
    modified_prompt = EnglishPromptTemplate.replace("${selection}", "{***}").strip()

    # Count the number of placeholders
    placeholder_count = modified_prompt.count("{***}")

    # Creating the "Inputs" section based on the number of placeholders
    inputs = [{"InputPlaceholder": "", "InputLabel": ""} for _ in range(placeholder_count)]

    # Creating a dictionary for JSON conversion with the specified structure
    json_dict = {
        "IsVisible": True,
        "Icon": "pen",
        "UsageDescription": "",
        "ChinesePromptTemplate": "",  # Assuming direct translation for example purposes
        "EnglishPromptTemplate": modified_prompt,
        "Inputs": inputs
    }

    # Converting the dictionary to a JSON string
    json_output = json.dumps(json_dict, ensure_ascii=False, indent=4)

    # Formatting the final output with the provided JSON string
    final_output = f"请修改prompt for GPT-4 json. 根据EnglishPromptTemplate字段合理填充其他所有字段。其中：\n" \
                   f"icon为bootstrap图标名称（例如\"pen\"， 请根据EnglishPromptTemplate修改为合理的内容，确保其在bootstrap中存在）\n" \
                   f"UsageDescription为此模版作用描述（例如\"按照文本撰写要求生成文本。\", 请根据EnglishPromptTemplate修改为合理的内容）\n" \
                   f"\"ChinesePromptTemplate\"为\"EnglishPromptTemplate\"的中文版本，请确保其与EnglishPromptTemplate完全对应\n" \
                   f"\"Inputs\"为对应于\"EnglishPromptTemplate\"的占位符（{{***}}）输入框的中文说明，其中的字典数量需与占位符数量相同。其中\"InputPlaceholder\"为\n" \
                   f"提示用户此处应该输入的内容，可以增加举例说明（如：请输入您的撰写文章类型（例如：科研文章、商业计划书、项目文档、小说）。 请根据EnglishPromptTemplate修改为合理的内容）；InputLabel为输入框的标签。要求用四字描述（如：文章类型， 请根据EnglishPromptTemplate修改为合理的内容）\n\n" \
                   f"json如下(###中)：\n" \
                   f"###\n" \
                   f"{json_output}\n" \
                   f"###"

    return final_output


if __name__ == '__main__':
    # Example usage of the function
    EnglishPromptTemplate = '''
Rewrite the text delimited by triple quotes and output it shorter to be no more than half the number of characters of the original text. Keep the meaning the same. Only give me the output and nothing else.Do not wrap responses in quotes.  Now, using the concepts above, re-write the following text. Respond in the same language variety or dialect of the following text: 
"""
${selection}
"""
    '''
    output = modify_json_template(EnglishPromptTemplate)
    print(output)
    pyperclip.copy(output)

