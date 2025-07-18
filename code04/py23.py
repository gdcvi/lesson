"""
 * @author: zkyuan
 * @date: 2025/7/18 10:19
 * @description: 进程2
"""
import time

# 进程程之间不共享资源（全局变量）

# 进程通信，通过队列实现
"""
Queue队列
    put():放入数据
    get()：取出数据
    empty()：判断队列是否为空
    qsize()：返回当前队列包含的消息数量
    full():判断队列是否满了
"""
# from queue import Queue #这个不支持多线程
from multiprocessing import Process,Queue

# q = Queue(3)  # 最多可以接收三条消息，没写或是负值表示没有上线
# q.put("zzz")
# q.put("kkk")
# q.put("yyy")
# print(q.get())  # 获取队列中的消息，并从队列中移除
# print(q.get())
# print(q.empty())
# print(q.qsize())
# print(q.full())

li = ["zhang", "kkkk", "zkyuan"]


def wData(q):
    for i in li:
        print("写入的数据是：", i)
        q.put(i)
        time.sleep(1)


def rData(q):
    while True:
        if q.empty():
            break
        else:
            print("取出的数据：", q.get())


if __name__ == '__main__':
    q = Queue(3)

    p1 = Process(target=wData, args=(q,))
    p2 = Process(target=rData, args=(q,))

    p1.start()
    p1.join()
    p2.start()
