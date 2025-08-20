"""
 * @author: zkyuan
 * @date: 2025/8/18 15:39
 * @description: qwen
"""

import os

from dotenv import load_dotenv

# 使用openai接口标准
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model="qwen-plus",
    # deepseek
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

messages = "你好，你是谁?"

print(model.invoke(messages))

print("------------------------------------分割线----------------------------------------")

# 使用tongyi接口
# pip install langchain-community
# pip install dashscope
from langchain_community.chat_models.tongyi import ChatTongyi

model2 = ChatTongyi(
    model="qwen-max",
    streaming=True,
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
print(model2.invoke(messages))