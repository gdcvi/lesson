"""
 * @author: zkyuan
 * @date: 2025/7/18 10:14
 * @description: 字符串 str
"""
str1: str = "字符串"
str2 = "字符串"
# 编码
"""
Unicode：所有字符都是2个字节
优点：字符和数字转换速度快
缺点：占用空间大

UTF-8：精准，不同字符用不同的长度表示
优点：节省空间
缺点：字符和数字转换速度慢，每次都需要计算字符要用多少个字节来表示

GKB
"""
# 字符编码转换
s = "hello"
print(s, type(s))  # 输出：hello <class 'str'>
# 编码
s_encode = s.encode()
print(s_encode, type(s_encode))  # 输出： b'hello' <class 'bytes'>
# 解码
s_encode_decode = s_encode.decode()
print(s_encode_decode, type(s_encode_decode))  # 输出： hello <class 'str'>
# 指定编码标准
str1 = "中文编码十六进制aaa"
encode = str1.encode(encoding="UTF-8")
print(encode)  # b'\xe4\xb8\xad\xe6\x96\x87\xe7\xbc\x96\xe7\xa0\x81\xe5\x8d\x81\xe5\x85\xad\xe8\xbf\x9b\xe5\x88\xb6aaa'
decode = encode.decode("UTF-8")
print(decode)

# 字符串拼接
print("10" + "10")  # 1010
fname = "张"
name = "三"
print(fname + name)  # 张三
print(fname, name)  # 张 三
print(fname, name, sep="")  # 张三

# 字符串重复 *
print("张起灵\t" * 10)

# 成员运算符：检查字符串中是否包含了某个子字符串
# in：包含返回True，不包含返回False
# not in：包含返回False，不包含返回True
name = "zhangkuiyuan"
print("yuan" in name)  # True
print("yuan" not in name)  # False
print("zkyuan" in name)  # False
print("zkyuan" not in name)  # True

# 字符数组
i = 0
while i < 11:
    print(name[i], end="-")
    i += 1
print()

# 字符截取切片 [开始位置:结束位置:步长]（包前不包后）
# zhangkuiyuan
# 正数：从左到右，正向 ;步长默认1
print(name[0:5])  # zhang
print(name[0:5:2])  # zag
# 负数：从右往左，反向 ；步长要指定
print(name[-1:-5:-1])  # nauy
print(name[-1:-5:-2])  # nu

# 查找元素 find()：检测某个子字符是否包含在字符串中，在则返回子字符串的开始下标，否则返回-1
# find("子字符串",开始位置,最后位置) 开始和结束可以省略
print(name.find("yuan"))  # 8
print(name.find("an", 4))  # 10
print(name.find("zh", 3))  # -1
print(name.find("an", 4, 8))  # -1

# index():检测某个子字符串是否包含在字符串中，在则返回子字符串的开始下标，否则报错
print(name.index("yuan"))  # 8
print(name.index("an", 4))  # 10
# print(name.index("zh", 3))  # 报错
# print(name.index("an", 4, 8))  # 报错

# count():返回某个子字符串出现的次数，没有就返回0
print(name.count("yuan"))  # 8
print(name.count("an", 4))  # 10
print(name.count("zh", 3))  # 0
print(name.count("an", 4, 8))  # 0

# 判断
# startswith():是否以某个字符串开头
print(name.startswith("zh"))  # True
print(name.startswith("zh", 2))  # False
# endswith():是否以某个字符串结尾
print(name.endswith("an"))  # True
print(name.endswith("an", 2, 6))  # False
# isupper():大小写检测，若全是大写返回True
print(name.isupper())  # False
print("ZHANGKUIYUAN".isupper())  # True

# 修改元素
# replace(旧字符串,新字符串,替换次数)：替换,
print(name.replace("zhangkui", "zk"))  # zkyuan
print(name.replace("a", "A"))  # zhAngkuiyuAn
print(name.replace("a", "A", 1))  # zhAngkuiyuan
# split()：指定分隔符来切分字符串,可指定分割次数
print(name.split("a"))  # ['zh', 'ngkuiyu', 'n']
# capitalize()：第一个字符大写，其他小写
print(name.capitalize())
# lower()：大写转小写
# upper()：小写转大写
