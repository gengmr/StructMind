# -*- coding: utf-8 -*-
from utils.init import set_page_style
from config.config import PAGE_TITLE, LAYOUT, ICON_DIR, MENU_DIR, PADDING_TOP
from utils.page import get_page_config, create_page, create_home_page, create_config_page, create_ppt
from utils.css_style import apple_style, sidebar_style


def main():
    # 设置初始页面样式
    selected_page = setup_initial_page_style()

    # 设置组件样式
    apple_style()
    sidebar_style()

    # 获取所有页面配置信息
    page_config = get_page_config(MENU_DIR)

    # 根据选择的菜单生成对应的页面
    generate_selected_page(selected_page, page_config)


def setup_initial_page_style():
    """
    设置初始页面样式，包括标题、布局、图标等。
    返回选定的页面。
    """
    return set_page_style(
        page_title=PAGE_TITLE,
        layout=LAYOUT,
        icon_dir=ICON_DIR,
        padding_top=PADDING_TOP,
        menu_dir=MENU_DIR
    )


def generate_selected_page(selected_page, page_config):
    """
    根据用户选择生成相应的页面。
    """
    if selected_page == '主页':
        create_home_page()
    elif selected_page == '配置文件生成':
        create_config_page()
    elif selected_page == '幻灯片制作':
        create_ppt(page_config=page_config[selected_page], domain=selected_page)
    elif selected_page in page_config:
        create_page(page_config=page_config[selected_page], domain=selected_page)


if __name__ == "__main__":
    main()
