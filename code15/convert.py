import csv
import json
import sys

def convert_csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            if len(row) < 2:
                continue
            # system列（row[0]）是固定角色描述，conversation列（row[1]）是JSON字符串
            conversation_str = row[1].strip()
            try:
                conversation = json.loads(conversation_str)
            except json.JSONDecodeError:
                print(f"警告：无法解析JSON行：{conversation_str[:100]}...", file=sys.stderr)
                continue
            # conversation是一个列表，每个元素是{"human": ..., "assistant": ...}
            for turn in conversation:
                if "human" in turn and "assistant" in turn:
                    instruction = turn["human"]
                    output = turn["assistant"]
                    # input字段留空
                    data.append({
                        "instruction": instruction,
                        "input": "",
                        "output": output
                    })
    # 如果不足1000条，输出所有；如果超过1000条，取前1000
    if len(data) > 1000:
        data = data[:1000]
        print(f"数据超过1000条，已截取前1000条。")
    else:
        print(f"数据共 {len(data)} 条，不足1000条，已全部输出。")
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 假设CSV文件名为 input.csv，输出文件名为 output.json
    convert_csv_to_json("input.csv", "train_03.json")