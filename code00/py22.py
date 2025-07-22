"""
 * @author: zkyuan
 * @date: 2025/7/18 10:19
 * @description: 进程
"""
import os

# 就绪态、执行态、阻塞态
# 进程语法
# multiprocessing模块提供了Process类代表进程对象
"""
    target：执行的目标任务名，即子进程要执行的任务
    args：以元组的形式传参
    kwargs：以字典的形式传参
    
    start()：开启子进程
    is_alive()：判断子进程是否活着，存活返回True，死亡返回False
    join()：主进程等待进程执行结束
    
    name：当前进程别名，默认Process-N
    pid：当前进程的进程编号
"""
from multiprocessing import Process


def sing(name):
    print(f"{name}唱歌", os.getpid(), "父进程id：", os.getppid())


def dance(name):
    print(f"{name}跳舞", os.getpid(), "父进程id：", os.getppid())


if __name__ == '__main__':
    # 创建进程
    p1 = Process(target=sing, args=("zkyuan",), name="子进程1")
    p2 = Process(target=dance, args=("zkyuan",), name="子进程2")

    # 开启进程
    p1.start()
    p1.join()
    p2.start()

    print("p1", p1.name, "pid:", p1.pid)
    print("p2", p2.name, "pid:", p2.pid)
    print("主进程id：", os.getpid())

    print("p1存活状态：", p1.is_alive())  # 阻塞一下才死亡，否则执行这里时还存活
    print("p2存活状态：", p2.is_alive())
