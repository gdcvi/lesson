"""
 * @author: zkyuan
 * @date: 2025/7/18 10:18
 * @description: 文件读写
"""
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

f = open('test.txt', 'r',
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

f = open('test.txt',
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
with open("resources\\a.png", 'rb') as file:
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
