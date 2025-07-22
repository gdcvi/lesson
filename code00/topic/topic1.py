"""
题目1：基础运算与类型转换

编写一个Python程序，要求：

1. 计算15除以4的整数结果和余数
2. 将3.14159四舍五入保留两位小数
3. 判断表达式 `(5 > 3) and (not (2 == 2)) or (4 <= 5)` 的值

"""
# 1. 计算15除以4的整数结果和余数
div_result = 15 // 4
remainder = 15 % 4
print(f"15除以4的整数结果是: {div_result}, 余数是: {remainder}")

# 2. 将3.14159四舍五入保留两位小数
rounded = round(3.14159, 2)
print(f"3.14159四舍五入保留两位小数: {rounded}")

# 3. 判断表达式的值
expression_value = (5 > 3) and (not (2 == 2)) or (4 <= 5)
print(f"表达式的结果是: {expression_value}")
