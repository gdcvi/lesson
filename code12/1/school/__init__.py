"""
学校包 - 包含人员和学生相关的类
此包用于演示Python面向对象编程中的继承和多态概念
"""

# 导出主要的类，方便外部直接导入
from .person import Person
from .student import Student

__all__ = ['Person', 'Student']
__version__ = '1.0.0'
__author__ = 'zkyuan'
