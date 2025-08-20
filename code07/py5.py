"""
 * @author: zkyuan
 * @date: 2025/8/19 11:08
 * @description: langchain历史消息模版2
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model_name="gpt-4o",
    # gpt代理配置
    base_url='https://api.openai-hk.com/v1/',
    api_key=os.getenv("OPEN_API_KEY")
)

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

# 使用MessagesPlaceholder来动态插入历史消息
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你是一个专业的技术专家。"),
    # 预留位置用于存储历史消息（包括用户和AI的交替消息）
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
# 假设历史消息已经是一个消息列表
from langchain.schema import HumanMessage, AIMessage

history = [
    HumanMessage(content="量子计算是什么？"),
    AIMessage(content="量子计算是利用量子力学原理进行计算的一种新型计算模式。"),
    HumanMessage(content="它有什么优势？")
]
# 使用模板
messages = prompt.format_prompt(
    history=history,
    input="与传统计算机相比呢？"
).to_messages()

print(messages)

print(model.invoke(messages))