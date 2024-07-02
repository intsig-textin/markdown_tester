import matplotlib.pyplot as plt
import numpy as np
import os
import re
import matplotlib.font_manager as fm
font = fm.FontProperties(fname=r'font/SimHei.ttf')


def print_aligned_dict(data):
    # 找到所有键的最长长度
    max_key_length = max(len(key) for key in data['testcase1'])

    # 打印表头
    print(f"{' ' * (max_key_length + 4)}", end="")
    for key in data:
        print(f"{key:>{max_key_length}}", end="")
    print()

    # 打印字典内容
    for subkey in data['testcase1']:
        print(f"{subkey:<{max_key_length + 4}}", end="")
        for key in data:
            print(f"{data[key][subkey]:>{max_key_length}}", end="")
        print()
def create_dict_from_folders(directory):
    body = {}
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        if os.path.isdir(folder_path):
            body[folder_name] = {}
    return body


def create_radar_chart(df, title, filename):
    labels = df.columns

    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    # 初始化雷达图
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True), dpi=200)
    # ax.spines['polar'].set_visible(False)

    # 绘制每个数据集的雷达图
    for index, row in df.iterrows():
        values = row.tolist()
        values += values[:1]
        ax.fill(angles, values, alpha=0.1)
        ax.plot(angles, values, label=index)

        # 在每个数据点旁边添加百分比标签
        for angle, value in zip(angles, values):
            ax.text(angle, value, '{:.1%}'.format(value), ha='center', va='center', fontsize=7, alpha=0.7)

    # 设置标签
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontproperties=font)
    ax.spines['polar'].set_visible(False)  # 隐藏最外圈的圆
    ax.grid(False)
    for j in np.arange(0, 1.2, 0.2):
        ax.plot(angles, len(values) * [j], '-.', lw=0.5, color='black', alpha=0.5)
    for j in range(len(values)):
        ax.plot([angles[j], angles[j]], [0, 1], '-.', lw=0.5, color='black', alpha=0.5)

    # 添加标题和图例
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    ax.tick_params(pad=30)
    ax.set_theta_zero_location('N')
    # 保存图表到文件
    plt.savefig(filename)


def markdown_to_html(markdown_table):
    rows = [row.strip() for row in markdown_table.strip().split('\n')]
    num_columns = len(rows[0].split('|')) - 2

    html_table = '<table>\n  <thead>\n    <tr>\n'

    header_cells = [cell.strip() for cell in rows[0].split('|')[1:-1]]
    for cell in header_cells:
        html_table += f'      <th>{cell}</th>\n'
    html_table += '    </tr>\n  </thead>\n  <tbody>\n'

    for row in rows[2:]:
        cells = [cell.strip() for cell in row.split('|')[1:-1]]
        html_table += '    <tr>\n'
        for cell in cells:
            html_table += f'      <td>{cell}</td>\n'
        html_table += '    </tr>\n'

    html_table += '  </tbody>\n</table>\n'
    return html_table
def convert_markdown_to_html(self, markdown_content, md_type):
    # Define a regex pattern to find Markdown tables with newlines
    markdown_content = markdown_content.replace('\r', '')
    pattern = re.compile(r'\|\s*.*?\s*\|\n', re.DOTALL)

    # Find all matches in the Markdown content
    matches = pattern.findall(markdown_content)
    for match in matches:
        html_table = markdown_to_html(match)
        markdown_content = markdown_content.replace(match, html_table, 1)  # Only replace the first occurrence
    res_html = convert_table(replace_table_with_placeholder(markdown_content))

    return res_html
def convert_table_str(s):
    s = re.sub(r'<table.*?>','<table>',s)
    s = re.sub(r'<th','<td',s)
    s = re.sub(r'</th>','</td>',s)
    # s = re.sub(r'<td rowspan="(.)">',lambda x:f'<td colspan="1" rowspan="{x.group(1)}">',s)
    # s = re.sub(r'<td colspan="(.)">',lambda x:f'<td colspan="{x.group(1)}" rowspan="1">',s)
    res = ''
    res += '\n\n'
    temp_item = ''
    for c in s:
        temp_item += c
        if c == '>' and not re.search(r'<td.*?>\$',temp_item):
            res += temp_item+'\n'
            temp_item = ''
    return res+'\n'
def merge_table(md):
    table_temp = ''
    for line in md:
        table_temp += line
    return convert_table_str(table_temp)
def find_md_table_mode(line):
    if re.search(r'-*?:',line) or re.search(r'---',line) or re.search(r':-*?',line):
        return True
    return False
def delete_table_and_body(input_list):
    res = []
    for line in input_list:
        if not re.search(r'</?t(able|head|body)>',line):
            res.append(line)
    return res
def merge_tables(input_str):
    # 删除HTML注释
    input_str = re.sub(r'<!--[\s\S]*?-->', '', input_str)

    # 使用正则表达式找到每个<table>块
    table_blocks = re.findall(r'<table>[\s\S]*?</table>', input_str)

    # 处理每个<table>块，将<th>替换为<td>
    output_lines = []
    for block in table_blocks:
        block_lines = block.split('\n')
        for i, line in enumerate(block_lines):
            if '<th>' in line:
                block_lines[i] = line.replace('<th>', '<td>').replace('</th>', '</td>')
        final_tr = delete_table_and_body(block_lines)
        if len(final_tr) > 2:
            output_lines.extend(final_tr)  # 忽略<table>和</table>标签，只保留表格内容

    # 将处理后的字符串重新连接
    merged_output = '<table>\n{}\n</table>'.format('\n'.join(output_lines))

    return "\n\n" + merged_output + "\n\n"
def replace_table_with_placeholder(input_string):
    lines = input_string.split('\n')
    output_lines = []

    in_table_block = False
    temp_block = ""
    last_line = ""

    org_table_list = []
    in_org_table = False

    i = 0
    for line in lines:
        if i == 334:
            #print(i)
            pass
        if not in_org_table:
            if "<table>" not in last_line and in_table_block == False and temp_block != "":
                output_lines.append(merge_tables(temp_block))
                temp_block = ""
            if "<table>" in line:
                if "<table><tr" in line:
                    org_table_list.append(line)
                    in_org_table = True
                    output_lines.append(last_line)
                    continue
                else:
                    in_table_block = True
                    temp_block += last_line
            elif in_table_block:
                if not find_md_table_mode(last_line) and "</thead>" not in last_line:
                    temp_block += "\n" + last_line
                if "</table>" in last_line:
                    if "<table>" not in line:
                        in_table_block = False
            else:
                output_lines.append(last_line)

            last_line = line
        else:
            org_table_list.append(line)
            if "</table" in line:
                in_org_table = False
                last_line = merge_table(org_table_list)
                org_table_list = []
        i += 1

    if "</table>" in last_line:
        output_lines.append(merge_tables(temp_block))

    return '\n'.join(output_lines)
def convert_table(input_str):
    # 替换<table>
    output_str = input_str.replace("<table>", "<table border=\"1\" >")

    # 替换<td>
    output_str = output_str.replace("<td>", "<td colspan=\"1\" rowspan=\"1\">")

    return output_str
def convert_markdown_to_html(markdown_content):
    # Define a regex pattern to find Markdown tables with newlines
    markdown_content = markdown_content.replace('\r', '')
    pattern = re.compile(r'\|\s*.*?\s*\|\n', re.DOTALL)

    # Find all matches in the Markdown content
    matches = pattern.findall(markdown_content)
    for match in matches:
        html_table = markdown_to_html(match)
        markdown_content = markdown_content.replace(match, html_table, 1)  # Only replace the first occurrence
    res_html = convert_table(replace_table_with_placeholder(markdown_content))

    return res_html