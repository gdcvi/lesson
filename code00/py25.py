"""
 * @author: zkyuan
 * @date: 2025/7/18 10:19
 * @description: 协程2
"""
import time

import gevent

# 安装模块：pip install gevent
# gevent ：遇到IO操作时，会进行自动切换，属于主动切换
# 文件命名不要与第三方库文件冲突

"""
gevent.spawn(函数名)：创建协程对象
genent.sleep()：耗时操作,此时会自动切换
gevent.join()：阻塞，等待协程执行结束
gevent.joinall()：等待所有协程执行结束，参数是一个协程对象
"""


def sing():
    print("唱歌")
    # time.sleep(2)
    gevent.sleep(2)
    print("唱歌结束")


def dance():
    print("跳舞")
    # time.sleep(3)
    gevent.sleep(3)
    print("跳舞结束")


from gevent import monkey

monkey.patch_all()  # 将用到的time.sleep()代码替换成gevent里面的自己实现耗时操作的gevent.sleep()


def song(name):
    for i in range(3):
        # gevent.sleep(1)
        time.sleep(1)
        print(f"{name}在唱歌，第{i}次")


if __name__ == '__main__':
    g1 = gevent.spawn(sing)
    g2 = gevent.spawn(dance)

    g1.join()  # 等待g1执行结束
    g2.join()
    gevent.joinall(
        [
            gevent.spawn(song("zzz")),
            gevent.spawn(song("kkk"))
        ]
    )
"""
线程是CPU调度的基本单位，进程是资源分配的基本单位

进程：切换需要的资源最大，效率最低
线程：切换需要的资源一般，效率一般
协程：切换需要的资源最小，效率最高

多线程适合IO密集的操作（文件、爬虫）
多进程适合CPU密集的操作（科学、计算、视频解码、计算圆周率）

"""