import streamlit as st
import streamlit_antd_components as sac
from utils.sidebar import top_blank_set, icon_set
from utils.menu import get_menu_config


def set_page_style(page_title, layout, icon_dir, padding_top, menu_dir):
    """
    设置初始页面样式，
    """
    # 设置页面布局(宽屏模式 or 标准模式), 设置页面标题
    st.set_page_config(page_title=page_title, layout=layout)
    # 设置侧边栏上方空白变小（调整padding-top:30px）
    top_blank_set(padding_top=padding_top)
    # 设置侧边栏图标
    icon_set(icon_dir=icon_dir)
    # 设置侧边栏菜单
    with st.sidebar:
        menu_config = get_menu_config(menu_dir=menu_dir)
        selected_page = sac.menu(menu_config,
                                 format_func='title',
                                 size='small',
                                 indent=30,
                                 open_all=False
                                 )

    return selected_page
