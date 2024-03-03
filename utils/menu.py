# -*- coding: utf-8 -*-
import os
import re
import json
import streamlit_antd_components as sac


def remove_numerical_prefix(path):
    """
    去除目录中的序号
    正则表达式匹配 "{数字}." 开头，后面跟一个或多个空格的模式.
    :param text:
    :return:
    """
    pattern = r'^\d+\.\s+'
    # 使用 re.sub() 函数替换匹配到的内容为空字符串
    format_path = re.sub(pattern, '', path)

    return format_path


def construct_menu_item_from_json(json_path, domain):
    """
    从JSON文件读取数据，并构建一个菜单项。
    """
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # 如果专家字典中 '是否显示' 键不存在或其值为 "否"，则不生成页面
    if not data.get('IsVisible', False):
        return False
    # 构建并返回菜单项
    label = domain
    icon = data['Icon']
    return sac.MenuItem(label=label, icon=icon)


def get_menu_config(menu_dir, is_top_level=True):
    """
    递归遍历指定目录，生成侧边栏菜单配置。
    此函数针对目录结构中的每个文件夹和JSON文件，创建相应的菜单项。
    对于文件夹，它将进一步递归遍历其子目录；对于JSON文件，它将调用函数创建菜单项。

    参数:
    menu_dir: 字符串，指定菜单配置的根目录路径。
    is_top_level: 布尔值，标识当前处理的目录是否为最顶层目录。默认为True。

    返回:
    菜单项列表，每个菜单项对应目录中的一个子目录或JSON文件。

    流程说明:
    1. 遍历指定目录中的每个条目（文件或文件夹）。
    2. 对于每个条目，检查它是文件夹还是JSON文件，并进行相应处理。
    3. 对于文件夹，递归调用此函数生成子菜单。
    4. 对于JSON文件，调用 `construct_menu_item_from_json` 函数创建菜单项。
    5. 根据条目的类型（文件夹或JSON文件）以及是否顶层目录，构建并添加菜单项到列表中。
    """
    menu_items = []

    for entry in sorted(os.listdir(menu_dir)):
        entry_path = os.path.join(menu_dir, entry)

        if os.path.isdir(entry_path):
            # 当前条目是目录，递归构建其子菜单
            children = get_menu_config(entry_path, is_top_level=False)
            folder = os.path.basename(entry_path)
            folder = remove_numerical_prefix(folder)

            # 解析目录名，分离出标签和图标
            if '@' in folder:
                label, icon = folder.split('@')
            else:
                label, icon = folder, None

            # 构建菜单项，顶层目录和子目录的处理有所不同
            if children and is_top_level:
                # 顶层目录，含子菜单，类型设为 'group'
                menu_items.append(sac.MenuItem(label=label, icon=icon, type='group', children=children))
            elif children:
                # 非顶层目录，含子菜单，不指定类型
                menu_items.append(sac.MenuItem(label=label, icon=icon, children=children))
            else:
                # 非顶层目录，不含子菜单，只添加目录本身
                menu_items.append(sac.MenuItem(label=label, icon=icon))
        elif entry.endswith('.json'):
            # 当前条目是JSON文件，构建单个菜单项
            domain = os.path.splitext(entry)[0]
            domain = remove_numerical_prefix(domain)
            result = construct_menu_item_from_json(entry_path, domain)
            if result:
                # 如果构建成功，将菜单项添加到列表中
                menu_items.append(result)

    return menu_items

