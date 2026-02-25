"""
 * @author: zkyuan
 * @date: 2026/2/25 17:10
 * @description: 权限校验基础演示 - 按照题目要求的简单示例
"""


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role


# 创建当前用户对象
current_user = User('张三', 'teacher')


def require_admin(func):
    def wrapper(*args, **kwargs):
        if current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            print("权限不足！")
            return None

    return wrapper


@require_admin
def delete_student(student_id):
    return f"学生 {student_id} 已被删除"


# 测试不同角色的访问
def test_permissions():
    print("=== 权限校验测试 ===")

    # 当前是教师角色
    print(f"当前用户: {current_user.username}, 角色: {current_user.role}")
    print("1. 教师角色尝试删除学生:")
    result1 = delete_student(1001)
    print(f"结果: {result1}\n")

    # 切换到管理员角色
    current_user.role = 'admin'
    current_user.username = '管理员'
    print(f"切换后用户: {current_user.username}, 角色: {current_user.role}")
    print("2. 管理员角色尝试删除学生:")
    result2 = delete_student(1002)
    print(f"结果: {result2}\n")

    # 切换到访客角色
    current_user.role = 'guest'
    current_user.username = '访客'
    print(f"切换后用户: {current_user.username}, 角色: {current_user.role}")
    print("3. 访客角色尝试删除学生:")
    result3 = delete_student(1003)
    print(f"结果: {result3}")


if __name__ == "__main__":
    test_permissions()
