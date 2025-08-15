"""
 * @author: zkyuan
 * @date: 2025/8/14 16:29
 * @description: 会话状态、数据缓存
"""
import streamlit as st

# session_state是一个字典，用于存储会话状态变量。st.session_state.key = value
# session_state是临时存储
if st.button("给变量设置默认值"):
    st.session_state.chat_input = "Hello, world!"

if "chat_input" not in st.session_state:
    st.session_state.chat_input = "你好呀！"

st.chat_input(key="chat_input", placeholder="请输入...")
st.write("输入的内容:", st.session_state.chat_input)

st.chat_message("user").write(st.session_state.chat_input)
st.chat_message("AI").write(st.session_state.chat_input)
st.chat_message("zky").write(st.session_state.chat_input)

# 海象运算符（或者叫海象操作符） := 来同时赋值和判断条件。
if prompt := st.chat_input("请输入..."):
    st.chat_message("user").write(prompt)
    st.chat_message("AI").write(f"{prompt}正在思考...")
    st.chat_message("zky").write("正在思考...")
    st.chat_message("AI").write("思考完成！")
    st.chat_message("zky").write("思考完成！")


