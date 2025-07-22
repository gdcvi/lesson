"""
 * @author: zkyuan
 * @date: 2025/7/18 10:14
 * @description: 异常
"""
# 对异常进行捕获处理，发生异常继续运行
"""
格式1：
    try:
        不确定是否能正常执行的代码（一般只当一行代码）
    except：
        如果有异常，执行这部分代码
可以指定捕获异常类型，但是遇到其他异常类型无法捕获会报错
可以指定多个类型，用元组的形式(TypeError, NameError),Exception为所有异常的父类
"""
try:
    print(a)
except (TypeError, NameError) as e:  # as相当于取别名，e：变量名
    print("发生了异常")
    print(e, type(e))  # 打印异常信息
    if str(type(e)) == "<class 'NameError'>":
        print(3333333333333)

"""
格式2：
    try:
        不确定是否能正常执行的代码
    except：
        如果有异常，执行这部分代码
    else:
        没有捕获到异常的代码
"""
aaa = 2
try:
    print(aaa)
except Exception:
    print("发生了异常")
else:
    print("没有发生异常")

"""
格式2：
    try:
        不确定是否能正常执行的代码
    except：
        如果有异常，执行这部分代码
    else:
        没有捕获到异常的代码
    finally:
        try（以及except和else部分）代码块结束后运行的代码，无论是否有异常最后都会执行
可以单独使用try和finally
"""
try:
    print(aa)
except Exception:
    print("发生了异常")
else:
    print("没有异常")
finally:
    print("finally部分")

# 自定义异常

"""
1、创建一个Exception('xxx')对象，
2、raise抛出这个异常对象
3、程序终止
"""

# raise Exception("这是自定义异常")


def fune():
    print("可以的")
    raise Exception("自定义异常")
    #print("raise后面")  # 这部分不会执行，爆黄线


# fune()


# 密码验证
def login():
    password = input("请输入密码")
    if len(password) >= 6:
        print("密码输入成功")
    else:
        raise Exception("密码长度太短")


login()
