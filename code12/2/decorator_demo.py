"""
 * @author: zkyuan
 * @date: 2026/2/25 16:50
 * @description: 装饰器演示 - 为函数增加日志功能
"""


def log_decorator(func):
    """
    日志装饰器函数
    接收一个函数作为参数，在不修改原函数的情况下为其添加日志功能
    
    Args:
        func: 被装饰的函数
        
    Returns:
        wrapper: 包装后的函数
    """

    def wrapper(*args, **kwargs):
        # 打印函数调用信息
        print(f"Calling function {func.__name__} with arguments {args}")
        # 调用原函数
        result = func(*args, **kwargs)
        # 打印函数结束信息和结果
        print(f"Function finished. Result: {result}")
        return result

    return wrapper


@log_decorator
def add(a, b):
    """
    计算两个数的和
    
    Args:
        a (int/float): 第一个数
        b (int/float): 第二个数
        
    Returns:
        int/float: 两数之和
    """
    return a + b


@log_decorator
def multiply(x, y):
    """
    计算两个数的乘积
    
    Args:
        x (int/float): 第一个数
        y (int/float): 第二个数
        
    Returns:
        int/float: 两数乘积
    """
    return x * y


@log_decorator
def greet(name, greeting="Hello"):
    """
    问候函数
    
    Args:
        name (str): 姓名
        greeting (str): 问候语，默认为"Hello"
        
    Returns:
        str: 完整的问候语
    """
    return f"{greeting}, {name}!"


def main():
    print("=== 装饰器功能演示 ===\n")

    print("1. 调用 add(3, 5):")
    result1 = add(3, 5)
    print(f"返回值: {result1}\n")

    print("2. 调用 multiply(4, 6):")
    result2 = multiply(4, 6)
    print(f"返回值: {result2}\n")

    print("3. 调用 greet('张三'):")
    result3 = greet('张三')
    print(f"返回值: {result3}\n")

    print("4. 调用 greet('李四', '你好'):")
    result4 = greet('李四', '你好')
    print(f"返回值: {result4}\n")

    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
