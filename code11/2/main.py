"""
 * @author: zkyuan
 * @date: 2026/2/25 14:45
 * @description: 测试增强版Student类
"""
from student import Student


def main():
    # 创建学生对象，包含年级信息
    zhang_san = Student("张三", [85, 92, 78], "大一")
    
    # 显示基本信息
    print(f"学生姓名: {zhang_san.name}")
    print(f"所在年级: {zhang_san.grade}")
    print(f"初始成绩: {zhang_san.scores}")
    
    # 计算并打印平均分
    average_score = zhang_san.get_average()
    print(f"{zhang_san.name}的平均分是: {average_score:.2f}")
    
    # 添加新成绩
    zhang_san.add_score(95)
    print(f"\n添加新成绩95后:")
    print(f"更新后的成绩: {zhang_san.scores}")
    
    # 检查是否所有科目都及格
    is_all_passing = zhang_san.is_passing()
    if is_all_passing:
        print(f"{zhang_san.name}所有科目都及格！")
    else:
        print(f"{zhang_san.name}有不及格的科目。")
    
    # 再次计算平均分
    new_average = zhang_san.get_average()
    print(f"更新后的平均分: {new_average:.2f}")


if __name__ == "__main__":
    main()
