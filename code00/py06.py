"""
 * @author: zkyuan
 * @date: 2025/7/18 10:14
 * @description: 元组tuple、字典dict、集合set
"""
# 1.元组tuple： 元素在小括号里面
# 格式：元组名 = (元素1,元素2,元素3...) 不同元素可以是不同的数据类型
tua = (1, 2, 'a', ("z", "k", "y"))
tub = (1,)  # 元组只有一个元素，必须加逗号，否则返回唯一值的数据类型
tuc = ()  # 空元组
"""
    元组只支持查询操作，不支持增删该操作。即元组定义后不可改变，常量
    应用场景：
        1、函数的参数和返回值，如：user = (age,name)  print("%d %s" % user) 
        2、数据不可被修改
"""

# 2.字典 dict
# 基本格式：字典名 ={键1：值1，键2：值2，键3：值3...} 键值对的形式，值可以重复，但键不可用
dic = {}  # 空字典
dic = {"name": "zky", "age": "20"}
print(dic)
# 字典查看访问：变量名[键名],字典中没有下标，只能根据键访问，键名不存在报错
#            变量名.get(键名), 键名不存在时默认返回None，可设置返回值get(键名，不存在的返回值)
# 一个是查看目标地址位置的值，一个是函数返回值
print(dic["name"])
# 键可以是其他数据类型
arr = {1: "one", 2: "two"}
print(arr[1])
print(arr.get(1))
print(arr.get(0, "没有键值"))

# 字典修改元素：通过 变量[键名] = 值 修改，如果不存在键名，就新增
arr[1] = 1  # 修改
arr[0] = 0  # 新增
print(arr)

# 字典删除
# del删除整个字典：del 字典名
# 删除指定键值对：del 字典名[键值]，没有指定的键就会报错
del arr[0]
print(arr)
# clear()清空字典的键值对：字典名.clear()
arr.clear()
print(arr)
# pop()删除指定键值对：字典名.pop(键名)，不存在键和没指定键就报错
dic.pop("name")
print(dic)
# popitem()默认删除最后一个键值对
dic.popitem()
print(dic)

# 其他操作
# len()求字典长度:len(字典名)，与字符串求长度一样
dic = {"name": "zky", "age": 18, "tel": "1869666"}
print(len(dic))
# keys()返回字典里面的所以键名：字典名.keys(),返回的是dict_keys类型的数据
print(dic.keys())
# for循环取出键名
[print(i) for i in dic]
# values()返回字典里面所以值：字典名.values(),返回的是dict_values类型的数据
print(dic.values())
# for循环取出值
[print(dic[i]) for i in dic]
[print(i) for i in dic.values()]
# items()返回字典里面所有的键值对，返回的是dict_items类型的数据,键值对以元组的形式返回，有几个键值对就有几个元组
print(dic.items())
# for循环取出
[print(i) for i in dic.items()]
[print(type(i)) for i in dic.items()]

# 字典的应用场景：使用键值对存储描述一个对象的相关信息，数据字典

# 3.集合 set
# 基本格式：集合名 = {元素1,元素2，元素3...}，集合是无序的，里面的元素是唯一的，去重
collection = {1, 2, 3, "asasa", "zky"}
print(collection)
s1 = {}  # 字典
s = set()  # 空集合
print(type(s), type(s1))
# 集合的无序性， 集合元素的hash值不同，在hash表中的位置不一样，故每次运行的结果顺序不一样，但是数字（int型）的hash是他本身，顺序的一定的
s = {1, 2, 3, 4, 5, 9, 6, 8, 7}
print(s)  # {1, 2, 3, 4, 5, 6, 7, 8, 9}
print(hash(1), hash(2), hash(3))
s = {'a', 'b', 'c', 'd'}
print(s)
print(hash('a'), hash('b'), hash('c'))
# 集合唯一性，自动去重
s = {1, 2, 3, 5, 6, 3, 2, 1, 4, 5, 7, 8, 5, 6, 5, 9, 8, 5}
print(s)  # {1, 2, 3, 4, 5, 6, 7, 8, 9}

# 集合的操作：添加和删除
# add()添加一个整体,若怡存在，则不进行任何操作,一次只能添加一个元素，为整体
collection.add("zhangkuiyuan")
collection.add("zhangkuiyuan")
collection.add(("zhang", "kuiyuan"))
print(collection)
# update() 把传入的元素拆分，每一个作为独立的元素添加，只能添加可迭代对象
collection.update("zky")
print(collection)

# remove()删除指定元素，有则删除，没有则报错
collection.remove("asasa")
print(collection)
# pop()删除默认删第一个，本次运行根据hash值排序后的第一个
collection.pop()
print(collection)
# discard()选择要删除的元素，有就删，没有就不操作
collection.discard("asasa")
collection.discard("zky")
print(collection)

# 4.交集和并集
# 交集 & ，公共部分
collection1 = collection
collection2 = {"zky", "zkyuan", "z", "k", 'y', "qwer"}
print(collection1 & collection2)
# 并集 | ，合起来的部分去重
print(collection1 | collection2)
[print(str(collection1)[i]) for i in range(0,10)]
