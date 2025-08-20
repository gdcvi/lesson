"""
 * @author: zkyuan
 * @date: 2025/8/19 10:54
 * @description: langchain的历史消息模版
1. 基本的多轮对话模板：直接在模板中硬编码历史消息（适用于固定示例）
2. 动态历史消息模板：使用`MessagesPlaceholder`动态传入消息列表
3. 带消息摘要的历史模板： 当历史较长时，使用摘要压缩信息
4. 带上下文窗口的历史模板：使用记忆机制（如`ConversationBufferWindowMemory`）维护固定长度的历史
5. 结构化历史模板：将历史数据转换为特定格式的文本
6. 带工具调用的历史模板：处理包含工具调用和返回的复杂对话

langchain历史消息模版1：
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

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

# 系统消息（可选）
system_template = "你是一个乐于助人的AI助手。"
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
# 历史消息（交替的用户和AI消息）
history_template = ChatPromptTemplate.from_messages(
    [
        # 系统消息
        system_message_prompt,
        # 第一轮对话
        HumanMessagePromptTemplate.from_template("你好！"),
        AIMessagePromptTemplate.from_template("你好！我是AI助手。有什么可以帮您？"),
        # 第二轮对话（使用变量）
        HumanMessagePromptTemplate.from_template("{user_input1}"),
        AIMessagePromptTemplate.from_template("{ai_response1}"),
        # 当前轮
        HumanMessagePromptTemplate.from_template("{current_input}")
    ]
)
# 使用模板
messages = history_template.format_prompt(
    user_input1="量子计算是什么？",
    ai_response1="量子计算是利用量子力学原理进行计算的一种新型计算模式。",
    current_input="我刚刚都问了你什么问题？"
).to_messages()

print(messages)

print(model.invoke(messages))
