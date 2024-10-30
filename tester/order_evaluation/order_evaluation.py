from utils import *
import re


class OrderEval(object):
    def __init__(self) -> None:
        self.threshold = 1.0
        self.threshold_bl = 0.8

    def __call__(self, raw_meta_json, raw_pred_json) -> dict:
        order_res = {}
        gt_objects = OrderEval.extract_objects_from_string(raw_meta_json)
        pred_objects = OrderEval.extract_objects_from_string(raw_pred_json)
        score = self.compute_order_score(gt_objects, pred_objects)
        order_res['order_score'] = score

        return order_res

    @staticmethod
    def extract_objects_from_string(s):
        texts = s.split('\n\n')
        objects = []

        for text in texts:
            text = text.strip()
            text = text.lstrip('\n')
            if text:  # Check if the stripped text is not empty
                if text.startswith('<table') and text.endswith('</table>'):
                    objects.append([text, 'table'])
                elif text.startswith('#') and '\n' not in text:
                    objects.append([text, 'title'])
                elif text.startswith('$'):
                    objects.append([text, 'formula'])
                else:
                    objects.append([text, 'text'])

        return objects

    @staticmethod
    def object_2_string(item):
        item[0] = remove_special_chars(item[0])
        if item[1] == 'table':
            the_list = re.findall('>(.*?)<', item[0].replace('\xa0', ''))  # extract only table info
            item[0] = ''.join(the_list)

    @staticmethod
    def compute_order_score(gt_objects, pred_objects):
        threshold = 0.8

        for gt_object in gt_objects:
            OrderEval.object_2_string(gt_object)

        for pred_object in pred_objects:
            OrderEval.object_2_string(pred_object)

        matched_gt_set = set()
        gt_objects_ = gt_objects.copy()
        for pred_object in pred_objects:
            best_score = 0
            matched_gt_text = None
            pred = pred_object[0]
            index_ = None
            for index, gt_object in enumerate(gt_objects):
                gt = gt_object[0]
                if gt in matched_gt_set:
                    continue
                if pred_object[1] == gt_object[1]:  # 类型相同
                    score = get_edit_distance_score(pred, gt)
                    if score > best_score and score > threshold:
                        best_score = score
                        matched_gt_text = gt
                        index_ = index
            if matched_gt_text is not None:
                gt_objects.pop(index_)
                pred_object[0] = matched_gt_text
            else:
                pred_object[0] = ''

        pred_all_text = ''
        gt_all_text = ''

        for pred_object in pred_objects:
            pred_all_text += pred_object[0]

        for gt_object in gt_objects_:
            gt_all_text += gt_object[0]

        order_score = get_edit_distance_score(pred_all_text, gt_all_text)

        return order_score
