# Python编程练习题答案

涵盖了Python基础语法中的变量、运算符、数据结构、控制流、函数、类和文件操作等核心概念，适合检验对Python基础知识的掌握程度。

## 题目1：基础运算与类型转换
编写一个Python程序，要求：
1. 计算15除以4的整数结果和余数
2. 将3.14159四舍五入保留两位小数
3. 判断表达式 `(5 > 3) and (not (2 == 2)) or (4 <= 5)` 的值

### 答案
```python
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
```

## 题目2：列表操作
编写一个Python程序，要求：
1. 创建一个包含数字1-10的列表
2. 使用切片获取列表中第3到第7个元素（索引从0开始）
3. 将列表反向输出
4. 在列表末尾添加数字11，然后在第2个位置插入数字0
5. 删除数字5并打印最终列表

### 答案
```python
# 1. 创建列表
numbers = list(range(1, 11))
print("原始列表:", numbers)

# 2. 获取第3到第7个元素
sliced = numbers[2:7]
print("切片结果:", sliced)

# 3. 反向输出列表
reversed_list = numbers[::-1]
print("反向列表:", reversed_list)

# 4. 添加和插入元素
numbers.append(11)
numbers.insert(1, 0)
print("添加元素后:", numbers)

# 5. 删除数字5并打印最终列表
numbers.remove(5)
print("最终列表:", numbers)
```

## 题目3：字典操作
编写一个Python程序，要求：
1. 创建一个字典，包含3个学生的姓名和成绩（如：{'Alice': 85, 'Bob': 92, '张魁元': 100}）
2. 添加一个新学生'张三'，成绩为88
3. 修改'Bob'的成绩为95
4. 删除成绩最低的学生
5. 打印最终字典和所有学生的平均成绩

### 答案
```python
# 1. 创建字典
students = {'Alice': 85, 'Bob': 92, 'Charlie': 78}
print("初始学生字典:", students)

# 2. 添加新学生
students['David'] = 88
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
```

## 题目4：类与对象
创建一个`Circle`类，要求：
1. 类有一个类属性`pi`值为3.14159
2. 构造函数接收半径参数
3. 有实例方法计算面积和周长
4. 创建一个半径为5的圆对象，调用方法计算并打印面积和周长

### 答案
```python
class Circle:
    pi = 3.14159  # 类属性
    
    def __init__(self, radius):
        self.radius = radius  # 实例属性
        
    def area(self):
        return self.pi * self.radius ** 2
    
    def circumference(self):
        return 2 * self.pi * self.radius

# 创建圆对象并计算
circle = Circle(5)
print(f"圆的面积: {circle.area():.2f}")
print(f"圆的周长: {circle.circumference():.2f}")
```

## 题目5：文件操作
编写一个Python程序，要求：
1. 使用代码创建一个名为"poem.txt"的文件
2. 写入两行诗句："白日依山尽，黄河入海流。\n欲穷千里目，更上一层楼。"
3. 读取文件内容并打印
4. 统计文件中的字符数
5. 将文件重命名为"唐诗.txt"

### 答案
```python
import os

# 1. 创建并写入文件
with open("poem.txt", "w", encoding="utf-8") as f:
    f.write("白日依山尽，黄河入海流。\n")
    f.write("欲穷千里目，更上一层楼。")

# 2. 读取文件内容
with open("poem.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("文件内容:")
    print(content)

# 3. 统计字符数
char_count = len(content)
print(f"文件字符数: {char_count}")

# 4. 重命名文件
os.rename("poem.txt", "唐诗.txt")
print("文件已重命名为'唐诗.txt'")
```

## 题目6：循环、控制
编写一个程序，要求用户输入一个正整数 `n`，计算并输出 `1` 到 `n` 之间所有能被 `3` 或 `5` 整除的数字之和。如果用户输入无效（非整数或小于1），程序应提示重新输入，直到输入有效为止。

要求：
1. 使用 `while` 循环处理输入验证（包括非整数和小于1的整数）。
2. 使用 `for` 循环遍历 `1` 到 `n` 的数字。
3. 用条件语句判断数字是否能被 `3` 或 `5` 整除。
4. 使用异常处理捕获非整数输入。

**示例输出：**

```
请输入一个正整数：abc
输入无效，请重新输入！
请输入一个正整数：-5
输入无效，请重新输入！
请输入一个正整数：10
1到10之间能被3或5整除的数的和为：33
```

### 答案

```python
while True:
    try:
        n = int(input("请输入一个正整数："))
        if n < 1:
            print("输入无效，请重新输入！")
        else:
            break  # 输入有效，退出循环
    except ValueError:  # 捕获非整数输入异常
        print("输入无效，请重新输入！")

total = 0
for i in range(1, n + 1):
    if i % 3 == 0 or i % 5 == 0:  # 判断能否被3或5整除
        total += i

print(f"1到{n}之间能被3或5整除的数的和为：{total}")
```
