from textin_tester.tester.table_evaluation.html_to_metric.metric import TEDS
from textin_tester.utils import *
default_html = "<html><body><table></table></body></html>"






class TextEval(object):
    def __init__(self):
        pass

    def __call__(self, raw_meta_json, raw_pred_json):
        return TextEval.compare_gt_and_pred(raw_meta_json, raw_pred_json)

    @staticmethod
    def make_pred_title_html(title_array):
        html_code = "<html><body><table>"  # 开始一个 div 元素，用于包裹所有标题

        for title in title_array:
            # 获取标题级别和标题内容
            level = 0
            try:
                while title.startswith('#'):
                    level += 1
                    title = title[1:].lstrip()
            except AttributeError:
                # 如果 title 不是字符串，遇到异常跳过当前 title
                continue

            title_content = title.strip()

            # 使用 f-string 构建 HTML 标签，去除前面的#以及到空格的部分
            html_code += f"<h{level}>{title_content}</h{level}>"

        html_code += "</table></body></html>"  # 结束 div 元素

        return html_code

    @staticmethod
    def extract_text_and_table_from_string(s):
        texts = s.split('\n\n')
        text_array = []
        title_array = []
        table_array = []
        formula_array = []
        for text in texts:
            text = text.strip()
            text = text.lstrip('\n')
            if text:  # Check if the stripped text is not empty
                if text.startswith('<table') and text.endswith('</table>'):
                    table_array.append(text)
                elif text.startswith('#') and '\n' not in text:
                    title_array.append(text)
                elif text.startswith('$') and text.endswith('$'):
                    formula_array.append(text)
                else:
                    text_array.append(text)
                    if '$' in text:
                        for formula in re.findall(r'\$(.*?)\$', text):
                            formula_array.append(formula)

        return text_array, title_array, table_array, formula_array

    @staticmethod
    def compute_score_and_recall(pred_arr, gt_arr, symbol):
        threshold = 0.8
        if symbol != '$':
            pred_arr = [pred.lstrip(symbol) for pred in pred_arr]
            gt_arr = [gt.lstrip(symbol) for gt in gt_arr]
        else:
            pred_arr = [pred.strip(symbol) for pred in pred_arr]
            gt_arr = [gt.strip(symbol) for gt in gt_arr]

        pred_arr = [remove_special_chars(pred) for pred in pred_arr]
        gt_arr = [remove_special_chars(gt) for gt in gt_arr]
        gt_arr_len = len(gt_arr)

        total_score = 0
        matched = 0

        for pred in pred_arr:
            cur_score = 0
            match_gt_text = None
            index_ = None
            for index, gt in enumerate(gt_arr):
                score = get_edit_distance_score(pred, gt)
                if score > threshold and score > cur_score:
                    cur_score = score
                    match_gt_text = gt
                    index_ = index

            if match_gt_text is not None:
                gt_arr.pop(index_)
                matched += 1

            total_score += cur_score

        match_num = matched
        total_recall = match_num / gt_arr_len if gt_arr_len > 0 else 0
        total_acc = match_num / len(pred_arr) if len(pred_arr) > 0 else 0
        f1 = 2 * total_acc * total_recall / (total_recall + total_acc) if (total_recall + total_acc) > 0 else 0
        return {f'total_score': total_score, 'recall_num': match_num, 'gt_num': gt_arr_len, 'pred_num': len(pred_arr),
                'f1': f1}

    @staticmethod
    def compare_gt_and_pred(raw_meta_json, raw_pred_json):
        # 获取文本内容 以\n\n分割
        eval_by_text_dict = {}
        model_text_array, title_array, table_array, formula_array = TextEval.extract_text_and_table_from_string(raw_pred_json)
        model_text_array = filter_model_text_array(model_text_array)

        gt_text_arr, gt_title_arr, gt_table_arr, gt_formula_arr = TextEval.extract_text_and_table_from_string(raw_meta_json)
        gt_text_arr = filter_model_text_array(gt_text_arr)

        # 计算段落分数
        text_score_dict = TextEval.compute_score_and_recall(model_text_array, gt_text_arr, '')

        # 计算标题分数
        title_score_dict = TextEval.compute_score_and_recall(title_array, gt_title_arr, '#')
        # 计算标题的树状编辑距离
        gt_res = TextEval.make_pred_title_html(gt_title_arr)
        pred_res = TextEval.make_pred_title_html(title_array)

        if gt_res == default_html and pred_res == default_html:
            teds_score = 0.0
        else:
            teds = TEDS()
            teds_score = teds.evaluate(pred_res, gt_res)

        formula_score_dict = TextEval.compute_score_and_recall(formula_array, gt_formula_arr, '$')

        status_dict = {'text': {}, 'title': {}, 'formula': {}}
        status_dict['text']['pred'] = text_score_dict['pred_num']
        status_dict['text']['gt'] = len(gt_text_arr)
        status_dict['title']['pred'] = title_score_dict['pred_num']
        status_dict['title']['gt'] = title_score_dict['gt_num']
        status_dict['formula']['pred'] = formula_score_dict['pred_num']
        status_dict['formula']['gt'] = formula_score_dict['gt_num']
        status_dict['formula']['gt_value'] = gt_formula_arr
        status_dict['formula']['pred_value'] = formula_array

        return text_score_dict['recall_num'], len(
            gt_text_arr), teds_score, title_score_dict, formula_score_dict, status_dict, text_score_dict['f1']
