"""
 * @author: zkyuan
 * @date: 2025/7/18 10:17
 * @description: 封装与继承
"""


# 面向对象的三大特性：封装、继承、多态
class Person:
    # 普通属性
    name = "zky"
    age = 18
    # 双下划线隐藏属性（内部访问，无法被继承，其他文件无法导入，一般是魔术方法或属性，有特殊含义如常量，轻易不要定义）
    __idCard = None
    # 单下划线的隐藏属性（外部可以使用，子类可以继承，但是其他文件无法导入，一般是为了避免与关键字冲突）
    _sex = "男"

    def __init__(self, salary, teacher):
        self._Person__idCard = 429006199907150011
        self.salary = salary
        self.teacher = teacher
        print("__init__构造函数")

    def money(self):
        self.__play()
        print("Person的Money方法")

    def info(self):
        # 内部访问隐藏方法
        print(f"姓名为：{Person.name},身份证号码为：{Person.__idCard}")
        print(f"姓名为：{Person.name},身份证号码为：{self.__idCard}")
        print(f"姓名为：{Person.name},身份证号码为：{self.__idCard}，性别为：{self._sex}")
        Person.__play(self)  # 在实例方法中调用私有方法，不推荐
        self.__play()  # 更简单
        self._play2()

    def __del__(self):
        print("析构函数__del__，对象销毁")

    @property
    def sex(self):
        return self._sex

    def __play(self):
        print(f"{self.name}在玩手机，双下划线私有方法")

    def _play2(self):
        print(f"{self.name}在学习，单下划线方法")


# 隐藏属性（私有权限），只允许在类的内部使用，无法通过对象访问，
# 在属性名或方法名的前面加上两个下划线
p = Person(10000, "张三")
p.info()
# 在外部访问双下划线隐藏属性：对象名._类名__属性名（少用甚至不用，不规范）
print(p._Person__idCard)
# 外部访问单下划线属性
print(p.sex)
print("---------------------------------------------------")

# 继承
"""
class 类名(父类名):
    代码块
"""


# 单继承
# 继承父类的属性和方法
class China(Person):
    GuoJi = "中国"

    def money(self):
        print("China的Money方法")
        pass  # 占位符，代码里面不写任何东西，会自动跳过不会报错


me = China(20000, "张起灵")
me.info()


class Boy(Person):
    sex = "boy"

    def boy(self):
        print(self.sex)

    def one(self):
        print(f"这是{self.sex}的one方法")


class Girl(Person):
    sex = "girl"

    def girl(self):
        print(self.sex)

    def one(self):
        print(f"这是{self.sex}的one方法")


b = Boy(30000, "zkyuan")
g = Girl(12000, "zkyuan")


# 传递继承：继承所有上面祖先的属性和方法
class ChinaBoy(China):
    def money(self):
        # 调用父类方法重载，用super() 或 父类名
        Person.money(self)
        super().money()
        super().money()
        print("ChinaBoy的Money方法")
        super(ChinaBoy, self).money()

    pass


cb = ChinaBoy(100000, "zkyuan")
cb.info()
print("----------------------------------------")
# 方法重写：覆盖
"""
    1、父类名.方法名(self)
    2、super().方法名()      多用这种
    3、super(子类名,self).方法名()
"""
p.money()
me.money()
b.money()
g.money()
cb.money()

# 新式类
"""
    class A: 经典类：不由任意内置类型派生出的类
    class A(B): 派生类，继承B后有新的属性或方法
    class A(object): 新式类：继承了object类。推荐使用。dir()函数查看 
    （所有类都继承object类，是为基类。且python3之后都是新式类，默认基础）
"""


class A(object):
    paa = 2


# 多继承：可以有多个父类

class Student(Girl, Boy):
    num = 125487542

    def stu(self):
        print(f"这是一个学生类,学号：{self.num}")


student = Student(3000, "zkyuan")

# 多个父类有同名方法时，按着就近原则，调用继承父类时写在前面的；且子类优先
student.one()
# 查看python中方法搜索顺序  __mro__
print(Student.__mro__)
