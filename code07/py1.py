"""
 * @author: zkyuan
 * @date: 2025/8/19 10:14
 * @description: langchain的提示词模版
1. 基本提示模板（PromptTemplate）
2. 聊天提示模板（ChatPromptTemplate）
3. 少量示例提示模板（FewShotPromptTemplate）
4. 带示例选择器的少量示例模板
5. 结构化输出模板（StructuredOutputParser）
6. 管道提示（PipelinePrompt）
7. 自定义复杂逻辑模板
8. 提示模板组合

 langchain的提示词模块1
    基本提示模板（PromptTemplate）
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

# 导入langchain提示词模版库
from langchain.prompts import PromptTemplate

# 定义一个提示模板，包含adjective和content两个模板变量，模板变量使用{}包括起来

prompt_template = PromptTemplate.from_template(
    "给我讲一个关于{content}的{adjective}笑话。"

)

# 通过模板参数格式化提示模板
result = prompt_template.format(adjective="冷", content="猴子")
print(result)

# 提示词推理结果
print(model.invoke(result))

