"""
 * @author: zkyuan
 * @date: 2025/8/14 15:10
 * @description: streamlit安装
"""

# streamlit官方文档：https://docs.streamlit.io/develop/api-reference

# 在python环境中安装依赖，因为这是国外的源，所以可以安装很慢，期间也可能会安装失败，出现问题可以重复执行安装多试几次，或者是开科学上网

# pip install streamlit
# 使用镜像源  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple streamlit
#           pip install -i https://mirrors.aliyun.com/pypi/simple/ streamlit
# 安装成功后，输入命令：streamlit hello 启动streamlit，这里有streamlit的一些demo案例

import streamlit as st

a, b = st.columns(2)
c, d = st.columns(2)

a.metric("Temperature", "30°F", "-9°F", border=True)
b.metric("Wind", "4 mph", "2 mph", border=True)

c.metric("Humidity", "77%", "5%", border=True)
d.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)

# 使用命令 streamlit run py1.py 启动
# 修改启动端口参数  --server.port 8080
