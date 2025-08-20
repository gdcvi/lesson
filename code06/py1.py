"""
 * @author: zkyuan
 * @date: 2025/8/18 10:47
 * @description: chatgpt
 首先新建一个文件 名为:  .env
 在里面配置api_key：
# 代理的chatgpt
OPEN_API_KEY="hk-zuxxf41......d7edf186f"

# 通义千问
DASHSCOPE_API_KEY="sk-955......e33d14e1e"

# deepseek
DEEPSEEK_API_KEY="sk-a3c609......29393f34"

# 智普
ZHIPUAI_API_KEY="ccbda373f......eDL4T4VBdfPCcgE"

# 百度千帆
QIANFAN_API_KEY="bce-v3/ALTAK-pqT2J......35a26a18f85c0ba9bb498"
"""

import os
# pip install python-dotenv
from dotenv import load_dotenv
# pip install langchain
# pip install langchain_openai
# 下载国外资源安装较慢
from langchain_openai import ChatOpenAI


load_dotenv()

model = ChatOpenAI(
    model_name="gpt-4o",
    # gpt代理配置
    base_url='https://api.openai-hk.com/v1/',
    api_key=os.getenv("OPEN_API_KEY")
)

messages = "你好，你是谁?"

print(model.invoke(messages))
