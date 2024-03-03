# StructMind

## 概览
StructMind是一款基于Streamlit开发的大型语言模型（LLM）辅助软件，专注于提供系统化和科学化的LLM应用方法。它采用了多种原理和工具，包括提示工程（Prompt Engineering）、思维链（Chain-of-Thoughts）、思维树（Tree of Thoughts, ToT）等原理，以及头脑风暴、六顶思考帽、5为什么分析等思维工具。这些方法帮助用户有效解决LLM的常见问题，如幻觉、内存限制和不稳定的输出结果，从而提高LLM结果的质量并扩展其处理问题的能力。

StructMind包含多种模式，专为不同类型的任务设计，涵盖了简单的日常任务、规范的流程化任务、复杂的专业项目，以及开放式的创新任务。这种多模式的灵活性和适应性确保无论面对何种类型的任务，StructMind都能有效地提升工作效率和简便性。

## 主要功能
- **专家模式**: 提供各领域的高质量提示词模板，便于快速复制和使用，适用于简单的日常任务。
- **流程模式**: 提供序列化的高质量提示词模板，适用于规范的流程化任务。
- **分析模式**: 用于需求澄清、任务拆解、功能实现、文档生成，适用于专业的复杂项目。
- **探索模式**: 探索开放式任务的多种可能性，以拓展思路。适用于开放式任务。

## 安装与使用
要安装并运行 StructMind，请按照以下步骤操作：

1. 克隆代码仓库到您的本地机器：
   ```
   git clone [仓库URL]
   ```
2. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

3. 启动应用程序，请运行：

   ```
   streamlit run app.py
   ```

按照屏幕上的指示操作，浏览不同页面和功能。

## 文件结构和功能描述
- `app.py`: 应用程序的入口点，负责初始化页面样式和处理页面配置。它设置页面标题、布局、侧边栏图标等，并根据用户的菜单选择生成相应的页面。
- `get_json_prompt.py`: 包含 `print_json_contents` 函数，用于读取 JSON 文件并按照模板打印其内容。此脚本用于处理和格式化 JSON 数据，特别是用于专家级提示。

### utils 目录
- `init.py`: 包含 `set_page_style` 函数，用于设置初始页面样式。它负责页面布局、标题、侧边栏样式等的初始化设置。
- `menu.py`: 提供动态菜单生成功能。包含 `construct_menu_item_from_json`、`remove_numerical_prefix`、`get_menu_config` 等函数，用于构建和管理应用程序中的菜单项。
- `page.py`: 负责页面内容的生成和显示。包含 `create_input_section`、`get_page_config`、`create_page` 等函数，用于创建输入部分、获取页面配置和生成页面内容。
- `sidebar.py`: 包含 `top_blank_set` 和 `icon_set` 函数，用于调整侧边栏的样式和图标显示。
- `css_style.py`: 提供样式自定义功能。包含 `apple_input_style` 和 `markdown_css` 函数，用于自定义输入框和文本显示的样式。


