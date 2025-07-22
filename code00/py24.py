"""
 * @author: zkyuan
 * @date: 2025/7/18 10:19
 * @description: 协程
"""

# 协程，微线程，单线程下的开发，单线程切换任务
# io操作多时可以用协程

# 安装模块：pip install greenlet
# 卸载模块：pip uninstall 模块名

# greenlet是一个由C语音实现的协程模块，通过设置switch()来实现任意函数之间的切换
# greenlet属于手动切换，遇到IO操作时，程序会阻塞，不能自动切换

from greenlet import greenlet


def sing():
    print("唱歌")
    g2.switch()
    print("唱歌结束")


def dance():
    print("跳舞")
    print("跳舞结束")
    g1.switch()


if __name__ == '__main__':
    g1 = greenlet(sing)
    g2 = greenlet(dance)

    g1.switch()  # 切换到g1中去运行
    g2.switch()


