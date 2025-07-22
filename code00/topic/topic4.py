"""
题目4：类与对象

创建一个`Circle`类，要求：

1. 类有一个类属性`pi`值为3.14159
2. 构造函数接收半径参数
3. 有实例方法计算面积和周长
4. 创建一个半径为5的圆对象，调用方法计算并打印面积和周长
"""

class Circle:
    pi = 3.14159  # 类属性

    def __init__(self, radius):
        self.radius = radius  # 实例属性

    def area(self):
        return self.pi * self.radius ** 2

    def circumference(self):
        return 2 * self.pi * self.radius


# 创建圆对象并计算
circle = Circle(5)
print(f"圆的面积: {circle.area():.2f}")
print(f"圆的周长: {circle.circumference():.2f}")
