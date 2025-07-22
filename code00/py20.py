"""
 * @author: zkyuan
 * @date: 2025/7/18 10:18
 * @description: 线程1
"""

import time


# 单线程示例
def speak():
    print("我要开始睡觉了！")
    time.sleep(2)
    print("睡醒了！")


def play():
    print("我要开始学习了！")
    time.sleep(2)
    print("学习完了")


# 从上往下执行
# speak()
# play()

# 多线程
# 使用threading模块里面的Thread类创建实例对象，然后通过start启动
"""
    group：线程组
    target：执行的目标的任务名
    args：以元组的方式给执行任务进行传参
    *args：传任意多个参数
    kwargs：以字典形式传参
    name：线程名
"""
import threading

"""
    1、导入模块
    2、创建子线程Thread()类
    3、守护线程setDaemon，设置守护线程时，主线程执行完了，子线程也会跟着结束
    4、启动子线程start()
    5、阻塞线程join()；a.join(),a为子线程，阻塞主线程时，主线程会等待子线程a执行完再执行下面的代码
"""

# 程序文件执行入口
"""
if __name__ == '__main__':
    for i in range(4):
        t = threading.Thread(target=speak)
        t.start()
"""
# 创建子线程
t1 = threading.Thread(target=speak)
t2 = threading.Thread(target=play)
"""
简化：
from threading import Thread
t1 = Thread(target=speak)
"""

# 设置守护线程
"""
旧版
t1.setDaemon(True)
t2.setDaemon(True)
"""
# python3.12
t1.daemon = True
t2.daemon = True

# 启动子线程
t1.start()
t2.start()

# 修改线程名字
# 旧版：setName getName
t1.name = "线程1"
print(t1.name)

print("这是主线程")  # 这里主线程执行完了，子线程也会跟着结束

# 阻塞子线程
t1.join()  # 主线程等待子线程t1执行完再执行
t2.join()


