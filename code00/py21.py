"""
 * @author: zkyuan
 * @date: 2025/7/18 10:18
 * @description: 线程2
"""
import time
from threading import Thread, Lock

# 线程之间的共享资源（全局变量）
li = []


def wData():
    for i in range(5):
        li.append(i)
        time.sleep(1)
    print("write :", li)


def rData():
    print("read :", li)


a = 0
b = 1000000
lock = Lock()


def add1():
    lock.acquire()  # 上锁
    global a
    for i in range(b):
        a += 1
    print("add1的结果：", a)
    lock.release()  # 解锁


def add2():
    lock.acquire()
    global a
    for i in range(b):
        a += 1
    print("add2的结果：", a)
    lock.release()


if __name__ == '__main__':
    # 创建子线程
    t1 = Thread(target=wData)
    t2 = Thread(target=rData)

    # 开启子线程
    t1.start()

    t1.join()  # 阻塞子线程，等t1执行完再接着执行下面的代码

    t2.start()

    # 资源竞争
    one = Thread(target=add1)
    two = Thread(target=add2)

    one.start()
    two.start()

# 线程同步：阻塞，一个线程执行完，再去执行第二个线程
# 互斥锁：对共享数据进行锁定，Lock
"""
    acquire()：加锁
    release()：解锁
    必须成对出现，否则会出现死锁
    用共享资源时上锁，用完后解锁
"""
