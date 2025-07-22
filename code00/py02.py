"""
 * @author: zkyuan
 * @date: 2025/7/18 10:13
 * @description: if判断
"""
# if判断 冒号一定要有
# 代码格式整理：ctrl+alt+L
a = 1
if a > 0:
    print("true")
else:
    print("false")

# 比较运算符 == ！= > < >= <=
# 逻辑运算符 and or not
# 三目运算符 ：为真结果 if 判断条件 else 为假结果
print("true") if a > 0 else print("fales")

# score 成绩90-100优秀，60-90合格，0-60不合格
# score = int(input("请输入成绩"))
score = 900
flag = 1
while flag == 1:
    score = int(input("请输入成绩"))
    if score >= 90 and score <= 100:  # 可以这样写 90 <= score <= 100
        print("成绩优秀")
        flag = 0
    elif score >= 60 and score < 90:
        print("成绩合格")
        flag = 0
    elif score >= 0 and score < 60:
        print("成绩不合格")
        flag = 0
    else:
        print("成绩输入错误，请重新输入")
        flag = 1
