"""
题目5：文件操作

编写一个Python程序，要求：

1. 使用代码创建一个名为"poem.txt"的文件
2. 写入两行诗句："白日依山尽，黄河入海流。\n欲穷千里目，更上一层楼。"
3. 读取文件内容并打印
4. 统计文件中的字符数
5. 将文件重命名为"唐诗.txt"
"""
import os

# 1. 创建并写入文件
with open("poem.txt", "w", encoding="utf-8") as f:
    f.write("白日依山尽，黄河入海流。\n")
    f.write("欲穷千里目，更上一层楼。")

# 2. 读取文件内容
with open("poem.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("文件内容:")
    print(content)

# 3. 统计字符数
char_count = len(content)
print(f"文件字符数: {char_count}")

# 4. 重命名文件
os.rename("poem.txt", "唐诗.txt")
print("文件已重命名为'唐诗.txt'")
