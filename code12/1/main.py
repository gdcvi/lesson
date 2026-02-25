"""
 * @author: zkyuan
 * @date: 2026/2/25 15:55
 * @description: 测试school包的功能 - 演示包的使用方式
"""
from school import Person as PersonFromInit
# 方式3：通过包的__init__.py直接导入（推荐）
from school import Student as StudentFromInit
from school import person
# 方式1：从包中导入整个模块
from school import student
from school.person import Person
# 方式2：从包的模块中直接导入类
from school.student import Student


def main():
    print("=== 学校包使用演示 ===\n")

    print("1. 使用方式1 - 从包中导入模块:")
    student1 = student.Student("张三", [88, 92, 76], "高一")
    person1 = person.Person("张老师")

    print("学生:", end=" ")
    student1.introduce()
    print("老师:", end=" ")
    person1.introduce()

    print("\n" + "=" * 50 + "\n")

    print("2. 使用方式2 - 直接从模块导入类:")
    student2 = Student("李四", [95, 87, 91], "高二")
    person2 = Person("李老师")

    print("学生:", end=" ")
    student2.introduce()
    print("老师:", end=" ")
    person2.introduce()

    print("\n" + "=" * 50 + "\n")

    print("3. 使用方式3 - 通过包的__init__.py导入（推荐）:")
    student3 = StudentFromInit("王五", [78, 85, 82], "高三")
    person3 = PersonFromInit("王老师")

    print("学生:", end=" ")
    student3.introduce()
    print("校长:", end=" ")
    person3.introduce()

    print("\n" + "=" * 50 + "\n")

    # 演示包的信息
    print("4. 包信息展示:")
    import school
    print(f"包版本: {school.__version__}")
    print(f"包作者: {school.__author__}")
    print(f"可导出内容: {school.__all__}")


if __name__ == "__main__":
    main()
