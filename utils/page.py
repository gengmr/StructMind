import os
import json
import streamlit as st
import streamlit_antd_components as sac
from utils.css_style import markdown_css
from utils.menu import remove_numerical_prefix


def create_input_section(placeholder, placeholder_tag, idx, field):
    col1, col2 = st.columns([1, 10])
    with col1:
        sac.tags([sac.Tag(label=placeholder_tag, color='black', bordered=False)])
    with col2:
        key = f"{field}-{idx}"
        input_value = st.text_area(
            label="input",  # 提供非空的label值, 避免警告
            height=0,
            label_visibility="collapsed",
            placeholder=placeholder,
            value=st.session_state.get(key, "")
        )
        st.session_state[key] = input_value
        return input_value


def get_page_config(menu_dir):
    """
    获取页面需要的配置
    遍历菜单目录下所有JSON文件，将它们读取为字典，并返回一个字典，
    其中键为JSON文件名（不包含后缀和路径），值为JSON文件内容。

    如果发现重名的文件名，将抛出异常并显示重名文件的路径。

    :param menu_dir: 菜单配置文件目录。
    :return: 一个字典，键为文件名，值为JSON文件内容。
    """
    page_config = {}
    duplicates = {}

    for root, dirs, files in os.walk(menu_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]
                format_file_name = remove_numerical_prefix(file_name)

                # 检查是否有重名文件
                if format_file_name not in duplicates:
                    duplicates[format_file_name] = [file_path]
                else:
                    duplicates[format_file_name].append(file_path)

                # 读取JSON文件内容
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    page_config[format_file_name] = json.load(json_file)

    for format_file_name, paths in duplicates.items():
        if len(paths) > 1: # 如果有多个文件
            # 创建一个包含所有重名文件路径的错误消息
            error_message = "发现重名的JSON文件。请重命名以下文件:\n"
            for path in paths:
                error_message += f"-{path}\n"
            raise ValueError(error_message)

    return page_config


def create_page(page_config: dict, domain: str):
    """
    生成页面
    :param page_config: 包含页面信息的字典。
    :param domain: 领域
    """

    # 获取专家的领域和用途说明
    usage_description = page_config['UsageDescription']

    # 使用 markdown_css 函数以居中、加粗、35号字体显示专家的应用领域
    markdown_css(text=domain, align='center', font_size=35, bold=True)

    # 使用 Streamlit 的 markdown 函数显示用途说明
    st.markdown(f"#### 用途说明：\n\n{usage_description}")

    # 利用列表推导创建输入框部分，每个输入框都是通过 create_input_section 函数生成
    input_values = [
        create_input_section(input['InputPlaceholder'], input['InputLabel'], idx, domain)
        for idx, input in enumerate(page_config['Inputs'])
    ]

    # 使用 Streamlit 的分割线组件和布局功能来显示 prompt 结果的部分
    sac.divider(label='Prompt', icon='feather', align='center', bold=True)
    col1, col2 = st.columns([1, 10])

    # 创建标签列
    with col1:
        sac.tags([sac.Tag(label='生成结果', color='orange', bordered=False)])

    # 创建代码显示列
    with col2:
        # 格式化 prompt 模版，将 "{***}" 占位符替换成实际的输入值
        formatted_code = page_config["PromptTemplate"]
        for value in input_values:
            formatted_code = formatted_code.replace("{***}", value, 1)

        # 使用 Streamlit 的 code 函数显示格式化后的代码
        st.code(formatted_code)



