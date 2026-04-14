import csv
import json

def main(csv_string: str):
    """
    将 CSV 格式的字符串转换为 ECharts 饼状图配置。
    CSV 至少包含两列：第一列为类别标签，第二列为数值。
    """
    # 解析 CSV 字符串
    lines = csv_string.strip().split('\n')
    reader = csv.reader(lines)
    rows = list(reader)

    if len(rows) < 2:
        # 没有数据行，返回空配置
        return {"result": "```echarts\n{}\n```"}

    # 提取标签和数值
    labels = []
    values = []
    for row in rows[1:]:
        if len(row) >= 2:
            label = row[0].strip()
            try:
                value = float(row[1])
            except ValueError:
                continue
            if value > 0:  # 饼图只取正值
                labels.append(label)
                values.append(value)

    if not values:
        return {"result": "```echarts\n{}\n```"}

    # 构造饼图数据格式
    pie_data = [{"name": label, "value": val} for label, val in zip(labels, values)]

    # ECharts 饼图配置
    echarts_config = {
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "data": labels
        },
        "series": [{
            "name": "数据分布",
            "type": "pie",
            "radius": "50%",
            "data": pie_data,
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    }

    # 生成输出（格式与原始代码一致）
    output = f'```echarts\n{json.dumps(echarts_config, ensure_ascii=False)}\n```'
    return {"result": output}