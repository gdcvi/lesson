"""
1、文本向量化
"""
# pip install langchain-community dashscope
import os

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings

# 加载环境变量
load_dotenv()

# 创建通义千问 embedding 模型
embeddings_model = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

embeddings = embeddings_model.embed_documents(
    [
        "嗨！",
        "哦，你好！",
        "你叫什么名字？",
        "我的名字是张魁元！",
        "Hello World！",
        "你的名字是什么"
    ]
)
# 第一个打印是embeddings的文本数量，第二个打印是第一段文本的embedding向量维度
print(len(embeddings), len(embeddings[0]))
