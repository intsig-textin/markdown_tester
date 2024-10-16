from textin_tester.tester.table_evaluation.md_to_metric.md_metric import MdTester
from textin_tester.tester.text_evaluation.text_evaluation import TextEval
from textin_tester.tester.order_evaluation.order_evaluation import OrderEval
from textin_tester.tester.table_converter.converter import TableConverter
import statistics


class TestFunction:

    def __init__(self):
        self.converter = TableConverter()
        self.md_tester = MdTester()
        self.text_eval = TextEval()
        self.order_eval = OrderEval()

    def run_compute_metric(self, sample_gt, pred_input):
        table_num, table_text_score, table_teds_score, table_struct_score = self.md_tester(sample_gt, pred_input)
        total_match_count, gt_len, title_score, title_score_dict, formula_score_dict, status_dict, text_f1 = self.text_eval(sample_gt, pred_input)
        order_res = self.order_eval(sample_gt, pred_input)

        body = {
            '平均表格文本全对率': statistics.mean(table_text_score) if table_num > 0 else None,
            '平均表格树状编辑距离': statistics.mean(table_teds_score) if table_num > 0 else None,
            '平均表格结构树状编辑距离': statistics.mean(table_struct_score) if table_num > 0 else None,

            '平均段落识别率': total_match_count / status_dict['text']['pred'] if status_dict['text']['pred'] > 0 else None,
            '段落召回率': total_match_count / gt_len if gt_len > 0 else None,
            '段落f1': text_f1 if gt_len > 0 else None,

            '平均标题识别率': title_score_dict['recall_num'] / title_score_dict['pred_num'] if title_score_dict['pred_num'] > 0 else None,
            '标题召回率': title_score_dict['recall_num'] / title_score_dict['gt_num'] if title_score_dict['gt_num'] > 0 else None,
            '标题f1': title_score_dict['f1'] if title_score_dict['gt_num'] > 0 else None,
            '平均标题树状编辑距离': title_score if title_score_dict['gt_num'] > 0 else None,

            '平均公式识别率': formula_score_dict['recall_num'] / formula_score_dict['pred_num'] if formula_score_dict['pred_num'] > 0 else None,
            '公式召回率': formula_score_dict['recall_num'] / formula_score_dict['gt_num'] if formula_score_dict['gt_num'] > 0 else None,
            '公式f1': formula_score_dict['f1'] if formula_score_dict['gt_num'] > 0 else None,

            '平均阅读顺序指标': order_res['order_score']
        }

        return body

    def __call__(self, raw_meta_json, raw_pred_json):
        raw_meta_json = self.converter.convert_markdown_to_html(raw_meta_json)
        raw_pred_json = self.converter.convert_markdown_to_html(raw_pred_json)
        return self.run_compute_metric(raw_meta_json, raw_pred_json)
