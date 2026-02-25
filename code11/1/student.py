"""
 * @author: zkyuan
 * @date: 2026/2/25 14:27
 * @description:
"""


class Student:
    def __init__(self, name, scores):
        """
        初始化学生对象
        
        Args:
            name (str): 学生姓名
            scores (list): 成绩列表
        """
        self.name = name
        self.scores = scores

    def get_average(self):
        """
        计算并返回学生的平均成绩
        
        Returns:
            float: 平均成绩，如果成绩列表为空则返回0
        """
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)
