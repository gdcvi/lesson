"""
 * @author: zkyuan
 * @date: 2025/7/18 10:18
 * @description: 静态方法、类方法
"""

"""
    用装饰器标识
    @staticmethod:静态方法，没有self、cls参数的限制。与类无关，可以被转换成函数使用，取消不必要的参数传递，降低内存销毁
    @classmethod:类方法，第一个参数必须为类对象本身，一般为cls。一般配合类属性使用
"""


class Person(object):
    familyName = "Person"

    @staticmethod
    def study(name):
        """静态方法,调用方法时传参"""
        print(f"{name}人类会学习")

    @classmethod
    def pfun(cls):
        """类方法,cls代表类对象本身"""
        print(f"{cls.familyName}这是类方法")


person = Person()
person.study("zky")
Person.study("zzz")
person.pfun()
