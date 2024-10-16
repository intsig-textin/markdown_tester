import os
import html
import unicodedata
import sys
import re
from textin_tester.tester.table_evaluation.html_to_metric.metric import TEDS
import Levenshtein

sys.path.append(os.path.dirname(__file__) + "/../../table_evaluation")


class MdTester:
    def __init__(self):
        pass

    @staticmethod
    def eval_by_table(pred, gt):
        gt_score = [0.0] * len(gt)
        table_num = len(gt)
        pred_arr = []
        gt_arr = []
        if len(gt) > 0 and len(pred) > 0:
            gt_cell_total = [None] * len(gt)
            pred_cell_total = [None] * len(pred)

            for idx, table_g in enumerate(gt):
                gt_str = re.findall('>(.*?)<', table_g.replace('\xa0', ''))
                gt_str = [g_s for g_s in gt_str if g_s]
                gt_cell_total[idx] = gt_str
                gt_arr.append(''.join(gt_str))

            for idx, table_p in enumerate(pred):
                pred_str = re.findall('>(.*?)<', table_p.replace('\xa0', ''))
                pred_str = [p_s for p_s in pred_str if p_s]
                pred_cell_total[idx] = pred_str
                pred_arr.append(''.join(pred_str))
            # 按表格中文本的最小编辑距离，match pred 与GT
            match_array = [[Levenshtein.distance(''.join(p), ''.join(g)) for p in pred_cell_total] for g in gt_cell_total]
            mini_data = [min(data) for data in match_array]
            match_pred_index = [match_array[i].index(data) for i, data in enumerate(mini_data)]
            for gt_index, pred_index in enumerate(match_pred_index):
                if MdTester.clean_text(pred_arr[pred_index]) == MdTester.clean_text(gt_arr[gt_index]):
                    gt_score[gt_index] = 1.0

        return table_num, gt_score

    @staticmethod
    def eval_by_teds_match(pred, gt):
        """
        将pred和gt中的表格进行匹配
        如果

        """

        def struct_clean(input_str):
            input_str = re.sub('<colgroup>.*?</colgroup>', '', input_str)
            return input_str

        gt_score = [0.0] * len(gt)
        total_score = 0.0
        table_num = len(gt)
        teds = TEDS(structure_only=False)

        if len(gt) > 0 and len(pred) > 0:
            gt_cell_total = [None] * len(gt)
            pred_cell_total = [None] * len(pred)

            for idx, table_g in enumerate(gt):
                gt_str = re.findall('>(.*?)<', table_g.replace('\xa0', ''))
                gt_str = [g_s for g_s in gt_str if g_s]
                gt_cell_total[idx] = gt_str

            for idx, table_p in enumerate(pred):
                pred_str = re.findall('>(.*?)<', table_p.replace('\xa0', ''))
                pred_str = [p_s for p_s in pred_str if p_s]
                pred_cell_total[idx] = pred_str
            # 按表格中文本的最小编辑距离，match pred 与GT
            match_array = [[Levenshtein.distance(''.join(p), ''.join(g)) for p in pred_cell_total] for g in
                           gt_cell_total]
            # match_array = np.array(match_array)
            # 按照文本编辑距离取框
            # match_pred_index = np.argmin(match_array, axis=0).tolist()
            mini_data = [min(data) for data in match_array]
            match_pred_index = [match_array[i].index(data) for i, data in enumerate(mini_data)]
            for gt_index, pred_index in enumerate(match_pred_index):
                if gt_score[gt_index] == 0.0:
                    gt_score[gt_index] = max(0.0, teds.evaluate(struct_clean(pred[pred_index]),
                                                                struct_clean(MdTester.clean_table(gt[gt_index]))))
                else:
                    gt_score[gt_index] = max(gt_score[gt_index], teds.evaluate(struct_clean(pred[pred_index]),
                                                                               struct_clean(
                                                                                   MdTester.clean_table(gt[gt_index]))))

        if table_num > 0:
            total_score = sum(gt_score) / table_num

        return total_score, gt_score

    @staticmethod
    def get_table_struct(table_str):
        table_str = re.sub('<table.*?>', '<table>', table_str)
        table_str = re.sub('<tr.*?>', '<tr>', table_str)
        table_str = re.sub('<td.*?>', '<td>', table_str)
        table_str = re.sub('<td>.*?</td>', '<td>-</td>', table_str)
        return table_str

    @staticmethod
    def eval_by_struct_teds_match(pred, gt):
        def struct_clean(input_str):
            input_str = re.sub('<colgroup>.*?</colgroup>', '', input_str)
            return input_str

        """
        将pred和gt中的表格进行匹配
        如果

        """

        gt_score = [0.0] * len(gt)
        total_score = 0.0
        table_num = len(gt)
        teds = TEDS(structure_only=False)

        if len(gt) > 0 and len(pred) > 0:
            gt_cell_total = [None] * len(gt)
            pred_cell_total = [None] * len(pred)

            for idx, table_g in enumerate(gt):
                gt_str = re.findall('>(.*?)<', table_g.replace('\xa0', ''))
                gt_str = [g_s for g_s in gt_str if g_s]
                gt_cell_total[idx] = gt_str

            for idx, table_p in enumerate(pred):
                pred_str = re.findall('>(.*?)<', table_p.replace('\xa0', ''))
                pred_str = [p_s for p_s in pred_str if p_s]
                pred_cell_total[idx] = pred_str
            # 按表格中文本的最小编辑距离，match pred 与GT
            match_array = [[Levenshtein.distance(''.join(p), ''.join(g)) for p in pred_cell_total] for g in
                           gt_cell_total]
            mini_data = [min(data) for data in match_array]
            match_pred_index = [match_array[i].index(data) for i, data in enumerate(mini_data)]
            pred = [MdTester.get_table_struct(table_str) for table_str in pred]
            gt = [MdTester.get_table_struct(table_str) for table_str in gt]
            for gt_index, pred_index in enumerate(match_pred_index):
                if gt_score[gt_index] == 0.0:
                    gt_score[gt_index] = max(0.0,
                                             teds.evaluate(struct_clean(pred[pred_index]), struct_clean(gt[gt_index])))
                else:
                    gt_score[gt_index] = max(gt_score[gt_index],
                                             teds.evaluate(struct_clean(pred[pred_index]), struct_clean(gt[gt_index])))

        if table_num > 0:
            total_score = sum(gt_score) / table_num

        return total_score, gt_score

    @staticmethod
    def clean_table(input_str, flag=True):
        if flag:
            input_str = input_str.replace('<sup>', '').replace('</sup>', '')
            input_str = input_str.replace('<sub>', '').replace('</sub>', '')
            input_str = input_str.replace('<span>', '').replace('</span>', '')
            input_str = input_str.replace('<div>', '').replace('</div>', '')
            input_str = input_str.replace('<p>', '').replace('</p>', '')
            input_str = input_str.replace('<spandata-span-identity="">', '')
        return input_str

    @staticmethod
    def clean_text(input_str, flag=True):
        if flag:
            input_str = input_str.replace('一', '-').replace('—', '-').replace('·', '•').replace(' ', '')
            input_str = input_str.replace('•', '·')
            input_str = input_str.replace('-', '')
            input_str = input_str.replace('**', '')
        return input_str

    @staticmethod
    def fetch_result_table_json(pred_md):
        """
        pred_md format edit
        """
        pred_md = pred_md.split("\n\n")
        table_flow = []
        table_flow_no_space = []
        for idx, md_i in enumerate(pred_md):
            if '<table' in md_i.replace(" ", "").replace("'", '"'):
                table_res = html.unescape(md_i).replace('\\', '').replace('\n', '')
                table_res = unicodedata.normalize('NFKC', table_res).strip()
                table_res = re.sub('<table.*?>', '', table_res)
                table_res = re.sub('</?tbody>', '', table_res)
                table_res = re.sub('( style=".*?")', "", table_res)
                table_res = re.sub('( height=".*?")', "", table_res)
                table_res = re.sub('( width=".*?")', "", table_res)
                table_res = re.sub('( align=".*?")', "", table_res)
                table_res = re.sub('( class=".*?")', "", table_res)
                table_res_no_space = '<html><body><table border="1" >' + table_res.replace(' ', '') + '</body></html>'
                # table_res_no_space = re.sub(' (style=".*?")',"",table_res_no_space)
                table_res_no_space = re.sub(r'[ $]', "", table_res_no_space)
                table_res_no_space = re.sub('colspan="', ' colspan="', table_res_no_space)
                table_res_no_space = re.sub('rowspan="', ' rowspan="', table_res_no_space)
                table_res_no_space = re.sub('border="', ' border="', table_res_no_space)

                table_res = '<html><body>' + table_res + '</body></html>'
                table_flow.append(table_res)
                table_flow_no_space.append(table_res_no_space)
        return table_flow, table_flow_no_space

    def __call__(self, raw_meta_json, raw_pred_json):
        tables = re.findall(r'<table[\s\S]*?</table>', raw_pred_json)
        new_tb = [re.sub(r'\*\*(.*?)\*\*', lambda x: x.groups()[0], table) for table in tables]
        for table, clean_table in zip(tables, new_tb):
            raw_pred_json = raw_pred_json.replace(table, clean_table)

        table_pred, table_pred_n_spc = MdTester.fetch_result_table_json(raw_pred_json)
        table_gt, table_gt_n_spc = MdTester.fetch_result_table_json(raw_meta_json)

        if len(table_gt) > 0:
            table_num, eval_res_n_spc = MdTester.eval_by_table(table_pred_n_spc, table_gt_n_spc)
            _, score_i_n = MdTester.eval_by_teds_match(table_pred_n_spc, table_gt_n_spc)
            _, struct_score = MdTester.eval_by_struct_teds_match(table_pred_n_spc, table_gt_n_spc)
        else:
            table_num = 0
            eval_res_n_spc = [0]
            score_i_n = [0]
            struct_score = [0]

        return table_num, eval_res_n_spc, score_i_n, struct_score
