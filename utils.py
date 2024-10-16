import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import font_manager
import re
import Levenshtein

def get_edit_distance_score(expected_v, actual_v):
    edit_distance = Levenshtein.distance(expected_v, actual_v)

    if max(len(expected_v), len(actual_v)) > 0:
        edit_score = 1 - edit_distance / max(len(expected_v), len(actual_v))
    else:
        # 处理两个字符串长度都为零的情况
        edit_score = 1.0 if len(expected_v) == 0 and len(actual_v) == 0 else 0.0

    return edit_score
def check_custom_structure(s):
    pattern = r'!\[\S*?\]\(.+?\)'
    return bool(re.match(pattern, s))


def filter_model_text_array(text_array):
    filtered_array = [text for text in text_array if not check_custom_structure(text)]
    return filtered_array
def strQ2B(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring
def remove_special_chars(input_string):
    # Remove '*'
    result_string = input_string.replace('*', '')

    # Remove '\t' (tabs)
    result_string = result_string.replace('\t', '')

    # Remove spaces
    result_string = result_string.replace(' ', '')

    # Change
    result_string = strQ2B(result_string)

    result_string = re.sub(r'!\[]\(http.*?\.[pj]ng.*?\)', '', result_string)

    result_string = re.sub(r'\xa0', '', result_string)

    result_string = re.sub(r'■', '☑', result_string)

    result_string = re.sub(r'\$\\square\$', '□', result_string)

    result_string = re.sub(r'\$(\d+)\\(%)\$', lambda x: x.group(1) + x.group(2), result_string)

    result_string = re.sub(r'(R)(不?适用)', lambda x: '☑' + x.group(2), result_string)
    result_string = re.sub(r'(R)([是否])', lambda x: '☑' + x.group(2), result_string)
    result_string = re.sub(r'\xa0', '', result_string)
    result_string = re.sub(r'\xa0', '', result_string)
    result_string = re.sub(r'\ufeff', '', result_string)

    return result_string

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
            ax.text(angle, value, '{:.1%}'.format(value), ha='center', va='center', fontsize=10, alpha=0.7)

    # 设置标签
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.spines['polar'].set_visible(False)  # 隐藏最外圈的圆
    ax.grid(False)
    for j in np.arange(0, 1.2, 0.2):
        ax.plot(angles, len(values) * [j], '-.', lw=0.5, color='black', alpha=0.5)
    for j in range(len(values)):
        ax.plot([angles[j], angles[j]], [0, 1], '-.', lw=0.5, color='black', alpha=0.5)

    # 添加标题和图例
    # plt.title(title, size=20, color='black', y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # 选择支持中文字符的字体
    font_dirs = ["fonts"]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    ax.tick_params(pad=30)
    ax.set_theta_zero_location('N')
    # 保存图表到文件
    plt.savefig(filename)
    plt.show()
