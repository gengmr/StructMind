from utils.init import set_page_style
from config.config import PAGE_TITLE, LAYOUT, ICON_DIR, MENU_DIR, PADDING_TOP
from utils.page import get_page_config, create_page, create_config_page, create_home_page


# 设置初始页面样式, 包括页面标题、宽屏模式、侧边栏图像、侧边栏上方空白大小、侧边栏菜单
selected_page = set_page_style(
    page_title=PAGE_TITLE,
    layout=LAYOUT,
    icon_dir=ICON_DIR,
    padding_top=PADDING_TOP,
    menu_dir=MENU_DIR
)
# 得到所有页面配置信息，并根据选择的菜单生成对应的页面
page_config = get_page_config(menu_dir=MENU_DIR)
# 因为页面的domain进行了去除数字的格式化，并且将label和icon分开。因此不符合原文件的文件名，需要找到包含的文件
if selected_page == '主页':
    create_home_page()
if selected_page == '配置文件生成':
    create_config_page()
if selected_page in page_config.keys():
    create_page(page_config=page_config[selected_page], domain=selected_page)







