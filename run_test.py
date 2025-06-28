import os
import statistics
import pandas as pd
import argparse
from tester.test_function import TestFunction
from utils import create_dict_from_folders, create_radar_chart
import json
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', None)


def main():
    parser = argparse.ArgumentParser(description="请输入文件路径")
    parser.add_argument('--pred_path', type=str, default='dataset/pred', help='预测值文件')
    parser.add_argument('--gt_path', type=str, default='dataset/gt', help='真值文件')
    args = parser.parse_args()
    total = create_dict_from_folders(args.pred_path)

    results = {}
    file_results = {}
    for folder_name, files in total.items():
        current_metrics = {}

        folder_a_path = args.gt_path
        folder_b_path = f"{args.pred_path}/{folder_name}"

        for file_name in os.listdir(folder_a_path):
            base_name = os.path.splitext(file_name)[0]
            pred_file = os.path.join(folder_b_path, f"{base_name}.md")

            if os.path.exists(pred_file):
                with open(os.path.join(folder_a_path, file_name), 'r', encoding='utf-8') as f:
                    gt_content = f.read()
                with open(pred_file, 'r', encoding='utf-8') as f:
                    pred_content = f.read()

                body = TestFunction()(gt_content, pred_content)
                file_results[file_name] = body
                for key, value in body.items():
                    if key not in current_metrics:
                        current_metrics[key] = []
                    if value is not None:
                        current_metrics[key].append(value)

        results[folder_name] = {key: statistics.mean(val) if val else 0 for key, val in current_metrics.items()}
    with open('file_results.json', 'w', encoding='utf-8') as f:
        json.dump(file_results, f, ensure_ascii=False, indent=4)
    df = pd.DataFrame(results)
    print(df.to_string())
    create_radar_chart(df.transpose(), 'performance test results', 'performance_test_results.png')
    df.to_excel('performance_test_results.xlsx', index=True)


if __name__ == "__main__":
    main()
