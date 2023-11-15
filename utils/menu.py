import os
import re
import json
import streamlit_antd_components as sac


def construct_menu_item_from_json(json_path, domain):
    """
    从JSON文件读取数据，并构建一个菜单项。
    """
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # 如果专家字典中 '是否显示' 键不存在或其值为 "否"，则不生成页面
    if not data.get('IsVisible', False):
        return False
    else:
        # 使用Domain字段作为label
        label = domain
        icon = data['Icon']
        # 返回一个没有子菜单的菜单项，因为这是最后一层
        return sac.MenuItem(label=label, icon=icon)


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


def get_menu_config(menu_dir, is_top_level=True):
    """
    得到侧边栏菜单配置，菜单目录构建方式如下：
    递归地列出目录中的子目录和文件，并为每个构建菜单项。
    如果目录包含子目录，则创建一个带有子菜单的菜单项；
    如果目录只包含文件，则每个文件对应一个菜单项。
    """
    menu_items = []
    for entry in sorted(os.listdir(menu_dir)):
        entry_path = os.path.join(menu_dir, entry)
        if os.path.isdir(entry_path):
            # 如果是目录，则递归构建子菜单
            children = get_menu_config(entry_path, is_top_level=False)
            folder = os.path.basename(entry_path)
            # 去除目录中前面的{数字.若干空格}。例如 "1. xxx"->"xxx"
            folder = remove_numerical_prefix(folder)
            # 目录如果包含图标，则解析，如果不包含，图标设置为None
            if '@' in folder:
                label, icon = folder.split('@')
            else:
                label = folder
                icon = None
            if children and is_top_level:
                # 只有在顶层并且有子菜单时才设置type为'group'
                menu_items.append(sac.MenuItem(label=label, icon=icon, type='group', children=children))
            else:
                # 其他情况不设置type
                if children:
                    menu_items.append(sac.MenuItem(label=label, icon=icon, children=children))
                else:
                    menu_items.append(sac.MenuItem(label=label, icon=icon))
        elif entry.endswith('.json'):
            # 如果是JSON文件，则构建一个菜单项
            domain = os.path.splitext(entry)[0]  # 移除.json扩展名获取Domain
            # 去除目录中前面的{数字.若干空格}。例如 "1. xxx"->"xxx"
            domain = remove_numerical_prefix(domain)
            result = construct_menu_item_from_json(entry_path, domain)
            if result:
                menu_items.append(result)

    return menu_items