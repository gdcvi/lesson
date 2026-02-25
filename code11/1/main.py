"""
 * @author: zkyuan
 * @date: 2026/2/25 14:27
 * @description:
"""
from student import Student


def main():
    # 创建学生对象
    zhang_san = Student("张三", [85, 92, 78])

    # 计算并打印平均分
    average_score = zhang_san.get_average()
    print(f"{zhang_san.name}的平均分是: {average_score:.2f}")


if __name__ == "__main__":
    main()
