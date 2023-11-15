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
    Display text with custom font size, optional font family, color, alignment, and boldness using Streamlit's markdown.

    Parameters:
    - text (str): The text to be displayed.
    - font_size (int): The size of the font in pixels. Default is 16.
    - font (str, optional): The font family of the text. If None, the browser's default font is used. Default is None.
    - color (str): The color of the text. It can be a named color or hex code. Default is "black".
    - align (str): The alignment of the text. It can be "left", "center", or "right". Default is "left".
    - bold (bool): If True, the text will be bold. Default is False.

    Returns:
    None
    """

    # Create a unique key for the CSS style to avoid conflicts with other markdown styles
    unique_key = hash((text, font_size, font, color, align, bold))

    # Start the style definition
    style = f"<style>\n.markdown-css-{unique_key} {{\n"

    # Add font-family if font is specified
    if font is not None:
        style += f"    font-family: {font};\n"

    # Add font-size, color, alignment, and boldness
    style += f"    font-size: {font_size}px;\n"
    style += f"    color: {color};\n"
    style += f"    text-align: {align};\n"

    # Set font-weight to bold if bold is True
    if bold:
        style += "    font-weight: bold;\n"

    style += "}</style>\n"

    # Combine the style and the text
    markdown_text = style + f'<div class="markdown-css-{unique_key}">{text}</div>'

    # Display the styled text using Streamlit's markdown
    st.markdown(markdown_text, unsafe_allow_html=True)


def markdown_style():
    """
    返回Markdown样式的字符串。
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



