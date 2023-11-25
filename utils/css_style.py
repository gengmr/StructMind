import streamlit as st
import json
import base64


def apple_input_style():
    # 苹果风格样式, 对st.text_area和st.code组件进行了样式的重调，增加边角圆润度和阴影效果，更改背景颜色。
    # 并去除st.text_area组件选中时显示红色边框效果
    style = """
        <style>
        /* Base styles for text area and code block */
        .stTextArea [data-baseweb=textarea], .stCodeBlock, .stTextArea [data-baseweb=base-input] {
            background-color: #f1f3f4;
            border: none !important;
            padding: 10px 15px;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 16px;
            outline: none !important;
        }

        /* Specific styles for text area and code block */
        .stTextArea [data-baseweb=textarea], .stCodeBlock {
            border-radius: 10px;  /* Rounded corners */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Differentiating st.code with a unique background color */
        .stCodeBlock {
            background-color: #e6e8e9;
        }

        /* Unify color for st.code children */
        .stCodeBlock * {
            background-color: #e6e8e9;
        }

        /* Hover effect for input and code block */
        .stTextArea [data-baseweb=textarea]:hover, .stCodeBlock:hover {
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }

        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


def markdown_css(text, font_size=16, font=None, color="black", align="left", bold=False):
    """
    使用Streamlit的markdown显示具有自定义字体大小、可选字体族、颜色、对齐方式和加粗的文本。

    参数:
    - text (str): 要显示的文本。
    - font_size (int): 字体大小（像素）。默认为16。
    - font (str, 可选): 文本的字体族。如果为None，则使用浏览器的默认字体。默认为None。
    - color (str): 文本的颜色。可以是命名颜色或十六进制代码。默认为"black"。
    - align (str): 文本的对齐方式。可以是"left"、"center"或"right"。默认为"left"。
    - bold (bool): 如果为True，则文本将加粗。默认为False。

    返回:
    无
    """

    # 创建唯一键以避免与其他markdown样式冲突
    unique_key = hash((text, font_size, font, color, align, bold))

    # 构建样式定义
    style_components = [
        f"font-family: {font};" if font else "",
        f"font-size: {font_size}px;",
        f"color: {color};",
        f"text-align: {align};",
        "font-weight: bold;" if bold else ""
    ]
    style = f"<style>\n.markdown-css-{unique_key} {{\n" + "\n".join(filter(None, style_components)) + "\n}}</style>\n"

    # 结合样式和文本
    markdown_text = style + f'<div class="markdown-css-{unique_key}">{text}</div>'

    # 使用Streamlit的markdown显示样式化文本
    st.markdown(markdown_text, unsafe_allow_html=True)


def markdown_style():
    """
    构造并返回一系列Markdown样式定义的字符串。

    此函数定义了几种特定的Markdown样式，可以被应用于Streamlit应用中的Markdown文本。
    定义的样式包括不同级别的文本缩进和颜色变化。

    返回:
    - str: 包含Markdown样式定义的字符串。
    """
    return """
    <style>
    .small-font {
        font-size: 15px;
        color: darkgray;
    }
    .level-1 {
        margin-left: 0px;
        color: #1B2430; /* 深空灰 */
    }
    .level-2 {
        margin-left: 20px;
        color: #C0C0C0; /* 银色 */
    }
    .level-3 {
        margin-left: 40px;
        color: #1B2430; /* 深空灰 */
    }
    .level-4 {
        margin-left: 60px;
        color: #C0C0C0; /* 银色 */
    }
    </style>
    """


def create_download_button(label, data, file_name, mime):
    """
    创建一个下载按钮，允许用户下载JSON格式的数据。

    参数:
    label (str): 按钮上显示的文本。
    data (dict): 要下载的数据，以字典格式提供。
    file_name (str): 下载文件的名称。
    mime (str): 文件的MIME类型，例如 'application/json'。
    """

    # 将数据转换为JSON字符串
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # 编码数据为Base64
    b64_data = base64.b64encode(json_data.encode()).decode()

    # 生成下载链接
    download_link = f"""
        <a download="{file_name}" href="data:{mime};base64,{b64_data}" class="apple-style-button">
            {label}
        </a>
    """

    # 设置按钮样式
    apple_style = """
        <style>
        .apple-style-button {
            background-color: #FFFFFF;  /* 白色背景 */
            color: #007AFF;  /* 蓝色字体，符合苹果设计 */
            border-radius: 15px;
            border: none;
            font-family: 'Helvetica Neue', sans-serif;  /* 使用苹果系统字体 */
            font-size: 16px;
            padding: 5px 15px;  /* 按钮的高度和宽度 */
            margin: 10px 0;
            box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s, box-shadow 0.3s;
            text-align: center;
            text-decoration: none;  /* 移除下划线 */
            display: inline-block;
            cursor: pointer;
        }
        .apple-style-button:hover {
            background-color: #F0F0F0;  /* 悬停时略微变暗 */
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
            text-decoration: none;  /* 悬停时也移除下划线 */
        }
        </style>
    """

    # 将样式和下载链接添加到Streamlit应用中
    st.markdown(apple_style, unsafe_allow_html=True)
    st.markdown(download_link, unsafe_allow_html=True)



