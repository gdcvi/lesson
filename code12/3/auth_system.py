"""
 * @author: zkyuan
 * @date: 2026/2/25 17:05
 * @description: 权限校验装饰器 - 班级管理系统权限控制
"""


class User:
    """用户类"""

    def __init__(self, username, role):
        """
        初始化用户对象
        
        Args:
            username (str): 用户名
            role (str): 用户角色 ('admin' 或 'teacher')
        """
        self.username = username
        self.role = role

    def __str__(self):
        return f"User(username='{self.username}', role='{self.role}')"


# 全局当前用户变量
current_user = None


def require_admin(func):
    """
    管理员权限装饰器
    检查当前用户是否有管理员权限
    
    Args:
        func: 被装饰的函数
        
    Returns:
        wrapper: 包装后的函数
    """

    def wrapper(*args, **kwargs):
        # 检查是否有当前用户
        if current_user is None:
            print("错误：未设置当前用户！")
            return None

        # 检查用户角色
        if current_user.role == 'admin':
            print(f"[权限验证] 用户 '{current_user.username}' 具有管理员权限")
            return func(*args, **kwargs)
        else:
            print(f"[权限拒绝] 用户 '{current_user.username}' 权限不足！需要管理员权限")
            return None

    return wrapper


@require_admin
def delete_student(student_id):
    """
    删除学生信息函数（需要管理员权限）
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        str: 操作结果信息
    """
    print(f"正在删除学生ID为 {student_id} 的学生信息...")
    return f"学生ID {student_id} 的信息已成功删除"


@require_admin
def add_student(name, grade):
    """
    添加学生信息函数（需要管理员权限）
    
    Args:
        name (str): 学生姓名
        grade (str): 学生年级
        
    Returns:
        str: 操作结果信息
    """
    print(f"正在添加学生 '{name}' 到 {grade} 年级...")
    return f"学生 '{name}' 已成功添加到 {grade} 年级"


def switch_user(user):
    """
    切换当前用户
    
    Args:
        user (User): 要切换到的用户对象
    """
    global current_user
    current_user = user
    print(f"已切换到用户: {user}")


def main():
    print("=== 班级管理系统权限校验演示 ===\n")

    # 创建不同角色的用户
    admin_user = User('张管理员', 'admin')
    teacher_user = User('李老师', 'teacher')
    guest_user = User('访客', 'guest')

    print("1. 使用教师角色尝试删除学生:")
    switch_user(teacher_user)
    result1 = delete_student(1001)
    print(f"操作结果: {result1}\n")

    print("2. 使用管理员角色删除学生:")
    switch_user(admin_user)
    result2 = delete_student(1002)
    print(f"操作结果: {result2}\n")

    print("3. 使用访客角色尝试添加学生:")
    switch_user(guest_user)
    result3 = add_student('王小明', '高一')
    print(f"操作结果: {result3}\n")

    print("4. 使用管理员角色添加学生:")
    switch_user(admin_user)
    result4 = add_student('赵小红', '高二')
    print(f"操作结果: {result4}\n")

    print("5. 测试未设置用户的情况:")
    global current_user
    current_user = None
    result5 = delete_student(1003)
    print(f"操作结果: {result5}\n")

    print("=== 权限校验演示完成 ===")


if __name__ == "__main__":
    main()
