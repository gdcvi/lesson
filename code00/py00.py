# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

"""
 * @author: zkyuan
 * @date: 2025/7/18 10:12
 * @description: 
"""
print('PyCharm')
a = 1
b = 2
print(a + b)
# 输出多个值，用逗号隔开
print(a, b)
# sep的值用来分隔多个值，默认是空格
print(a, b, sep='分割符')
# end的值来设定结尾，默认是\n
print(a, b, sep='---', end='结束符\n')

# 虚数、复数，虚数只能用j
ma = 1 + 2j
print(ma)

# 字符串 单引号、双引号、三个双引号
str1 = '单引号'
str2 = "双引号"
str3 = """
三个双引号的字符串
"""
print(str3)
# 若三个双引号没有赋值给变量，则为注释
""" 这是注释 """

# 占位符 %  字符串%s 整形%d 浮点型%f
# 单个站位
print("占位符输出：%s" % str1)
# 多个站位，%( , )
print("占位符输出：%s %s" % (str1, str2))
print("占位符输出：%s，占位符个数：%d" % (str1, 2))
# %04d输出四位，前面补0
# %.4f保留四位小数
# %% 百分号
print("%%" % ())
print("输出百分号：%")
print("占位符输出百分号：%%" % ())

# 格式化输出 f"{表达式}"
age = 18
name = "zky"
print(f"我的名字是{name}，我的年龄是{age}")

