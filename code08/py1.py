"""
 * @author: zkyuan
 * @date: 2025/8/19 11:20
 * @description: langchain的LCEL链式编程

"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# 提示词
prompt = ChatPromptTemplate.from_template("详细介绍怎么做{input}")
# 模型
model = ChatOpenAI(
    model_name="gpt-4o",
    # gpt代理配置
    base_url='https://api.openai-hk.com/v1/',
    api_key=os.getenv("OPEN_API_KEY")
)
# 解析器
parser = StrOutputParser()
chain = prompt | model | parser

print(chain.invoke({"input": "西红柿炒蛋"}))

"""
管道操作符（|）：是一种用于将一个命令或函数的输出直接传递给下一个命令或函数作为输入的工具

一、为什么顺序不能改变？
1. 输入输出兼容性：
   每个组件的输出必须与下一个组件的输入在类型和结构上兼容。
   例如，`prompt`组件输出的是一个`PromptValue`对象（通常包含格式化后的字符串或消息列表），而`model`组件期望的输入正是这种格式。
   如果调换顺序，比如`model | prompt`，那么`model`的输出（通常是一个字符串或消息）可能无法满足`prompt`组件的输入要求（可能需要一个字典或其他结构）。
2. 功能逻辑：
   链的顺序反映了处理步骤的逻辑顺序。在RAG（检索增强生成）中，典型的顺序是：检索文档 -> 构建提示 -> 调用模型 -> 解析输出。
   - 如果改变顺序，比如先调用模型再检索文档，那么模型将无法利用检索到的文档信息。
3. 组件的职责：
   每个组件都有其特定的职责。例如：
   `prompt`：负责将输入变量填充到提示模板中，生成一个完整的提示。
   `model`：负责接收提示并调用大模型生成响应。
   `parser`：负责将模型的原始输出解析为所需的格式（如字符串、JSON对象等）。
   改变顺序会打破这种职责链，导致组件无法正常工作。



二、如何确定连接顺序？
确定连接顺序的关键在于理解每个组件的输入和输出要求，以及整个链的处理流程。以下是确定顺序的步骤：
1. 明确处理流程：
   定义你的任务需要哪些步骤。例如，一个简单的问答链可能需要：
     接收用户问题。
     将问题填充到提示模板中（形成完整的提示）。
     将提示发送给大模型。
     解析模型的输出。
2. 了解每个组件的输入输出：
   PromptTemplate：输入是一个字典（包含模板中需要的变量），输出是一个`PromptValue`（可以转换为字符串或消息列表）。
   Model（如`ChatOpenAI`）：输入可以是字符串、`PromptValue`或消息列表，输出是一个`ChatMessage`或`LLMResult`（取决于模型类型）。
   Parser（如`StrOutputParser`）：输入是模型的输出，输出是解析后的结果（如字符串、字典等）。
3. 按照逻辑顺序连接：
   从接收原始输入开始，逐步处理，直到得到最终输出。
   典型顺序：`input -> prompt -> model -> parser`。
     `prompt`接收原始输入（通常是字典）并生成提示。
     `model`接收提示并生成模型输出。
     `parser`接收模型输出并解析。
4. 检查兼容性：
   确保前一个组件的输出类型与下一个组件的输入类型匹配。例如：
     `prompt`的输出是`PromptValue`，而`ChatOpenAI`的输入可以是`PromptValue`（因为它可以自动转换为消息列表）。因此`prompt | model`是可行的。
     `model`的输出是`ChatMessage`，而`StrOutputParser`的输入是`ChatMessage`（它会提取其中的文本内容）。因此`model | parser`是可行的。
     
"""