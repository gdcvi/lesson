"""
 * @author: zkyuan
 * @date: 2025/8/18 15:34
 * @description: deepseek
"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model_name="deepseek-chat",
    # deepseek
    base_url='https://api.deepseek.com/v1',
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

messages = "你好，你是谁?"

print(model.invoke(messages))
