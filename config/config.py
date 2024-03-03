import base64


# 菜单配置文件地址
MENU_DIR = 'config/菜单配置'
# 图标文件地址及内容
ICON_DIR = 'config/img/logo.png'
# 使用base64编译加载图标非常慢
with open(ICON_DIR, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
    ICON_CONTENT = "data:image/png;base64," + encoded_string
# 侧边栏上方空白大小
PADDING_TOP = 0
# 页面标题
PAGE_TITLE = "StructMind"
# 页面宽屏模式
LAYOUT = "wide"
# 配置文件生成页面中英文提示占位符
prompt_placeholder = """请输入{language}提示模版【占位符用"{***}"表示，且个数与输入框项个数相同】

以下仅做参考：
作为【输入角色】，您的任务是参考用户提供信息/要求完成【输入任务】。请按照以下步骤进行：
```
步骤1：
【步骤1】
步骤2：
【步骤2】
...
```

提供信息/要求如下:
```
【字段名称】：
{***}
【字段名称】：
{***}
...
```

注意事项：
```
【注意事项1】
【注意事项2】
```
"""
AUTHOR = "作者姓名"
INSTITUTE = "XX机构"
