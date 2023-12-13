# -*- coding: utf-8 -*-
import os
import json
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


def create_config_page():
    """
    创建配置文件生成页面
    """
    field = 'config_file'
    # 一. 标题
    markdown_css(text='配置文件生成', align='center', font_size=35, bold=True)
    # 二. 用途说明
    st.markdown("#### 用途说明：用于生成配置文件")
    with st.expander(label='字段说明', expanded=False):
        # 应用设置好的markdown样式
        st.markdown(markdown_style(), unsafe_allow_html=True)
        st.markdown("""
            字段说明
            <div class="small-font">
                <div class="level-1"><b>IsVisible</b></div>
                    <div class="level-2">- 类型: 布尔值</div>
                    <div class="level-2">- 含义: 指示此功能是否应该对用户可见。</div>
                <div class="level-1"><b>Icon</b></div>
                    <div class="level-2">- 类型: 字符串</div>
                    <div class="level-2">- 含义: 定义图标，可从bootstrap官网中选择。官网链接为:<a href="https://icons.bootcss.com" target="_blank">bootstrap官网</a></div>
                <div class="level-1"><b>UsageDescription</b></div>
                    <div class="level-2">- 类型: 字符串</div>
                    <div class="level-2">- 含义: 描述该功能的用途。</div>
                <div class="level-1"><b>ChinesePromptTemplate</b></div>
                    <div class="level-2">- 类型: 字符串</div>
                    <div class="level-2">- 含义: 中文提示词模版。</div>
                <div class="level-1"><b>EnglishPromptTemplate</b></div>
                    <div class="level-2">- 类型: 字符串</div>
                    <div class="level-2">- 含义: 英文提示词模版。</div>
                <div class="level-1"><b>Inputs</b></div>
                    <div class="level-2">- 类型: 对象数组</div>
                    <div class="level-2">- 含义: 定义了用户输入的字段。每个对象包含以下子字段：</div>
                        <div class="level-3"><b>InputPlaceholder</b>: 输入框占位文本，提示用户应输入何种信息。</div>
                            <div class="level-4">- 类型: 字符串</div>
                            <div class="level-4">- 含义: 输入框占位文本，提示用户应输入何种信息。</div>
                        <div class="level-3"><b>InputLabel</b>: 输入框标签，说明该输入字段的内容。</div>
                            <div class="level-4">- 类型: 字符串</div>
                            <div class="level-4">- 含义: 输入框占位文本，提示用户应输入何种信息。</div>
            </div>
            """, unsafe_allow_html=True)

    # 使用 Streamlit 的分割线组件和布局功能来显示配置项的部分
    sac.divider(label='Config', icon='feather', align='center', bold=True)

    # 三. 配置项
    # 常规配置
    col1, col2 = st.columns([1, 10])
    with col1:
        sac.tags([sac.Tag(label='常规配置', color='black', bordered=False)], key='tag-0')
    with col2:
        df = pd.DataFrame(
            [
                {"IsVisible": True, "Icon": "", "UsageDescription": ""},
            ]
        )
        regular_configs = st.data_editor(df, num_rows="fixed", use_container_width=True)

    col1, col2 = st.columns([1, 10])
    with col1:
        sac.tags([sac.Tag(label='中文模版', color='black', bordered=False)], key='tag-1')
    with col2:
        # 定义一个回调函数，当输入文本框文字改变时更新 session_state
        def on_text_area_change():
            st.session_state[chinese_key] = st.session_state[chinese_key + "-input"]

        chinese_key = f"{field}-ChinesePromptTemplate"
        chinese_template = st.text_area(
            label="input",  # 提供非空的label值, 避免警告
            height=200,
            label_visibility="collapsed",
            placeholder=prompt_placeholder.replace('{language}', '中文'),
            key=chinese_key + "-input",  # 使用不同的 key
            value=st.session_state.get(chinese_key, ""),
            on_change = on_text_area_change  # 当文本框内容改变时调用函数
        )
        # 如果 session_state 中没有存储过当前文本框的值，则存储
        if chinese_key not in st.session_state:
            st.session_state[chinese_key] = chinese_template

    col1, col2 = st.columns([1, 10])
    with col1:
        sac.tags([sac.Tag(label='英文模版', color='black', bordered=False)], key='tag-2')
    with col2:
        def on_text_area_change():
            st.session_state[english_key] = st.session_state[english_key + "-input"]

        english_key = f"{field}-EnglishPromptTemplate"
        english_template = st.text_area(
            label="input",  # 提供非空的label值, 避免警告
            height=200,
            label_visibility="collapsed",
            placeholder=prompt_placeholder.replace('{language}', '英文'),
            key=english_key + "-input",  # 使用不同的 key
            value=st.session_state.get(english_key, ""),
            on_change = on_text_area_change  # 当文本框内容改变时调用函数
        )
        if english_key not in st.session_state:
            st.session_state[english_key] = english_template

    col1, col2 = st.columns([1, 10])
    with col1:
        sac.tags([sac.Tag(label='输入框项', color='black', bordered=False)], key='tag-3')
    with col2:
        df = pd.DataFrame(columns=["InputLabel", "InputPlaceholder"])
        inputs = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    col1, col2 = st.columns([1, 10])

    # 四. 结果显示
    sac.divider(label='JSON Result', icon='feather', align='center', bold=True)
    # 将输入框数据转换为符合 JSON 结构的格式
    inputs_json = [{"InputPlaceholder": row["InputPlaceholder"], "InputLabel": row["InputLabel"]} for index, row in
                   inputs.iterrows()]
    # 收集数据以构造 JSON
    json_data = {
        "IsVisible": bool(regular_configs.iloc[0]["IsVisible"]),
        "Icon": regular_configs.iloc[0]["Icon"],
        "UsageDescription": regular_configs.iloc[0]["UsageDescription"],
        "ChinesePromptTemplate": chinese_template,
        "EnglishPromptTemplate": english_template,
        "Inputs": inputs_json
    }
    # 将数据转换为 JSON 格式的字符串
    json_data = json.dumps(json_data, indent=2, ensure_ascii=False)
    # 显示json和下载按钮
    col1, col2 = st.columns([1, 10])
    with col1:
        # 创建下载按钮
        create_download_button(
            label="下载",
            data=json_data,
            file_name="config.json",
            mime="application/json"
        )
    with col2:
        # 显示json
        st.code(json_data)

    # 计算中文、英文占位符数量是否与输入项一致，如果不一致显示报错
    # 计算占位符的数量
    placeholders_chinese = chinese_template.count("{***}")
    placeholders_english = english_template.count("{***}")
    # 计算 inputs 中的字典个数
    num_inputs = len(inputs)
    # 检查数量是否匹配
    match_chinese = placeholders_chinese == num_inputs
    match_english = placeholders_english == num_inputs
    # 显示结果
    if not match_chinese or not match_english:
        st.error(
            f"占位符数量不匹配。中文模板占位符数: {placeholders_chinese}, 英文模板占位符数: {placeholders_english}, 输入项数: {num_inputs}。请确保占位符数量与输入项数一致。")
    else:
        st.success(
            f"占位符数量匹配。中文模板占位符数: {placeholders_chinese}, 英文模板占位符数: {placeholders_english}, 输入项数: {num_inputs}。")


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









