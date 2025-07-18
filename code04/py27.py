"""
 * @author: zkyuan
 * @date: 2025/7/18 10:19
 * @description: os、sys、time、logging、random模块
"""
import os

# os模块：用于和操作系统进行交互
"""
    os.name:指示正在使用的工作平台（返回操作系统类型）
    os.getenv：读取环境变量
    os.path.split()：把目录名和文件名分离，以元组形式接收，第一个是目录路径，第二个是文件名
    os.path.dirname()：显示split分割的第一个元素，即目录
    os.path.basename()：显示split分割的第二个元素，即文件名
    os.path.exists()：判断路径是否存在
    os.path.isfile()：判断路径是否是文件
    os.path.isdir()：判断路径是否是目录
    os.path.abspath()：获取当前路径下的绝对路径
    os.path.isabs()：判断是否是绝对路径
"""
print(os.name)
print(os.getenv("path"))
# r"" 原生字符串取消转义
print(os.path.split(r"E:\code\GitWork\python_study\py1\py27.py"))
print(os.path.exists(r"E:\code\GitWork\python_study\py1\py270.py"))
print(os.path.isfile(r"E:\code\GitWork\python_study\py1\py27.py"))
print(os.path.isdir(r"E:\code\GitWork\python_study\py1"))
print(os.path.abspath("py27.py"))
print(os.path.isabs(r"E:\code\GitWork\python_study\py1\py27.py"))

# sys模块:负责程序跟python解释器的交互
import sys

"""
    sys.getfilesystemencoding():获取系统默认编码格式
    sys.path:获取环境变量路径，跟解释器相关；以列表形式返回，第一项为当前工作目录
    sys.platform：获取操作系统平台名称
    sys.version：获取python解释器版本信息
"""
print(sys.getfilesystemencoding())
print(sys.path)
print(sys.platform)
print(sys.version)

# time模块：程序中的时间
import time

"""
    timestamp：时间戳
    format_time：格式化时间
    struct_time：时间元组
    
    time.sleep()：程序睡眠，以秒为单位
    time.time():获取当前的时间戳，秒为单位，从1970.1.1 00:00:00开始到现在的时间差
    time.localtime()：将一个时间戳转换为当前时区的struct_time
    time.asctime()：获取系统当前时间
    time.ctime()：获取系统当前时间，把时间戳转换成固定的字符串表达式
    time.strftime()：格式化时间，将struct_time转换为指定格式
    time.strptime()：将时间字符串转换成struct_time时间元组
"""
time.sleep(1)
print(time.time())
print(time.localtime())
print(time.localtime().tm_year)  # 查看是哪一年
print(time.asctime())
print(time.ctime())

# logging模块：记录日志信息
import logging

"""
由高到低：
    critical
    error
    warning
    info
    debug
    notest
"""
# 设置一个日志文件，中文会乱码。filemode:打开方式，默认是a追加;level:最低级别;format:输出格式
logging.basicConfig(filename='log.log', filemode='w', level=logging.NOTSET,
                    format='%(levelname)s:%(asctime)s\t%(message)s')

logging.debug("debug")
# 只会显示级别大于等于warning的信息
logging.warning("warning")

# ramdom模块：随机模块，生成随机数
import random

"""
    random.random()   生成0-1之间的小数
    random.uniform(1, 3)   产生指定范围的随机小数
    random.randint(1, 5)   产生指定范围的整数，包括开头和结尾
    random.randrange(start=开头,stop=结尾,step=步长) 产生随机步长的随机数
"""
