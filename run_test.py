from tester.table_evaluation.md_to_metric.md_metric import Md_Tester
from tester.text_evaluation.text_evaluation import TextEval
from tester.order_evaluation.order_evaluation import OrderEval
from tester.converter.converter import Converter
from tester.adapter.adapter import *
import os
import statistics
import pandas as pd
from utils import create_dict_from_folders, create_radar_chart, convert_markdown_to_html
import argparse
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.width', 200)  # 设置显示宽度
pd.set_option('display.max_columns', None)  # 确保所有列都显示

class TestFunction(object):

    def __init__(self):
        self.converter = Converter()

    def run_compute_metric(self, sample_gt, pred_input, run_type):
        pred_input = titleAdapter(pred_input)
        sample_gt = gtAdapter(sample_gt, run_type)
        table_num, text_score, teds_score, struct_score, child_index = Md_Tester()(sample_gt, pred_input)
        total_match_count, gt_len, title_score, title_score_dict, formula_score_dict, status_dict, text_f1 = TextEval()(
            sample_gt, pred_input, run_type)
        order_res = OrderEval()(sample_gt, pred_input)

        body = {'平均表格文本全对率': statistics.mean(text_score) if table_num > 0 else None,
                '平均表格树状编辑距离': statistics.mean(teds_score) if table_num > 0 else None,
                '平均表格结构树状编辑距离': statistics.mean(struct_score) if table_num > 0 else None,
                '平均段落识别率': total_match_count / status_dict['text']['pred'] if
                status_dict['text']['pred'] > 0 else None,
                '段落召回率': total_match_count / gt_len if gt_len > 0 else None,
                '段落f1': text_f1 if gt_len > 0 else None,
                '平均标题识别率': title_score_dict['recall_num'] / title_score_dict['pred_num'] if
                title_score_dict['pred_num'] > 0 else None,
                '标题召回率': title_score_dict['recall_num'] / title_score_dict['gt_num'] if
                title_score_dict['gt_num'] > 0 else None,
                '标题f1': title_score_dict['f1'] if title_score_dict['gt_num'] > 0 else None,
                '平均标题树状编辑距离': title_score if title_score_dict['gt_num'] > 0 else None,
                '平均公式识别率': formula_score_dict['recall_num'] / formula_score_dict['pred_num'] if
                formula_score_dict['pred_num'] > 0 else None,
                '公式召回率': formula_score_dict['recall_num'] / formula_score_dict['gt_num'] if
                formula_score_dict['gt_num'] > 0 else None,
                '公式f1': formula_score_dict['f1'] if formula_score_dict['gt_num'] > 0 else None,
                '平均阅读顺序指标': order_res['order_score']}
        return body

    def __call__(self, raw_meta_json, raw_pred_json):
        raw_meta_json = Converter().convert_markdown_to_html(raw_meta_json)
        raw_pred_json = Converter().convert_markdown_to_html(raw_pred_json)
        new_body = self.run_compute_metric(raw_meta_json, raw_pred_json, "pred")

        return new_body


def main():
    parser = argparse.ArgumentParser(description="请输入文件路径")
    parser.add_argument('--pred_path', type=str, default='dataset/pred', help='预测值文件')
    parser.add_argument('--gt_path', type=str, default='dataset/gt', help='真值文件')
    parser.add_argument('--out', type=str, default='output', help='评测结果存放目录')
    args = parser.parse_args()

    total = create_dict_from_folders(args.pred_path)
    for total_key in total:
        current = {
            '平均表格文本全对率': [],
            '平均表格树状编辑距离': [],
            '平均表格结构树状编辑距离': [],
            '平均段落识别率': [],
            '段落召回率': [],
            '段落f1': [],
            '平均标题识别率': [],
            '标题召回率': [],
            '标题f1': [],
            '平均标题树状编辑距离': [],
            '平均公式识别率': [],
            '公式召回率': [],
            '公式f1': [],
            '平均阅读顺序指标': []
        }

        folder_a_path = args.gt_path
        folder_b_path = f"{args.pred_path}/{total_key}"
        folder_a_files = os.listdir(folder_a_path)
        folder_b_files = os.listdir(folder_b_path)
        for file_a in folder_a_files:
            file_a_name = file_a.split(".")[0]
            for file_b in folder_b_files:
                file_b_name = file_b.split(".")[0]
                if file_a_name == file_b_name:
                    with open(folder_a_path + '/' + file_a, 'r', encoding='utf-8') as infile:
                        gt_markdown_content = infile.read()
                    with open(folder_b_path + '/' + file_a, 'r', encoding='utf-8') as infile:
                        pred_markdown_content = infile.read()
                    body = TestFunction()(convert_markdown_to_html(gt_markdown_content),
                                          convert_markdown_to_html(pred_markdown_content))
                    for key, value in body.items():
                        if value is not None:
                            current[key].append(value)
        for key, value in current.items():
            if value:
                current[key] = statistics.mean(value)
            else:
                current[key] = 0
        total[total_key] = current

    df = pd.DataFrame(total)
    print(df.to_string())
    if not os.path.exists(args.out):
        os.makedirs(args.out)
    create_radar_chart(df.transpose(), 'performance test results', os.path.join(args.out, 'performance_test_results.png'))
    df.to_excel(os.path.join(args.out, 'performance_test_results.xlsx'), index=True)


if __name__ == "__main__":
    main()
