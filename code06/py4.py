"""
 * @author: zkyuan
 * @date: 2025/8/18 16:25
 * @description: 智普
"""
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model='glm-4-plus',
    api_key=os.getenv("ZHIPU_API_KEY"),
    # 智普
    base_url='https://open.bigmodel.cn/api/paas/v4/'
)

messages = "你好，你是谁?"

print(model.invoke(messages))

print("------------------------------------分割线----------------------------------------")

# pip install pyjwt
from langchain_community.chat_models import ChatZhipuAI

model2 = ChatZhipuAI(
    model="glm-4-plus",
    streaming=True,
    zhipuai_api_key=os.getenv("ZHIPU_API_KEY"),
)

print(model2.invoke(messages))
