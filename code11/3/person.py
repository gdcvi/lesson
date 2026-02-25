"""
 * @author: zkyuan
 * @date: 2026/2/25 14:55
 * @description: Person基类，体现类的继承思想
"""

class Person:
    def __init__(self, name):
        """
        初始化人员对象
        
        Args:
            name (str): 人员姓名
        """
        self.name = name
    
    def introduce(self):
        """
        自我介绍方法
        """
        print(f"大家好，我是{self.name}")