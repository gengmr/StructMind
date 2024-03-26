# -*- coding: utf-8 -*-
import os
import json
import re
import pandas as pd
import streamlit as st
import streamlit_antd_components as sac
from utils.css_style import markdown_css, markdown_style, create_download_button, highlight_code
from utils.menu import remove_numerical_prefix
from utils.latex import json_to_latex_beamer
from config.config import prompt_placeholder, PAGE_TITLE, AUTHOR, INSTITUTE


def create_input_section(input_placeholder, input_placeholder_tag, input_list, idx, field):
    custom_input = "自定义输入"
    col1, col2 = st.columns([1, 10])
    with col1:
        sac.tags([sac.Tag(label=input_placeholder_tag, color='black', bordered=False)])
    with col2:
        key = f"{field}-{idx}"

        # 定义文本区域内容变化时的回调函数
        def on_text_area_change():
            st.session_state[key + "-area"] = st.session_state[key + "-input"]

        # 定义下拉列表内容变化时的回调函数
        def on_select_area_change():
            st.session_state[key + "-selectbox"] = st.session_state[key + "-select"]

        # 只有当input_list不为空时，才创建下拉列表
        if input_list:
            options = [custom_input] + input_list

            selected_option = st.selectbox(
                label="xxx",  # 非空即可
                options=options,
                index=options.index(st.session_state.get(key + "-selectbox", custom_input)),
                key=key + "-select",
                on_change=on_select_area_change,
                label_visibility="collapsed"
            )

            # 当选择“自定义输入”时，显示文本区域供用户输入
            if selected_option == custom_input:
                input_value = st.text_area(
                    label="xxx",  # 非空即可
                    height=0,
                    label_visibility="collapsed",
                    placeholder=input_placeholder,
                    value=st.session_state.get(key + "-area", ""),  # 从 session_state 获取初始值
                    key=key + "-input",
                    on_change=on_text_area_change
                )
                return input_value
            else:
                return selected_option
        else:
            # input_list为空，直接使用文本输入
            input_value = st.text_area(
                label="input",
                height=0,
                label_visibility="collapsed",
                placeholder=input_placeholder,
                value=st.session_state.get(key + "-area", ""),  # 从 session_state 获取初始值
                key=key + "-input",
                on_change=on_text_area_change
            )
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


def custom_template_page(domain):
    """
    创建自定义模版页面
    :param domain: 领域
    """
    # 一. 标题
    markdown_css(text='自定义模版', align='center', font_size=35, bold=True)
    # 二. 用途说明
    st.markdown("#### 用途说明：使用自定义模版进行文本生成")
    # 模板文本，其中"{{...}}"表示占位符

    def custom_text_area_change():
        st.session_state[domain + "-area"] = st.session_state[domain + "-input"]

    prompt = st.text_area(
        "示例模版如下，请根据需求修改。占位符格式为：{{...}}",
        height=500,
        value=st.session_state.get(domain + "-area",
                                   "作为xx领域专家，请根据提供的【输入信息】，按照【执行原则】完成xx任务，"
                                   "并严格按照【返回格式】返回结果。确保结果的专业性、规范性、逻辑性，同时遵循行业的标准与最佳实践。\n\n"
                                   "【输入信息】\n"
                                   "{{输入信息}}\n\n"
                                   "【执行原则】\n"
                                   "{{执行原则}}\n\n"
                                   "【返回格式】\n"
                                   "{{返回格式}}"
                                   ),
        key=domain + "-input",  # 使用不同的 key
        on_change=custom_text_area_change  # 当文本框内容改变时调用函数
    )

    # 使用正则表达式找出所有的占位符
    placeholders = re.findall(r"\{\{(.+?)\}\}", prompt)

    # 为每个占位符生成一个输入框，将用户输入存储在一个列表中
    user_inputs = []
    for idx, placeholder in enumerate(placeholders):
        # 创建列以改善布局
        col1, col2 = st.columns([1, 10])

        with col1:
            # 使用占位符文本作为标签显示，增强用户体验
            sac.tags([sac.Tag(label=placeholder, color='black', bordered=False)])
        with col2:
            key = f"{domain}-{idx}"  # 格式化key以区分不同的输入框

            # 定义内容变化时的回调函数
            def on_text_area_change():
                st.session_state[key + "-area"] = st.session_state[key + "-input"]
            # 为每个占位符生成输入区域
            user_input = st.text_area(
                label="xxx",  # 非空即可
                height=200,
                label_visibility="collapsed",
                placeholder=f"请输入{placeholder}",
                value=st.session_state.get(key + "-area", ""),
                key=key + "-input",
                on_change=on_text_area_change
            )
            user_inputs.append(user_input)

    for placeholder, value in zip(placeholders, user_inputs):
        prompt = re.sub(rf"\{{\{{({placeholder})\}}\}}", value, prompt)

    # 使用自定义代码高亮组件显示
    highlight_code(prompt, language='python')


def create_home_page():
    """
    读取并显示README.md文件的内容在Streamlit主页上。
    """
    # 读取README.md文件的内容
    with open('README.md', 'r', encoding='utf-8') as file:
        readme_content = file.read()
        try:
            readme_content = readme_content.replace('# StructMind', '')
        except:
            pass

    # 在Streamlit主页上显示Markdown内容
    st.markdown(f"<h1 style='text-align: center;'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)
    st.markdown(readme_content)


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
        create_input_section(input['InputPlaceholder'], input['InputLabel'], input['InputList'], idx, domain)
        for idx, input in enumerate(page_config['Inputs'])
    ]

    # 使用 Streamlit 的分割线组件和布局功能来显示 prompt 结果的部分
    sac.divider(label='Prompt', icon='feather', align='center', bold=True)
    col1, col2 = st.columns([1, 10])

    # 创建标签列
    with col1:
        mode = sac.switch(label='英语模式', value=False, size='small')
        if mode:
            prompt = page_config["EnglishPromptTemplate"]
        else:
            prompt = page_config["ChinesePromptTemplate"]
        # 格式化 prompt 模版，将 "{***}" 占位符替换成实际的输入值
        for value in input_values:
            prompt = prompt.replace("{***}", str(value), 1)

    # 创建代码显示列
    with col2:
        # 使用自定义代码高亮组件显示
        highlight_code(prompt, language='python')


def create_ppt(page_config, domain):
    # json格式是否正确, json数据
    if 'json_flag' not in st.session_state:
        st.session_state['json_flag'] = False
    if 'json_data' not in st.session_state:
        st.session_state['json_data'] = ""

    tab = sac.steps(
        items=[
            sac.StepsItem(title='step 1', description='确定PPT主题及子主题'),
            sac.StepsItem(title='step 2', description='生成json'),
            sac.StepsItem(title='step 3', description='json格式检查'),
            sac.StepsItem(title='step 4', description='PPT生成'),
        ], format_func='title'
    )
    if tab == 'step 1':
        st.markdown('### 请利用`分析模式`的`需求澄清`和`框架搭建`功能明确`PPT的主题和子主题`\n步骤如下：\n1. 利用`分析模式`的`需求澄清`的`任务目标`'
                    '中填写`制作关于[此处填写PPT主题]`的PPT，得到`需求文档`\n2. 利用`分析模式`的`框架搭建`功能列出`PPT主题及子主题`')
    elif tab == 'step 2':
        create_page(page_config=page_config, domain=domain)
    elif tab == 'step 3':
        col1, col2 = st.columns([1, 10])

        with col1:
            sac.tags([sac.Tag(label="格式数据", color='black', bordered=False)])
        with col2:
            key = f"{domain}-json_input"
            # 定义文本区域内容变化时的回调函数

            def on_text_area_change():
                st.session_state[key + "-area"] = st.session_state[key + "-input"]

            input_data = st.text_area(
                label="input",  # 提供非空的label值, 避免警告
                height=200,
                label_visibility="collapsed",
                placeholder="请输入PPT的JSON数据",
                key=key + "-input",  # 使用不同的 key
                value=st.session_state.get(key + "-area", ""),
                on_change=on_text_area_change  # 当文本框内容改变时调用函数
            )

            try:
                # 尝试解析输入数据为JSON
                st.session_state['json_data'] = json.loads(input_data)

                # 检查解析结果是否为字典或列表
                if isinstance(st.session_state['json_data'], (dict, list)):
                    # 如果是字典或列表，显示成功信息和JSON数据
                    st.session_state['json_flag'] = True
                    st.success("数据符合JSON格式要求!")
                    st.markdown("### JSON数据如下:")
                    st.json(st.session_state['json_data'])
                else:
                    # 如果解析结果不是字典或列表，则不是有效的JSON
                    st.session_state['json_flag'] = False
                    st.error("数据不是有效的JSON格式!")

            except json.JSONDecodeError:
                st.session_state['json_flag'] = False
                # 如果解析过程中出现异常，表示数据不是JSON格式
                st.error("数据不是有效的JSON格式!")

    elif tab == 'step 4':
        if not st.session_state['json_flag']:
            st.error("请在步骤3中输入PPT的JSON数据!")
        else:
            highlight_code(json_to_latex_beamer(json_data=st.session_state['json_data'], author=AUTHOR, institute=INSTITUTE), language='python')









