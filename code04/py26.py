"""
 * @author: zkyuan
 * @date: 2025/7/18 10:19
 * @description: 正则表达式
"""

# 导入re模块
import re

# re.match(pattern=正则表达式,string=需要匹配的字符串,flags=)
# 从开头位置匹配
# <re.Match object; span=(开始位置, 字符个数), match=匹配结果>
re_match = re.match(pattern='.*y', string='zkyuan')
print(re_match)  # <re.Match object; span=(0, 3), match='zky'>
print(re_match.group())  # zky

res = re.match("abc|.*def", "abcdef")
print(res.group())

# 高级用法
"""
    match()：从开头开始匹配，返回第一个匹配成功的对象，通过group()提取，失败则返回None
    search()：扫描整个字符串，并返回第一个成功匹配的对象，如果失败则返回None
    findall()：从头到尾匹配，找到所有匹配成功的数据，返回一个列表
    sub(pattern=正则,repl=新内容,string=字符串,count=指定替换次数)：将正则匹配上的替换为新内容
    split(pattern=正则,string=字符串,maxsplit=最大分割次数)：在正则匹配到的地方进行分割
"""