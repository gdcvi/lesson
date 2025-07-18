"""
 * @author: zkyuan
 * @date: 2025/7/18 10:18
 * @description: 迭代器、生成器
"""
# 可迭代对象Iterable:依次从对象中把元素取出来
# str、list、tuple、dict、set、迭代器、生成器等能被for遍历取值的
# 可迭代对象>迭代器>生成器
"""
可迭代对象的条件
    1、对象实现了__iter__()方法
    2、__iter__()方法返回了迭代器对象
"""
# isinstance(o,t)：o：对象，t：类型；判断一个对象是否是可迭代对象或是一个已知的数据类型
# 导入模块
# from collections.abc import Iterator
instance = isinstance(123, str)
print(instance)

# 迭代器Iterator：是一个可以记住遍历位置的对象，在上次停留的位置继续做一些事情
# iter()：获取可迭代对象的迭代器
# next()：一个个去获取元素，取完元素后会引发一个异常StopIteration
li = [1, 2, 3, 4, 5]
li1 = iter(li)
print(next(li1))
print(next(li1))
print(next(li1))
print(next(li1))

# iter()调用对象的__iter__()，并把__iter__()方法的返回值结果作为自己的返回值
li2 = li.__iter__()
print(li2.__next__())
print(li2.__next__())
print(li2.__next__())
print(li2.__next__())
print(li2.__next__())

# 可迭代对象iterable和迭代器iterator
# 凡是可以作用于for循环的都是可迭代对象
# 凡是可以作用于next()的都是迭代器
# 可迭代对象并不一定是迭代器对象
# 迭代器对象一定是可迭代对象
# 可迭代对象可以通过iter()方法转换成迭代器对象
# 如果一个对象拥有__iter__()，是可迭代对象；如果一个对象拥有__next__()和__iter__()方法，是迭代器对象。（用dir(obj)查看）

print("----------------------------")


# 自定义迭代器类
# 两个特性：__iter__和__next__
class Test:
    def __init__(self):
        self.num = 1

    def funa(self):
        print(self.num)
        self.num += 1


t = Test()
t.funa()
t.funa()
t.funa()


class MyIterator:
    """自定义迭代器"""

    def __init__(self):
        self.num = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.num == 10:
            raise StopIteration("迭代完成！")
        self.num += 1
        return self.num


m = MyIterator()

print(next(m))

print(m.__next__())

for i in m:
    print(i)  # 迭代完成，抛出异常时正常结束for循环

# 生成器generator：python中一边循环一边计算的机制叫做生成器
# 生成器表达式
# 列表推导式
l = [i * 2 for i in range(5)]
print(l)
# 将[]改成()就成了生成器
gen = (i * 2 for i in range(5))
print(gen)

print(gen.__next__())
print(next(gen))  # 生成器也是可迭代对象


# python中，使用了yield关键字的函数被称为生成器函数
# yield的作用
# 1、类似return，将指定值或多个值返回给调用者
# 2、yield语句一次返回一个结果，每个结果中间，挂起函数，执行next()，在重新从挂起点继续执行

# 生成器函数
def gene():
    print("生成器函数")
    yield 'a'  # 返回一个'a'，并暂停，下一次在此开始，并不会从头开始
    yield 'b'
    yield 'c'
    yield 'd'


g = gene()
print(g.__next__())
print("================")


def gene2(n):
    i = 0
    while i < n:
        yield i
        i += 1


for i in gene2(5):
    print(i)
