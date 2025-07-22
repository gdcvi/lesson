# python基础语法

## 一、注释

Python中用#表示单行注释，#之后的同行的内容都会被注释掉。

```
# Python中单行注释用#表示，#之后同行字符全部认为被注释。
```

使用三个连续的双引号表示多行注释，两个多行注释标识之间内容会被视作是注释。

```
""" 与之对应的是多行注释
  用三个双引号表示，这两段双引号当中的内容都会被视作是注释
"""
```

## 二、基础变量类型与操作符

int（整数）

float（浮点数）

bool（布尔）

str（字符串）

tuple（元组）

list（列表）

dict（字典）

set（集合）

None（空）

bytes（二进制类型）

### 1、算术运算

``` 
1 + 1   # > 2   加法
8 - 1   # > 7   减法
10 * 2  # > 20  乘法
35 / 5  # > 7.0 除法
int(35 / 5) # > 7 强制类型转换
10 / 3  # > 3.3333333333333335 除法
10 // 3 # > 3 除法取整
10 % 3  # > 1 除法取余数
2**3  # > 8 乘方
```

### 2、逻辑运算

- 是、否

    ```
    True   # 是
    False  # 否
    not True # 否
    not False # 是
    True and False # 否
    True or False  # 是
    ```

- 大于、小于

    ```
    1 == 1  # 是
    2 == 1  # 否
    1 > 2  # 否
    1 < 2  # 是
    1 >= 1 # 是
    1 <= 2 # 是
    1 != 2 # 是
    ```

- and、or

  ```
  1 < 2 and 2 < 3  # 是
  2 < 3 and 3 < 2  # 否

  1 < 2 or 2 < 3  # 是
  2 < 3 or 3 < 2  # 是
  ```
  
  ### 3、list和字符串
  
  ```
  a = [1,2,3,4] 
  b = a             
  b is a  # 是
  b == a  # 是
  b = [1,2,3,4]
  b is a  # 否  引用类型
  b == a  # 是  值类型
  ```
  
  ```
  s1 = "这是字符串1"
  s2 = '这是字符串2'
  s3 = """这是字符串3
  这是第二行"""
  
  len(s1+s2)  # 字符串长度12 
  print(f"s1+s2的长度为：{len(s1+s2)}") # s1+s2的长度为：12
  ```
  
## 三**、变量与集合**

### 1、输入input、输出print

```
print("hello world")

s = input("请输入")
print(s)

```

### 2、变量

```
a = 100  # 申明
print(a)
```

```
# 三元表达式
s = "hello world" if 3 > 1 else "no hello"
print(s)

s2 = "hello world" if 3 > 4 else "no hello"
print(s2)
```

```
if 3 > 1:
	return "hello world"
else:
	return "no hello"
```

### 3、list列表

```
l1 = []
l2 = [1,2,3]

l1.append(1)  # [1]
l1.append(2)  # [1,2]  加在后面

l1.append(1)  # [2]
```

```
li = [1,2,3,4,5,6]
li[0] # 1
li[1] # 2
li[5] # 6
```

切片取数[start:end]，**左闭右开区间**

[1:5:2]表示从1号位置开始，5号位置为止，步长为2获取元素

``` 
li[1:3] # [2,3]  1到3
li[1:]  # [2, 3, 4, 5, 6]  1到最后
li[:3]  # [1, 2, 3]  开头到3
li[::-1] # 反向遍历 [6, 5, 4, 3, 2, 1]
```

```
del li[0] # 删除
li.remove(2) # 删除数据2

li.insert(0,2) # 在0号位置插入元素2

1 in li # 判断1是否在列表中 False
```

### 4、tuple元组

元组是不可变对象，一旦生成不可改变。元组只有一个元素时，末尾要加逗号

```
tup = (1,2,3)
tup2 = (1,)

tup[0] # 1
```

### 5、dict字典

键值对，key:value

```
dic = {"1":"one", "2":"two"}

dic["1"] # 取出键为1的值

"1" in dic  # 判断1是否为键，判断键为1是否存在

dic["3"] = "three"  # 添加新的键值对，如果已有就替换更新
```

### 6、set集合

集合的元素不可重复

```
set1 = {1,1,2,2,3,3,4}
print(set1) # {1, 2, 3, 4}
```

## **四、控制流和迭代**

### 1、判断语句

```
if a >1:
	print(a>1)
else:
	print(a不>1)
```

```
if a>1:
	print(a>1)
elif a=1:
	print(a=1)
else:
	print(a<1)
```

### 2、循环

for和 while

```
for i in [1,2,3]:
	print(i)
```

```
for i in range(4): # range表示自然数序列，从0开始
	print(i)
```

```
x = 0
while x<4:
	print(x)
	x+=1
```

### 3、异常捕获

```python
try:
    # 代码出现异常
    raise IndexError("This is an index error")
except IndexError as e:
    print("异常捕获")
finally:
    print("finally")
```

### 4、with

文件操作，使用with不用手动关闭

### 5、函数

```
def add(x,y):
	return x + y
```

```

# 调用函数：函数名(实参1，实参2...)
# 函数返回值 return（执行return函数结束），没有返回值默认为None，多个返回值为元组的形式返回

# 参数
# 必备参数（位置参数）：传递和定义参数的顺序及个数必须一致
def fun1(parameter1, parameter2):
    print("fun1函数体：")


fun1(1, 2)


# 默认参数：为参数提供默认值，调用函数可以不穿该参数的值（所有位置参数必须出现在默认参数前面）
def fun2(parameter1, parameter2, a=1):
    print("fun2函数体:")


fun2(1, 2)


# 可变参数：*args，传入的值的数量是可以改变的，可以传多个，也可以不传
def fun3(*args):
    print("fun3函数体：")


fun3()


# 关键字参数：**keyWordsArgs,实参使用键值对的形式(变量名=值)，以字典的形式接收
def fun4(**kwargs):
    print("fun4函数体：")
    print(kwargs)


fun4(name="zky", age="18")
```

## 五、类

```
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
```

```
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

```

## 六、文件读写

```
# 打开、读写、关闭
# 文件对象的方法
"""
    open()：创建一个file对象，默认是以只读打开
            第一个参数是文件路径+文件名，第二个参数是访问模式，第三个参数是编码方式
    read(n)：n表示从文件中读取的数据长度，没有传n就是默认一次性读所有内容
    write()：将指定内容写入文件
    close()：关闭文件
    readline()：一次读一行，执行完文件指针移到下一行
    readlines()：按行的方式把文件内容一次性读取，返回的是一个列表，每行数据作为一个列表元素
"""
# 文件对象的属性
"""
    文件名.name：返回要打开的文件的文件名，可以包含文件的具体路径
    文件名.mode：返回文件的访问模式
                r :读，只读
                r+:读写，文件不存在就会报错
                w :写，先清空，再写入；不存在就创建新文件
                w+:写读，先写再读。文件存在就编辑，先清空，再写入；不存在就创建
                a :追加模式，不存在就创建新文件写入，存在则在原有内容追加新内容
                a+:
                rb：二进制读
                wb:二进制写
    文件名.closed：检测文件是否关闭，关闭就返回True
"""

# 打开文件

f = open('E:\\code\\GitWork\\python_study\\py1\\test.txt', 'r',
         encoding='utf-8')  # SyntaxWarning: invalid escape sequence '\c' 单斜杠要换成双斜杠
print(f.name)
print(f.mode)
# print(f.read())  # 设置读取的长度
result = ''
while True:
    text = f.readline()  # 读取一行
    if not text:
        break
    result = result + text
print(result)
f.close()  # 有打开就要有关闭，成对出现

f = open('E:\\code\\GitWork\\python_study\\py1\\test.txt',
         encoding='utf-8')

text = f.readlines()
print(text)
print(type(text))

f.close()
del f

f = open("test01.txt", 'w+', encoding='utf-8')
f.write("zhang\nzkyuan\n这是写文件aaa")
f.close()

# 文件指针：标记从哪个位置开始操作
"""
    tell()：显示文件指针当前位置
    seek(offset,whence)：移动文件读取指针到指定位置
                        offset：偏移量
                        whence：起始位置，表示移动字节的参考位置，默认是0代表开头，1代表当前位置，2代表末尾位置
    seek(0,0)：指针移动到开头位置
"""

# with open：代码执行完系统自动调用close关闭文件
with open("test01.txt", 'r+', encoding='utf-8') as file:
    print(file.read())

# 图片复制 rb模式
"""
    1、读图片，二进制
    2、写图片，二进制
    不要encoding
"""
with open("E:\\code\\GitWork\\python_study\\py1\\resources\\a.png", 'rb') as file:
    readImg = file.read()

with open("p.png", 'wb') as file:
    file.write(readImg)

# 文件目录操作
# 导入模块 os
import os

# 文件重命名
os.rename("p.png", "p2.png")

# 删除文件
os.remove("p2.png")

# 创建文件夹
os.mkdir("zzz")

# 删除文件夹
os.rmdir("zzz")

# 获取当前目录
os.getcwd()

# 获取目录列表
os.listdir()  # 获取当前目录列表
os.listdir("../")  # 获取上级目录列表

```



