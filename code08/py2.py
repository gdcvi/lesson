"""
 * @author: zkyuan
 * @date: 2025/8/19 13:51
 * @description: chain的异步流式输出
"""
import asyncio
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_template("详细介绍怎么做{input}")
model = ChatOpenAI(
    model_name="gpt-4o",
    # gpt代理配置
    base_url='https://api.openai-hk.com/v1/',
    api_key=os.getenv("OPEN_API_KEY")
)
parser = StrOutputParser()
chain = prompt | model | parser


async def async_stream():
    async for text in chain.astream({"input": "西红柿炒蛋"}):
        print(text, end="", flush=True)


# 运行异步流处理
asyncio.run(async_stream())
