"""
 * @author: zkyuan
 * @date: 2026/2/25 9:55
 * @description:
"""

import subprocess
import sys
import threading
import time
import webbrowser


def run_streamlit():
    """运行Streamlit应用"""
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])


def open_browser():
    """在延迟后打开浏览器"""
    time.sleep(3)  # 等待Streamlit服务器启动
    webbrowser.open("http://localhost:8501")


if __name__ == "__main__":
    print("启动图书管理系统...")
    print("正在启动Streamlit服务器...")

    # 在另一个线程中打开浏览器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()

    # 运行Streamlit应用
    run_streamlit()
