"""
 * @author: zkyuan
 * @date: 2025/8/19 14:07
 * @description:

使用 LangChain 实现一个动态历史对话系统

1、使用 MessagesPlaceholder 动态管理历史消息

2、实现多轮对话功能（至少3轮）

3、使用 ConversationBufferMemory 存储对话历史

4、通过 LCEL 链式编程整合提示词、模型和输出解析器

5、支持流式输出
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 加载环境变量
load_dotenv()

model = ChatOpenAI(
    model_name="deepseek-chat",
    # deepseek
    base_url='https://api.deepseek.com/v1',
    api_key=os.getenv("DEEPSEEK_API_KEY")
)


# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位专业的技术专家，用{style}风格回答问题"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 创建记忆系统
memory = ConversationBufferMemory(
    return_messages=True,  # 在加载记忆时返回消息对象列表，而不是格式化后的字符
    memory_key="history"  # 设置记忆存储的键名为 "history"
)


# 定义历史加载函数
def load_history(_):
    # 该表达式返回一个包含历史对话消息的列表
    return memory.load_memory_variables({})["history"]


# 构建LCEL链
chain = (
        RunnablePassthrough.assign(    # 动态加载历史对话消息
            history=load_history,      # 这里的参数是函数
            style=lambda _: "简洁专业"  # lambda匿名函数表达式：无论输入什么参数，这个函数都会返回字符串 "简洁专业"
        )
        | prompt
        | model
        | StrOutputParser()
)

# 对话演示
questions = [
    "量子计算的基本原理是什么？",
    "它与传统计算的主要区别是什么？",
    "量子计算目前有哪些实际应用？"
]

for i, question in enumerate(questions):
    print(f"\n\033[1;35m### 第 {i + 1} 轮提问: {question}\033[0m")

    # 输出内容保存起来
    response = ""

    # 调用链并流式输出
    for chunk in chain.stream({"input": question}):
        print(chunk, end="", flush=True)
        response += chunk

    # 保存历史
    memory.save_context({"input": question}, {"output": response})

    print("\n" + "-" * 80)