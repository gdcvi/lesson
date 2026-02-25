"""
 * @author: zkyuan
 * @date: 2026/2/25 11:10
 * @description: 主程序文件 - 使用Python标准库增强功能
 * 演示random和statistics模块的使用
"""

# 导入自定义模块
import data_cleaner
# 导入Python标准库模块
import random
import statistics

def main():
    """主函数 - 执行完整的数据处理流程，包含标准库功能"""
    
    # 原始数据
    raw_data = ["  Alice, 85 ", "BOB, 92", "张魁元, 100", "david, 78", "Ella, 95", ""]
    
    print("=" * 60)
    print("模块化数据处理程序 - Python标准库增强版")
    print("=" * 60)
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
    
    # ========== 新增功能1: 使用random模块随机抽取幸运学生 ==========
    print("🎲 正在抽取幸运学生...")
    if score_dict:
        # 使用random.choice()从字典的键中随机选择
        lucky_student = random.choice(list(score_dict.keys()))
        lucky_score = score_dict[lucky_student]
        print(f"🎉 幸运学生是: {lucky_student}，成绩为: {lucky_score}")
    else:
        print("❌ 没有学生数据可供抽取")
    print()
    
    # ========== 新增功能2: 使用statistics模块计算平均分 ==========
    print("📊 正在使用statistics模块计算平均分...")
    if score_dict:
        # 获取所有成绩值
        scores_list = list(score_dict.values())
        print(f"成绩列表: {scores_list}")
        
        # 使用statistics.mean()计算平均分
        stats_average = statistics.mean(scores_list)
        print(f"statistics.mean() 计算的平均分: {stats_average:.2f}")
        
        # 使用自定义函数计算平均分
        custom_average = data_cleaner.calculate_average(score_dict)
        print(f"自定义函数 calculate_average() 计算的平均分: {custom_average}")
        
        # 对比验证结果 （ < 0.01 避免浮点数的误判）
        if abs(stats_average - custom_average) == 0:
            print("✅ 验证通过：两种方法计算结果一致！")
        else:
            print("❌ 验证失败：两种方法计算结果不一致！")
    else:
        print("❌ 没有成绩数据可供计算")
    print()
    
    # 调用模块中的查找最高分学生函数
    print("🏆 正在查找成绩最高的学生...")
    top_student, max_score = data_cleaner.find_top_student(score_dict)
    
    if top_student:
        print(f"成绩最高的学生是: {top_student}，成绩为: {max_score}")
    else:
        print("没有有效的学生成绩数据")
    
    print()
    print("=" * 60)
    print("程序执行完毕！")
    print("=" * 60)

# 程序入口点
if __name__ == "__main__":
    main()