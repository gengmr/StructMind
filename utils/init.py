import os
import streamlit as st
import streamlit_antd_components as sac
from utils.sidebar import top_blank_set, icon_set
from utils.menu import get_menu_config


def set_page_style(page_title, layout, icon_dir, padding_top, menu_dir):
    """
    设置初始页面样式。

    参数:
    - page_title (str): 页面标题。
    - layout (str): 页面布局，可选值为 'wide' 或 'centered'。
    - icon_dir (str): 侧边栏图标的目录路径。
    - padding_top (int): 侧边栏上方的填充大小。
    - menu_dir (str): 菜单配置的目录路径。

    返回:
    - selected_page (str): 用户从侧边栏选择的页面名称。
    """
    # 参数验证
    if layout not in ['wide', 'centered']:
        raise ValueError("无效的布局参数。可接受的值为 'wide' 或 'centered'。")

    if not os.path.exists(icon_dir):
        raise FileNotFoundError(f"图标目录 '{icon_dir}' 不存在。")

    if not os.path.exists(menu_dir):
        raise FileNotFoundError(f"菜单目录 '{menu_dir}' 不存在。")

    # 设置页面布局和标题
    st.set_page_config(page_title=page_title, layout=layout)
    top_blank_set(padding_top=padding_top)
    # icon_set()  # 设置侧边栏图标

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


