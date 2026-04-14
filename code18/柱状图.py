import json
import re

def main(csv_string):
    # 1. 去除 Markdown 代码块标记和 BOM
    csv_string = csv_string.strip()
    if csv_string.startswith('\ufeff'):
        csv_string = csv_string[1:]
    if csv_string.startswith('```csv'):
        csv_string = csv_string[5:]
    elif csv_string.startswith('```'):
        csv_string = csv_string[3:]
    if csv_string.endswith('```'):
        csv_string = csv_string[:-3]
    csv_string = csv_string.strip()

    # 2. 按行分割（保留非空行）
    lines = [line.strip() for line in csv_string.splitlines() if line.strip()]
    if len(lines) < 2:
        return {"result": f"错误：CSV 至少需要两行（标题+数据）。实际行数：{len(lines)}"}

    # 3. 手动解析 CSV 行（支持引号内逗号）
    def parse_csv_row(row_str):
        fields = []
        current = ''
        in_quotes = False
        for ch in row_str:
            if ch == '"':
                in_quotes = not in_quotes
            elif ch == ',' and not in_quotes:
                fields.append(current.strip())
                current = ''
            else:
                current += ch
        fields.append(current.strip())
        # 去除字段首尾的引号
        fields = [f.strip('"') for f in fields]
        return fields

    parsed_lines = [parse_csv_row(line) for line in lines]

    # 自动修复：如果第一行只有一个字段且第二行有多个字段，则丢弃第一行
    if (len(parsed_lines) >= 2 and len(parsed_lines[0]) == 1 and
        len(parsed_lines[1]) > 1):
        parsed_lines = parsed_lines[1:]  # 丢弃第一行

    if len(parsed_lines) < 2:
        return {"result": "错误：解析后不足两行数据"}

    headers = parsed_lines[0]
    data_rows = parsed_lines[1:]

    # 确保所有数据行与标题行列数一致
    max_cols = len(headers)
    for row in data_rows:
        if len(row) < max_cols:
            row.extend([''] * (max_cols - len(row)))
        elif len(row) > max_cols:
            row[:] = row[:max_cols]

    # 数字转换函数（自动去除逗号、空格，提取数字）
    def to_float(s):
        if not isinstance(s, str):
            s = str(s) if s is not None else ''
        s = s.strip()
        s = s.replace(',', '')
        # 提取数字（包括负号和小数点）
        match = re.search(r'-?\d+(?:\.\d+)?', s)
        if match:
            try:
                return float(match.group())
            except:
                return None
        return None

    # 识别数值列（从第二列开始）
    numeric_col_indices = []
    numeric_col_names = []
    for col_idx in range(1, max_cols):
        for row in data_rows:
            val = row[col_idx] if col_idx < len(row) else ''
            if to_float(val) is not None:
                numeric_col_indices.append(col_idx)
                numeric_col_names.append(headers[col_idx])
                break

    if not numeric_col_indices:
        sample = f"标题行: {headers}\n第一行数据: {data_rows[0] if data_rows else '无'}"
        return {"result": f"错误：没有找到数值列。请检查 CSV 中是否包含数字。\n解析结果样例：\n{sample}"}

    # X 轴类别（第一列）
    x_axis_data = [row[0].strip() or f"项{i+1}" for i, row in enumerate(data_rows)]

    # 构建系列
    series_list = []
    for idx, col_idx in enumerate(numeric_col_indices):
        series_data = []
        for row in data_rows:
            val = row[col_idx] if col_idx < len(row) else ''
            num = to_float(val)
            if num is None:
                num = 0
            series_data.append(num)
        series_list.append({
            "name": numeric_col_names[idx],
            "type": "bar",
            "data": series_data
        })

    # ECharts 配置
    echarts_config = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": numeric_col_names},
        "xAxis": {"type": "category", "data": x_axis_data, "axisLabel": {"rotate": 30 if len(x_axis_data) > 8 else 0}},
        "yAxis": {"type": "value"},
        "series": series_list
    }

    output = f'```echarts\n{json.dumps(echarts_config, ensure_ascii=False)}\n```'
    return {"result": output}