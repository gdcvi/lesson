"""
题目2：列表操作

编写一个Python程序，要求：

1. 创建一个包含数字1-10的列表
2. 使用切片获取列表中第3到第7个元素（索引从0开始）
3. 将列表反向输出
4. 在列表末尾添加数字11，然后在第2个位置插入数字0
5. 删除数字5并打印最终列表
"""
# 1. 创建列表
numbers = list(range(1, 11))
print("原始列表:", numbers)

# 2. 获取第3到第7个元素
sliced = numbers[2:7]
print("切片结果:", sliced)

# 3. 反向输出列表
reversed_list = numbers[::-1]
print("反向列表:", reversed_list)

# 4. 添加和插入元素
numbers.append(11)
numbers.insert(1, 0)
print("添加元素后:", numbers)

# 5. 删除数字5并打印最终列表
numbers.remove(5)
print("最终列表:", numbers)
