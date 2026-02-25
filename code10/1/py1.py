"""
 * @author: zkyuan
 * @date: 2026/2/25 9:51
 * @description: 基础巩固与模块初探
 任务一：基础语法强化——文本数据清洗
"""

# 原始数据
raw_data = ["  Alice, 85 ", "BOB, 92", "张魁元, 100", "david, 78", "Ella, 95", ""]

print("原始数据:")
print(raw_data)
print()

# 任务1: 数据清洗
cleaned_data = []
for item in raw_data:
    # 跳过空字符串
    if item.strip() == "":
        continue

    # 去除两端空格
    cleaned_item = item.strip()

    # 分割姓名和成绩
    parts = cleaned_item.split(',')

    # 处理姓名：首字母大写，其他小写
    name = parts[0].strip().title()

    # 处理成绩：转换为整数
    score = int(parts[1].strip())

    cleaned_data.append((name, score))

print("清洗后的数据:")
print(cleaned_data)
print()

# 任务2: 转换为字典格式
score_dict = {}
for name, score in cleaned_data:
    score_dict[name] = score

print("字典格式的数据:")
print(score_dict)
print()

# 任务3: 找出成绩最高的学生
if score_dict:  # 确保字典不为空
    max_score = 0
    top_student = ""

    for name, score in score_dict.items():
        if score > max_score:
            max_score = score
            top_student = name

    print(f"成绩最高的学生是: {top_student}，成绩为: {max_score}")
else:
    print("没有有效的学生成绩数据")

print()

# 任务4: 使用列表推导式计算平均分
if score_dict:  # 确保字典不为空
    # 使用列表推导式生成成绩列表
    scores = [score for score in score_dict.values()]

    print("所有成绩列表:")
    print(scores)

    # 计算平均分
    average_score = sum(scores) / len(scores)

    print(f"平均分为: {average_score:.2f}")
else:
    print("无法计算平均分，没有有效数据")

print("\n" + "=" * 50)
print("程序执行完毕！")
