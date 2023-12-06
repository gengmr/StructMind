import json


def json_to_latex_beamer(json_data, author):
    """
    根据提供的JSON数据生成LaTeX Beamer演示文稿代码。

    :param json_data: 包含演示文稿结构的JSON数据。
    :param author: Beamer作者
    :return: 生成的LaTeX Beamer代码。
    """

    # 确保必要的键存在
    if 'title' not in json_data or 'subtitle' not in json_data:
        raise ValueError("JSON数据缺少必要的'title'或'subtitle'键")

    # 设置文档类和一些基本配置
    latex_code = "\\documentclass[11pt,notheorems,hyperref={pdfauthor=whatever}]{beamer}\n\n"
    latex_code += "% 导入演示文稿的设置\n\\input{loadslides.tex}\n\n"

    # 设置文档的标题、副标题和作者信息
    latex_code += "% 设置文档的标题、副标题、作者、日期信息"
    latex_code += "\\title{%(title)s}\n" % json_data
    latex_code += "\\subtitle{%(subtitle)s}\n" % json_data
    latex_code += f"\\author{{{author}}}\n"
    latex_code += "\\date{\\today}\n"
    latex_code += "\\begin{document}\n"
    latex_code += "\n% 生成标题页\n\maketitleframe\n% 生成目录页\n\maketocframe\n\n"

    # 遍历各个章节
    for section_idx, section in enumerate(json_data["sections"]):
        latex_code += f"% section {section_idx+1}\n"
        latex_code += "\\section{%s}\n" % section["title"]

        # 遍历每个小节
        for subsection_idx, subsection in enumerate(section.get("subsections", [])):
            latex_code += f"% subsection {section_idx+1}-{subsection_idx+1}\n"
            latex_code += "\\subsection{%s}\n" % subsection["title"]

            # 遍历每个帧
            for frame_idx, frame in enumerate(subsection.get("frames", [])):
                latex_code += f"% frame {section_idx+1}-{subsection_idx+1}-{frame_idx+1}\n"
                latex_code += "\\begin{frame}\n"

                # 遍历帧中的每个内容
                for content in frame.get("contents", []):
                    if content["type"] == "text":
                        latex_code += content["data"] + "\n"
                    elif content["type"] == "list":
                        latex_code += "\\begin{itemize}\n"
                        for item in content["items"]:
                            latex_code += "\t\\item {}\n".format(item)
                        latex_code += "\\end{itemize}\n"
                    elif content["type"] == "grouped_list":
                        latex_code += "\\begin{itemize}\n"
                        for item in content["dict"]:
                            latex_code += "\t\\item {}\n".format(item)
                            if content["dict"][item] != []:
                                latex_code += "\\begin{itemize}\n"
                                for subitem in content["dict"][item]:
                                    latex_code += "\t\t\\item {}\n".format(subitem)
                                latex_code += "\\end{itemize}\n"
                        latex_code += "\\end{itemize}\n"

                    elif content["type"] == "table":
                        # 设置表格的额外行高和列格式
                        latex_code += "\\setlength\\extrarowheight{3pt}\n"
                        # 生成列格式字符串，例如对于两列，结果应为 "|l|l|"
                        column_format = "|" + "|".join(["l" for _ in content["columns"]]) + "|"
                        # 使用格式化字符串
                        latex_code += "\\begin{tabular}{" + column_format + "}\n"
                        latex_code += "\\hline\n"
                        # 添加行颜色和列标题
                        latex_code += "\\rowcolor{primary}\\color{white}" + " & \\color{white}".join(
                            content["columns"]) + " \\\\\\hline\n"

                        # 添加表格内容
                        for row in content["rows"]:
                            latex_code += " & ".join(row) + " \\\\\n"
                            latex_code += "\\hline\n"  # 每行后添加横线

                        latex_code += "\\end{tabular}\n"

                latex_code += "\\end{frame}\n\n"

    # 添加结束幻灯片
    if json_data.get("thanks", False):
        latex_code += "\\section{}\n"
        latex_code += "\\begin{frame}\n"
        latex_code += "\\Huge{\\centerline{Thank you!}}\n"
        latex_code += "\\end{frame}\n"

    # 结束文档
    latex_code += "\\end{document}\n"

    return latex_code


if __name__ == '__main__':
    with open('../test.json', 'r', encoding='utf8') as fcc_file:
        author = '张三'
        data = json.load(fcc_file)
        latex_code = json_to_latex_beamer(data, author=author)
        print(latex_code)