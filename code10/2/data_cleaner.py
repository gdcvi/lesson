"""
 * @author: zkyuan
 * @date: 2026/2/25 10:10
 * @description: 数据清洗模块
 * 提供数据清洗和统计计算功能
"""


def clean_data(raw_list):
    """
    清洗原始数据列表
    
    参数:
        raw_list (list): 包含原始数据的列表，格式如 ["  Alice, 85 ", "BOB, 92", ...]
    
    返回:
        dict: 清洗后的字典，键为学生姓名，值为成绩
              格式如 {'Alice': 85, 'Bob': 92, ...}
    
    功能说明:
        1. 跳过空字符串
        2. 去除两端空格
        3. 分割姓名和成绩
        4. 标准化姓名格式（首字母大写，其余小写）
        5. 转换成绩为整数类型
        6. 返回字典格式的结果
    """
    # 存储清洗后的数据
    cleaned_data = []
    
    # 遍历原始数据
    for item in raw_list:
        # 跳过空字符串
        if item.strip() == "":
            continue
        
        # 去除两端空格
        cleaned_item = item.strip()
        
        # 分割姓名和成绩
        parts = cleaned_item.split(',')
        
        # 处理姓名：首字母大写，其他小写
        name = parts[0].strip().title()
        
        # 处理成绩：转换为整数
        score = int(parts[1].strip())
        
        cleaned_data.append((name, score))
    
    # 转换为字典格式
    score_dict = {}
    for name, score in cleaned_data:
        score_dict[name] = score
    
    return score_dict


def calculate_average(score_dict):
    """
    计算成绩字典的平均分
    
    参数:
        score_dict (dict): 成绩字典，键为学生姓名，值为成绩
    
    返回:
        float: 平均分，保留两位小数
               如果字典为空则返回0
    
    功能说明:
        1. 检查字典是否为空
        2. 提取所有成绩值
        3. 计算平均分
        4. 返回格式化的平均分
    """
    # 检查字典是否为空
    if not score_dict:
        return 0
    
    # 使用列表推导式获取所有成绩
    scores = [score for score in score_dict.values()]
    
    # 计算平均分
    average_score = sum(scores) / len(scores)
    
    return round(average_score, 2)


def find_top_student(score_dict):
    """
    找出成绩最高的学生
    
    参数:
        score_dict (dict): 成绩字典，键为学生姓名，值为成绩
    
    返回:
        tuple: (学生姓名, 最高成绩) 或 (None, 0) 如果字典为空
    
    功能说明:
        1. 检查字典是否为空
        2. 遍历找出最高分及其对应的学生
    """
    # 检查字典是否为空
    if not score_dict:
        return None, 0
    
    max_score = 0
    top_student = ""
    
    for name, score in score_dict.items():
        if score > max_score:
            max_score = score
            top_student = name
    
    return top_student, max_score


# 测试代码（当直接运行此模块时执行）
if __name__ == "__main__":
    # 测试数据
    test_data = ["  Alice, 85 ", "BOB, 92", "张魁元, 100", "david, 78", "Ella, 95", ""]
    
    # 测试数据清洗功能
    result_dict = clean_data(test_data)
    print("清洗后的字典:", result_dict)
    
    # 测试平均分计算功能
    avg_score = calculate_average(result_dict)
    print("平均分:", avg_score)
    
    # 测试找最高分学生功能
    top_name, top_score = find_top_student(result_dict)
    print(f"最高分学生: {top_name}, 成绩: {top_score}")