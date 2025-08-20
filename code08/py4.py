"""
 * @author: zkyuan
 * @date: 2025/8/19 14:27
 * @description:
使用 LangChain 实现一个带示例的问答系统，要求：

1、使用 FewShotPromptTemplate 提供问题解答示例

2、实现结构化输出（包含问题分类和答案）

3、使用 PydanticOutputParser 解析模型输出

4、通过 LCEL 链式编程整合所有组件
"""
import os
from typing import List

from dotenv import load_dotenv
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# 加载环境变量
load_dotenv()

# 创建模型
model = ChatOpenAI(
    model_name="deepseek-chat",
    # deepseek
    base_url='https://api.deepseek.com/v1',
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

# 示例数据
examples = [
    {
        "question": "量子纠缠是什么？",
        "answer": "量子纠缠是量子力学中的现象，当两个粒子相互纠缠时，无论它们相距多远，其状态都会即时相互影响。"
    },
    {
        "question": "量子计算的优势在哪里？",
        "answer": "量子计算在解决特定问题（如大数因子分解、优化问题）上比经典计算机快指数级，能处理经典计算机难以解决的复杂问题。"
    },
    {
        "question": "量子比特与传统比特的区别？",
        "answer": "传统比特只能表示0或1，而量子比特可以同时处于0和1的叠加态，且能通过量子纠缠实现并行计算。"
    }
]

# 示例模板
example_template = """
问题：{question}
答案：{answer}
"""
example_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template=example_template
)

# 创建少量示例提示词
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="问题：{input}\n",
    input_variables=["input"],
)


# 定义输出结构
class QAResponse(BaseModel):
    category: str = Field(description="问题分类")
    answer: str = Field(description="问题答案")
    related_questions: List[str] = Field(description="相关问题列表")


# 创建输出解析器
parser = PydanticOutputParser(pydantic_object=QAResponse)

format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

# 创建最终提示模板
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位量子计算专家，请根据以下示例回答问题。回答格式必须是JSON格式：、、\n" + format_instructions),
    ("human", few_shot_prompt.format(input="{input}"))
])

print(final_prompt.format(input="量子退相干是什么意思"))

# 构建LCEL链
chain = final_prompt | model | parser

# 测试问题
questions = [
    "量子退相干是什么意思？",
    "量子计算机如何解决优化问题？",
    "量子隐形传态的原理是什么？"
]

for question in questions:
    print(f"\n\033[1;35m### 问题: {question}\033[0m")
    response = chain.invoke({"input": question})

    print(f"\n分类: {response.category}")
    print(f"答案: {response.answer}")
    print(f"相关问题: {', '.join(response.related_questions)}")
    print("-" * 80)
