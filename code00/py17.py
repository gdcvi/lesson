"""
 * @author: zkyuan
 * @date: 2025/7/18 10:18
 * @description: 单例模式、魔法方法
"""


class Person(object):
    """类属性：类所拥有的属性"""
    familyName = "Person"

    def __new__(cls, *args, **kwargs):
        """
            new方法：在内存中为对象分配空间，返回对象引用
            new方法重写后，就没有__init__了，也覆盖了父类的new方法
            重新new方法要继承父类new方法,new对象后要返回，并return类对象，否则对象无法得到分配的内存空间，创建的对象为None
            new是静态方法，必须要传cls参数，
        """
        print("开始new对象")
        # print(super().__new__(cls))
        # 返回的对象传到__init__方法里
        return super().__new__(cls)

    def __init__(self):
        """实例属性：对象私有"""
        self.age = 18
        print("__init__方法")

    def play(self):
        """实例方法"""
        """可以访问类属性"""
        print(f"{self.familyName},{self.age}")

    @staticmethod
    def sfn(params):
        """静态方法"""
        """可以访问类属性，但是没有意义；不能访问实例属性。"""
        print(f"{params}，{Person.familyName}")

    @classmethod
    def cfn(cls):
        """类方法"""
        """不能访问实例属性,可以访问静态方法"""
        cls.sfn(333)
        print(f"{cls.familyName}")


p = Person()
Person.sfn("222")
p.sfn("999")
p.cfn()
print("------------------------------------")
"""
 单例模式：确保一个类只有一个对象
 可以理解为一个特殊的类，无论创建多少个对象，都是同一个对象
 优点：节省内容空间。缺点：多线程访问时有线程安全问题
 1、通过@classmethod实现
 2、通过装饰器实现
 3、通过重写__new__()方法实现
 4、通过导入模块实现
"""

# 3、通过重写__new__()方法实现
"""
    设计流程
    1、定义一个类属性，初始值为None，用来记录单例对象的引用
    2、重新__new__()方法，
    3、判断是否是None，如果是None，就把new方法返回的对象引用保存起来
    4、返回类属性中记录的引用
"""


class Singleton(object):
    # 记录第一个创建的对象
    obj = None

    def __new__(cls, *args, **kwargs):
        print(f"这是new方法,{cls}")  # 这个cls是类本身Singleton
        # 判断obj是否为空
        if cls.obj is None:
            cls.obj = super().__new__(cls)
        return cls.obj

    def __init__(self):
        print("这是init方法")


s1 = Singleton()
print(s1)
s2 = Singleton()
print(s2)

# 4、通过导入模块实现
"""
    在模块里面创建对象，然后通过取别名的方式。模块就是天然的单例模式
"""
from pytest import t as t1
from pytest import t as t2

print(t1)
print(t2)

# 魔法方法：__xxx__()，特殊功能的函数，魔法属性
"""
    __doc__：类、函数的描述信息，多行注释信息
    __module__：表示当前操作对象所在的模块
    __class__：表示当前操作对象所在的类
    __str__：表示对象的描述信息，若类中定义了此方法，那么在打印对象时，默认输出该方法的返回值，也就是return的内容，且必须返回字符串类型
    __del__：析构函数，程序结束时调用，程序结束、删除对象时调用
    __call__：调用回调，使一个实例对象成为一个可调用对象，就像函数那样可以调用。调用对象执行__call__
    ____：
"""
