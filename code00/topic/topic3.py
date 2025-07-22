"""
题目3：字典操作

编写一个Python程序，要求：

1. 创建一个字典，包含3个学生的姓名和成绩（如：{'Alice': 85, 'Bob': 92, '张魁元': 100}）
2. 添加一个新学生'张三'，成绩为88
3. 修改'Bob'的成绩为95
4. 删除成绩最低的学生
5. 打印最终字典和所有学生的平均成绩
"""
# 1. 创建字典
students = {'Alice': 85, 'Bob': 92, '张魁元': 78}
print("初始学生字典:", students)

# 2. 添加新学生
students['张三'] = 88
print("添加David后:", students)

# 3. 修改Bob的成绩
students['Bob'] = 95
print("修改Bob成绩后:", students)

# 4. 删除成绩最低的学生
min_score = min(students.values())
for name, score in list(students.items()):
    if score == min_score:
        del students[name]
print("删除最低分学生后:", students)

# 5. 计算并打印平均成绩
average = sum(students.values()) / len(students)
print(f"学生平均成绩: {average:.2f}")