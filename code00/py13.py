"""
 * @author: zkyuan
 * @date: 2025/7/18 10:17
 * @description: 面向对象
"""

# 类（类名、属性、方法）
"""
class 类名:
    代码块
"""


# 类
class Washer:
    # 类属性
    height = 800

    def wash(self):  # self表示调用当前方法的对象
        self.height = 880
        print("洗衣机洗衣服")


# 获取类属性
print(Washer.height)
# 增加属性
Washer.width = 500
print(Washer.width)

# 创建对象：类名()
w = Washer()
print(w)
print(w.height)
print(w.width)

# 实例方法和实例属性
# 由对象调用，至少有一个self参数，执行实例方法时，自动调用该方法的对象赋值给self
# self表示调用当前方法的对象
w.wash()


class Person:
    name = "zky"
    age = 18

    # 实例化对象（new对象）时，自动调用
    # 构造函数 __init__() 通常用来做属性初始化或者赋值
    def __init__(self, salary, teacher):
        # self.salary = 10000
        # self.teacher = "张三"
        self.salary = salary
        self.teacher = teacher
        print("__init__构造函数")

    def per(self):
        # 实例属性 self.属性名
        print(f"姓名：{self.name}，年龄：{self.age}")
        # 公共的，都能访问
        print("类属性（Person.name）：" + Person.name)
        # 对象私有的，只能由对象访问
        print("实例属性（self.name）：" + self.name)
        # 对象私有属性的访问
        print(f"height:{self.height}")
        print(f"月薪{self.salary}元,老师是{self.teacher}")

    def run(self):
        print(f"{self.name}会跑步！")

    def eat(self):
        print(f"{self.name}在{self.age}岁的时候吃蛋糕了！")

    # 析构函数__del__()，删除对象的时候，解释器默认调用__del__()方法
    def __del__(self):
        print("析构函数__del__方法，对象销毁")  # 代码运行结束（对象销毁时）会执行这行


# 对象:创建对象也叫实例化对象

p = Person(10000, "张三")  # 构造函数的参数
p.height = 180
# 调用实例化方法
p.per()
p.run()
p.eat()
del p  # 手动销毁时，执行这行后执行析构函数
print("这是最后一行代码")
