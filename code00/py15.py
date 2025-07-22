"""
 * @author: zkyuan
 * @date: 2025/7/18 10:17
 * @description: 多态
"""


# 多继承的弊端：容易引发冲突，代码更复杂

# 多态：同一种行为有多种不同的表现形式

# 多态的前提：继承、重写

class Animal(object):
    familyName = "Animal"

    def shout(self):
        print(f"{self.familyName}会叫")


class Dog(Animal):
    familyName = "Dog"

    def shout(self):
        print(f"{self.familyName}会叫")


class Cat(Animal):
    familyName = "Cat"

    def shout(self):
        print(f"{self.familyName}会叫")


class Pig(Animal):
    familyName = "Pig"

    def shout(self):
        print(f"{self.familyName}会叫")


dog = Dog()
cat = Cat()
pig = Pig()

dog.shout()
cat.shout()
pig.shout()


def test(obj):
    obj.shout()


test(dog)
test(cat)
test(pig)
