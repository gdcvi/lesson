"""
 * @author: zkyuan
 * @date: 2025/8/18 15:34
 * @description: deepseek流式输出
"""
import asyncio
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

messages = "详细介绍怎么做西红柿炒蛋"

# for chunk in model.stream(messages):
#     print(chunk)

# for chunk in model.stream(messages):
#     print(chunk.content)

for chunk in model.stream(messages):
    print(chunk.content, end="")


print("--------------------------分割线--------------------------")
# 异步流式输出
async def async_stream():
    async for chunk in model.astream(messages):
        print(chunk.content, end="")


# 运行异步流处理
asyncio.run(async_stream())
