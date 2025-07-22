"""
 * @author: zkyuan
 * @date: 2025/7/18 10:17
 * @description: 装饰器
"""


# 函数作为参数的普通实现方法
def test(fun):
    print("登录")
    print("注册")
    fun()


def test2():
    print("发消息")


test(test2)


# 装饰器

# 装饰器：让其他函数不在需要变动的情况下增加新的功能
# 装饰器本质上是一个函数，返回值为一个函数对象
# 新函数作为参数传给核心函数，

# 标准版装饰器--闭包函数
def send():
    print("发消息222")


# 装饰器
def outer(fn):
    def inner():
        print("装饰部分")
        fn()

    return inner


print(outer(send))
outer(send)
outer(send)()


# 装饰器的原理就是将原有的函数名重新定义为以原函数为参数的闭包

# 语法糖：@装饰器名称，后面不要加小括号
def outer1(fn):
    def inner1():
        print("登录login...")
        fn()

    return inner1


@outer1
def send1():
    print("语法糖装饰发送消息")


send1()


# 有参数的情况1
def outer2(fn):
    def inner2(name):
        print(f"{name}正在登录login...")
        fn()

    return inner2


@outer2
def send2():
    print("语法糖装饰发送消息")


send2("zky")  # 参数给内涵数


# 有参数的情况2
def outer3(fn):
    def inner3(name):
        print(f"{name}正在登录login...")
        fn(name)

    return inner3


@outer3
def send3(name):
    print("语法糖装饰发送消息")


send3("张三")  # 参数给内涵数


# 可变参数
def func(*args, **kwargs):
    print(args)
    print(kwargs)


func("zzz", 'z', name='zky', age='18')


def out(fn):
    def inn(*args, **kwargs):
        print(args)
        print(kwargs)
        fn(*args, **kwargs)

    return inn


@out
def funa(*args, **kwargs):
    print(args)
    print(kwargs)


out(funa("AAA", 'z', name='zky', age='18'))

funa("qqqqqqqqqqqq")


# 多个装饰器的情况
def deco1(fn):
    def inner():
        return "--第一个装饰器--" + fn()

    return inner


def deco2(fn):
    def inner():
        return "--第二个装饰器--" + fn()

    return inner


@deco1
@deco2  # 先装饰deco2，再把结果装饰到到deco2（从下到上，从近到远）
def test3():
    return "--study python--"


print(test3())  # 第一个装饰器第二个装饰器study python
