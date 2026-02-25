"""
 * @author: zkyuan
 * @date: 2026/2/25 14:55
 * @description: 测试类的继承和多态特性
"""
from person import Person
from student import Student


def main():
    print("=== 类的继承与多态演示 ===\n")
    
    # 创建Person对象
    person1 = Person("李老师")
    print("1. Person对象的自我介绍:")
    person1.introduce()
    
    print("\n" + "="*40 + "\n")
    
    # 创建Student对象
    student1 = Student("张三", [85, 92, 78], "大一")
    print("2. Student对象的自我介绍:")
    student1.introduce()
    
    print("\n" + "="*40 + "\n")
    
    # 演示继承的属性和方法
    print("3. 继承特性演示:")
    print(f"学生姓名: {student1.name}")  # 继承自Person类
    print(f"所在年级: {student1.grade}")
    print(f"成绩列表: {student1.scores}")
    
    # 使用Student特有的方法
    average = student1.get_average()
    print(f"平均分: {average:.2f}")
    
    passing_status = "及格" if student1.is_passing() else "不及格"
    print(f"整体状态: {passing_status}")
    
    print("\n" + "="*40 + "\n")
    
    # 多态演示 - 同样的方法调用，不同的行为
    print("4. 多态演示:")
    print("调用不同对象的introduce()方法:")
    
    # 将不同类型的对象放在同一个列表中
    people = [person1, student1]
    
    for i, person in enumerate(people, 1):
        print(f"\n对象{i} ({type(person).__name__}):")
        person.introduce()  # 同样的方法调用，但表现出不同的行为
    
    print("\n" + "="*40 + "\n")
    
    # 添加新成绩并再次展示
    print("5. 动态行为演示:")
    student1.add_score(95)
    print("添加新成绩95后:")
    student1.introduce()  # 重写的introduce方法会显示更新后的平均分


if __name__ == "__main__":
    main()