"""
 * @author: zkyuan
 * @date: 2026/2/25 10:15
 * @description: 主程序文件 - 使用自定义数据清洗模块
 * 演示如何导入和使用自己创建的模块
"""

# 导入自定义模块
import data_cleaner

def main():
    """主函数 - 执行完整的数据处理流程"""
    
    # 原始数据
    raw_data = ["  Alice, 85 ", "BOB, 92", "张魁元, 100", "david, 78", "Ella, 95", ""]
    
    print("=" * 50)
    print("模块化数据处理程序")
    print("=" * 50)
    print()
    
    print("原始数据:")
    print(raw_data)
    print()
    
    # 调用模块中的数据清洗函数
    print("正在清洗数据...")
    score_dict = data_cleaner.clean_data(raw_data)
    
    print("清洗后的字典格式数据:")
    print(score_dict)
    print()
    
    # 调用模块中的平均分计算函数
    print("正在计算平均分...")
    average_score = data_cleaner.calculate_average(score_dict)
    
    print(f"平均分为: {average_score}")
    print()
    
    # 调用模块中的查找最高分学生函数
    print("正在查找成绩最高的学生...")
    top_student, max_score = data_cleaner.find_top_student(score_dict)
    
    if top_student:
        print(f"成绩最高的学生是: {top_student}，成绩为: {max_score}")
    else:
        print("没有有效的学生成绩数据")
    
    print()
    print("=" * 50)
    print("程序执行完毕！")
    print("=" * 50)

# 程序入口点
if __name__ == "__main__":
    main()