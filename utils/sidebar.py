import streamlit as st
import base64
import streamlit_antd_components as sac


def top_blank_set(padding_top=30):
    """
    设置侧边栏上方的空白大小。

    :param padding_top: 上方空白的大小（默认为30px）
    """
    st.markdown(f'''
        <style>
        .stApp [data-testid='stSidebar']>div:nth-child(1)>div:nth-child(2){{
            padding-top:{padding_top}px;
        }}
        </style>
        ''', unsafe_allow_html=True)


def icon_set(icon_dir):
    # 在侧边栏中显示图标
    with st.sidebar:
        # 将图片文件转换为 Base64 编码
        def get_image_as_base64(path):
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            return "data:image/png;base64," + encoded_string

        # 获取图片的 Base64 编码
        image_base64 = get_image_as_base64(icon_dir)

        # 构建带有 Base64 编码的图片的 HTML 代码
        image_html = f"""
            <style>
                .custom-img {{
                    width: 200px; /* 设置固定宽度 */
                    height: auto; /* 高度自动调整以保持纵横比 */
                    display: block; /* 使图像成为块级元素 */
                    margin-left: 40px; /* 设置左边距 */
                }}
            </style>
            <img src="{image_base64}" class="custom-img">
        """

        # 使用 st.markdown 显示图片
        st.markdown(image_html, unsafe_allow_html=True)
        sac.divider(label='', align='center')