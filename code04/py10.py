"""
 * @author: zkyuan
 * @date: 2025/7/18 10:15
 * @description: 模块
"""
# 一个.py文件就是一个模块，导入模块就是导入一个py文件
# 1、内置模块
# 2、第三方模块（第三方库） cmd窗口命令
"""
    pip list 
    pip uninstall
    pip install 模块名
"""
# 3、自定义模块

# 导入模块方式1：
# import 模块名
# import 模块名1, 模块名2...
# 调用方式：
# 模块名.功能名（函数名）
import test

test.funTest()

# 导入模块方式2：
# from 模块名 import 函数名1,函数名2...
# from test import funTest
# 调用方式：
# 功能名（函数名）
# funTest()

# 导入模块方式3：
# from 模块名 import * （全部导入，少用，会有命名冲突的错误）
# 调用方式：函数名()

# 调用模块取别名
import test as pyt

pyt.funTest()

# 给功能取别名
# from 模块名 import 函数名1 as 别名1,函数名2 as 别名2...
from test import funTest as fun

fun()

# 内置全局变量 __name__
# if __name__ == "__main__":
# 私有的private，被别的文件导入时，不会被别的文件使用
