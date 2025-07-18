"""
 * @author: zkyuan
 * @date: 2025/7/18 10:14
 * @description: 函数
"""
# define定义函数
"""
def 函数名(参数1,参数2...):
    函数体
"""


# 调用函数：函数名(实参1，实参2...)
# 函数返回值 return（执行return函数结束），没有返回值默认为None，多个返回值为元组的形式返回

# 参数
# 必备参数（位置参数）：传递和定义参数的顺序及个数必须一致
def fun1(parameter1, parameter2):
    print("fun1函数体：")


fun1(1, 2)


# 默认参数：为参数提供默认值，调用函数可以不穿该参数的值（所有位置参数必须出现在默认参数前面）
def fun2(parameter1, parameter2, a=1):
    print("fun2函数体:")


fun2(1, 2)


# 可变参数：*args，传入的值的数量是可以改变的，可以传多个，也可以不传
def fun3(*args):
    print("fun3函数体：")


fun3()


# 关键字参数：**keyWordsArgs,实参使用键值对的形式(变量名=值)，以字典的形式接收
def fun4(**kwargs):
    print("fun4函数体：")
    print(kwargs)


fun4(name="zky", age="18")

# 函数嵌套：在一个函数里面调用另一个函数
# 嵌套定义

# 作用域  全局变量、局部变量
# 申请为全局变量 global
# nonlocal 申明外一层的局部变量，用此申明，能对上一层的变量进行修改
a = 100


def fun5(*args):
    print("fun5函数体：")
    a = 110
    b = 200
    global c  # 全局变量先申明，再赋值
    c = 300
    print(a)


fun5()  # 110
print(a)  # 100
# print(b) # 报错没有b变量
print(c)  # 300
c = 111
print(c)  # 111


# 匿名函数：函数名 = lambda 形参 : 返回值
# 普通函数
def add(a, b):
    return a + b


print(add(1, 2))
# 匿名函数
add = lambda a, b: a + b
print(add(1, 3))

# 没有参数
fun6 = lambda: "fun1：无参的匿名函数"
print(fun6())

# 默认参数(默认参数必须写在非默认参数后面)
fun7 = lambda name, age=18: (name, age)
print(fun7("zky", 20))
print(fun7("zky"))

# 关键字参数
fun8 = lambda **kwargs: kwargs
print(fun8(name="zhangkyuan", age="22"))

# lambda与if结合

# 内置函数
# 查看所有内置函数
import builtins

print(dir(builtins))  # 大写开头：内置常量名 ； 小写开头：内置函数名
# sum(参数为可迭代对象)
# max(，key=abs) min(，key=) key=abs即比较绝对值的大小
# abs()绝对值
# zip()：将可迭代对象作为参数，将对象中的对应的元素打包成一个元组
list1 = [1, 2, 3]
list2 = ["z", "k", "y"]
for i in zip(list1, list2):
    print(i, type(i))
"""
(1, 'z') <class 'tuple'>
(2, 'k') <class 'tuple'>
(3, 'y') <class 'tuple'>
"""
# 如果元素个数不一致，就按最短的返回
list3 = ["zhang", "kui", "yuan", "26"]
print(list(zip(list1, list3)))  # 类型转换为列表list：[(1, 'zhang'), (2, 'kui'), (3, 'yuan')]

# map()：可以对可迭代对象中的每一个元素进行映射，分别去执行
# map(func,iter1):func自己定义的函数，iter1要放进去的可迭代对象
# iter1中的每个元素都会作为参数去执行func这个函数

fun9 = lambda x: x * 2
m = map(fun9, list1)
# print(list(m), type(m)) # 一个变量被强制类型转换后，值发生了变化
[print(i) for i in m]

# reduce() 累计参数：把可迭代对象中的元素取出，放在函数中执行，结果继续跟下一个元素进行执行
from functools import reduce

# reduce(func,sequence) func：必须是有两个参数的函数，sequence：序列，可迭代对象
add = lambda x, y: x + y
"""
[1,2,3,4]
1 + 2 = 3
3 + 3 = 6
6 + 4 = 10
"""
re = reduce(add, list1)
print(re)

# 拆包
# 对于函数中的多个返回数据，去掉元组、列表、字典，直接获取里面的数据的过程
tua = (1, 2, 3, 4)
print(tua)
print(tua[1])
# 方法1：要求元组内的个数与接收的个数相同;变量不一致报错ValueError
a, b, c, d = tua  # 在获取元组值的时候使用
print(a, b, c, d)
# 方法2：可变参数变量，多在函数调用时使用
x, *y = tua
print(x, y)  # 1 [2, 3, 4]
