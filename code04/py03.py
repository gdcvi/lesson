"""
 * @author: zkyuan
 * @date: 2025/7/18 10:13
 * @description: 循环
"""
# while循环
"""
while 循环条件
    循环体
"""
i = 0
while i <= 10:
    print("循环" + str(i))
    i += 1
# 死循环
"""
while True:
    print("死循环")
"""

# for循环
"""
for 临时变量 in 可迭代变量 :
    循环体
"""
str = "hello world !"
for s in str:
    print(s, end="-")
print()

# range() 用来记录循环次数，相当于一个计数器
# range(num1 , num2) 包含前面的，不包含后面的（包前不包后）
# range(num) 只有一个数，这个数就是循环次数，默认0开始
for i in range(1, 6):
    print(i, end=" ")
# 计算1+2+3+...+100
sum1 = 0
for i in range(1, 101):
    sum1 += i
    i += 1
print(sum1)

sum2 = 0
for i in range(101):
    sum2 += i
print(sum2)

# break 结束循环体 ； continue 结束本次循环
