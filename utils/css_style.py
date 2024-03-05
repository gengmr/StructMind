import streamlit as st
import streamlit.components.v1 as components
import json
import base64
import shutil
from pathlib import Path


def apple_style():
    # 苹果风格样式, 对st.text_area、st.code、st.button组件进行了样式的重调，增加边角圆润度和阴影效果，更改背景颜色。
    # 并去除st.text_area组件选中时显示红色边框效果
    style = """
        <style>
        /* Base styles for text area and code block */
        .stTextArea [data-baseweb=textarea], .stTextArea [data-baseweb=base-input] {
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
        
        .stCodeBlock* {
            background-color: #f1f3f4;
            padding: 10px 15px;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 16px;
        }

        /* Hover effect for input and code block */
        .stTextArea [data-baseweb=textarea]:hover, .stCodeBlock:hover {
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        .stButton>button {
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
        .stButton>button:hover {
            background-color: #F0F0F0;  /* 悬停时略微变暗 */
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
            text-decoration: none;  /* 悬停时也移除下划线 */
        }
        .stButton>button:focus, .stButton>button:active {
            color: #007AFF;  /* 保持原始字体颜色 */
            box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.2);
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


def highlight_code(text, language):
    file_path = 'config/img/logo.svg'
    with open(file_path, 'r') as file:
        svg_content = file.read()
    # HTML, CSS, and JavaScript for the custom display with syntax highlighting
    html = f"""
    <html>
    <head>
    <style>
        /* Custom styles */
        .code-container {{
            position: relative;
            border: none !important;
            border-radius: 15px;
            padding: 10px;
            margin-top: 0px;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 300px;
            background-color: #F0F0F0;
        }}
        .code-container:hover {{
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }}
        .code-container pre {{
            margin: 0;
            padding: 0;
            overflow: auto;
            height: 280px;
        }}
        .code {{
            padding: 10px;
            box-sizing: border-box;
        }}
        .copy-button {{
            position: absolute;
            top: 10px;
            right: 20px;
            cursor: pointer;
            background-color: transparent;
            border: none;
            outline: none;
        }}
        .copy-button img {{
            width: 30px;
            height: 30px;
            transition: transform 0.3s ease;
        }}
        .copy-button:hover img {{
            transform: scale(1.2);
        }}
        .copied-text {{
            position: absolute;
            top: 45px;
            right: 10px;
            color: green;
            font-size: 15px;
            display: none;
        }}

        /* Override highlight.js styles */
        .hljs {{
            background: transparent !important; /* Make background transparent */
            color: #333; /* Optional: Set text color */
        }}
    </style>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>
    <script>hljs.initHighlightingOnLoad();</script>
    </head>
    <body>

    <div class="code-container">
        <pre><code class="{language} code">{text}</code></pre>
        <button class="copy-button" onclick="copyCode()">
            <img src="data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}" alt="Copy">
        </button>
        <div id="copied-text" class="copied-text">Copied!</div>
    </div>

    <script>
    function copyCode() {{
        var copyText = document.querySelector('.code-container .code');
        navigator.clipboard.writeText(copyText.innerText);
        var copiedText = document.getElementById("copied-text");
        copiedText.style.display = 'block';
        setTimeout(function() {{ copiedText.style.display = 'none'; }}, 2000);
    }}
    </script>

    </body>
    </html>
    """

    components.html(html, height=330)


def sidebar_style():
    """
    设置streamlit侧边栏样式
    """
    # 创建一个多行字符串，其中包含CSS样式
    style = """
    <style>
        
    @media(hover: hover){
        /* 当设备支持悬停时，应用以下样式 */
        [data-testid='stSidebarUserContent'] iframe[title='streamlit_antd_components.utils.component_func.sac'] {
            width: 280px !important;  /* 侧边栏iframe宽度设置为 280px，使其悬停时不改变样式 */
        }

        /* 隐藏页面顶部的header部分 */
        header[data-testid="stHeader"] {
            display:none;
        }

        /* 设置侧边栏的基本样式 */
        section[data-testid='stSidebar'] {
            background-color: #f5f5f7; /* 苹果设计风格的浅灰色背景 */
            height: 100%; /* 高度设置为100% */
            min-width:30px !important; /* 最小宽度设置为30px */
            width: 30px !important; /* 宽度固定为30px */
            transform:translateX(0px); /* 位移变换设置为0 */
            position: relative; /* 相对定位 */
            z-index: 1; /* 层级为1 */
            top: 0; /* 顶部对齐 */
            left: 0; /* 左侧对齐 */
            overflow-x: hidden; /* 水平滚动条隐藏 */
            transition: 0.5s ease; /* 过渡效果，持续时间0.5秒 */
            padding-top: 60px; /* 顶部内边距为60px */
            white-space: nowrap; /* 不允许文本换行 */
        }

        /* 当鼠标悬停在侧边栏上时，改变其最小宽度 */
        section[data-testid='stSidebar']:hover{
            min-width: 330px !important; /* 最小宽度调整为330px */
        }

        /* 隐藏页眉和收起控件的按钮 */
        button[kind="header"], div[data-testid="collapsedControl"] {
            display: none;
        }
    }
    </style>
    """
    # 使用Streamlit的markdown方法来渲染这个样式字符串，并允许使用不安全的HTML
    st.markdown(style, unsafe_allow_html=True)




