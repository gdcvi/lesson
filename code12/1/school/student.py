"""
 * @author: zkyuan
 * @date: 2026/2/25 14:55
 * @description: Student类继承Person类，体现继承和多态思想
"""
from .person import Person


class Student(Person):
    def __init__(self, name, scores, grade=""):
        """
        初始化学生对象
        
        Args:
            name (str): 学生姓名
            scores (list): 成绩列表
            grade (str): 学生年级，默认为空字符串
        """
        # 调用父类构造函数初始化姓名
        super().__init__(name)
        self.scores = scores
        self.grade = grade

    def get_average(self):
        """
        计算并返回学生的平均成绩
        
        Returns:
            float: 平均成绩，如果成绩列表为空则返回0
        """
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)

    def add_score(self, new_score):
        """
        向学生的成绩列表中添加一个新成绩
        
        Args:
            new_score (int/float): 新的成绩分数
        """
        self.scores.append(new_score)

    def is_passing(self):
        """
        判断学生是否所有科目都及格（>=60）
        
        Returns:
            bool: 所有科目都及格返回True，否则返回False
        """
        if not self.scores:
            return False
        return all(score >= 60 for score in self.scores)

    def introduce(self):
        """
        重写父类的自我介绍方法，体现多态特性
        """
        average_score = self.get_average()
        print(f"大家好，我是学生{self.name}，我的平均分是{average_score:.2f}")
