"""
 * @author: zkyuan
 * @date: 2025/1/21 11:31
 * @description: 包：模块分类管理、递归、闭包、装饰器
"""
import com
# 文件夹里面有“__init__.py”文件，
# 导包时首先执行“__init__.py”文件，控制包的导入行为,不要在里面写太多代码
# 当包被作为模块导入时，包目录下生成一个“__pycache__”文件夹
from com import *  # 导入时执行__init__.py

print(type(com))
register.registerFun()

# __all__：本质上是一个列表，可以控制要引入的东西
login.loginFun()


# 包中包含包

# 递归函数：函数调用自己
# 斐波拉契数列
def feibo(n):
    if n <= 1:
        return n
    return feibo(n - 1) + feibo(n - 2)


for i in range(1, 10):
    print(feibo(i))


# 闭包
# 1、函数嵌套定义
# 2、内层函数使用外层函数的局部变量
# 3、外层函数的返回值是内层函数的函数名

def outer(m):
    n = 10

    def inner():
        print(n)

    return inner  # 返回函数名而不是inner()，是因为inner里面参数多时，写法不规范


# 闭包函数调用
outer(1)()
out = outer(1)
out()


# 函数引用
def funa():
    print("aa")


print(funa)  # 函数名里保存了函数所在的位置的引用（内存地址）
# id()
print(id(funa))


# 每次开启函数都在使用同一份闭包变量

def outer1(m):
    def inner1(n):
        return m + n

    return inner1


outer_re = outer1(10)(111)
print(outer_re)

# 装饰器：让其他函数不在需要变动的情况下增加新的功能
# 装饰器本质上是一个函数，返回值为一个函数对象
# 新函数作为参数传给核心函数，
