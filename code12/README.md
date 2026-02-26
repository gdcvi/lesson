## 任务一：构建自己的包——创建一个“学校”包
将我们上节课创建的模块，组织成一个结构清晰的包。
1. 在项目目录下创建一个名为 school 的文件夹（即包）。
2. 在该文件夹中创建一个空的 __init__.py 文件，告诉Python这是一个包。
3. 将之前的 person.py 和 student.py 文件移动到 school 文件夹中。
4. 修改 student.py 中的导入语句，使其能从同一包中导入 Person（from .person import Person）。这里的点.表示当前包。
5. 创建一个新的主程序文件 main.py，在与 school 包同级的目录下。
6. 在 main.py 中，使用 from school import student 或 from school.student import Student 来导入并使用Student类。

## 任务二：初识装饰器——为函数增加“日志”功能
假设我们有一个简单的函数，用于计算两个数的和。现在我们想在不修改这个函数的前提下，记录下每次函数被调用时的输入参数和输出结果。
1. 定义一个简单的函数 add(a, b)，返回两数之和。
2. 定义一个装饰器函数 log_decorator(func)。它接收一个函数作为参数，内部定义一个wrapper函数，在wrapper中先打印“Calling function XXX”，然后调用原函数func，再打印“Function finished.”，最后返回结果。
3. 使用“语法糖”@log_decorator来装饰add函数。
4. 调用add函数，观察输出。
```python
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
```
## 任务三：实战应用——使用装饰器进行权限校验
结合面向对象的知识，为一个“班级管理系统”添加权限校验功能。假设只有特定角色的用户才能执行删除学生信息的操作。
1. 定义一个简单的 User 类，有 username 和 role (如 'admin' 或 'teacher') 属性。
2. 创建一个当前用户对象 current_user = User('张三', 'teacher')。
3. 定义一个装饰器 require_admin(func)，它检查一个全局的 current_user 的 role 是否为 'admin'。如果是，则执行函数；如果不是，则打印“权限不足！”。
4. 定义一个函数 delete_student(student_id)，用 @require_admin 装饰它。
5. 尝试以不同角色的用户身份调用 delete_student，观察结果。