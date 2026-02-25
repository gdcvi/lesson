"""
 * @author: zkyuan
 * @date: 2026/2/25 16:55
 * @description: 装饰器基础演示 - 按照题目要求的简单示例
"""


def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__} with arguments {args}")
        result = func(*args, **kwargs)
        print(f"Function finished. Result: {result}")
        return result

    return wrapper


@log_decorator
def add(a, b):
    return a + b


# 调用 add(3, 5)
result = add(3, 5)
print(f"最终返回值: {result}")
