import streamlit as st
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
        # st.markdown(icon_html, unsafe_allow_html=True)
        left_column, center_column, right_column = st.columns([0.1, 2.8, 0.1])
        with center_column:
            st.image(icon_dir)
        sac.divider(label='', align='center')