"""
2、向量检索文本
演示如何使用 embedding 模型将文档和查询转换为向量，用于后续的语义检索
"""
# pip install langchain-community dashscope
import os
import numpy as np

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings

# 加载环境变量
load_dotenv()

# 创建通义千问 embedding 模型实例
embeddings_model = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

documents = [
        "嗨！",
        "哦，你好！",
        "你叫什么名字？",
        "我的名字是张魁元！",
        "Hello World！",
        "你的名字是什么"
    ]

# 将文档列表转换为向量表示，用于构建向量数据库
embeddings = embeddings_model.embed_documents(documents)

# 将查询文本转换为向量，用于与文档向量进行相似度匹配
embedded_query = embeddings_model.embed_query("你的名字是什么")

# 输出查询向量的前5个维度值，验证向量化结果
print(embedded_query[:5])
print(embedded_query[0])

# 计算查询向量与每个文档向量的余弦相似度，找出最相关的文本
# 使用余弦相似度公式计算查询向量与所有文档向量的相似度
similarities = [np.dot(embedded_query, emb) / (np.linalg.norm(embedded_query) * np.linalg.norm(emb)) for emb in embeddings]

# 将文档和相似度配对，并按相似度从高到低排序
ranked_results = sorted(zip(documents, similarities), key=lambda x: x[1], reverse=True)

# 输出最相似的文档
most_similar_doc, most_similar_score = ranked_results[0]
print(f"\n最相似文档：{most_similar_doc}")
print(f"相似度：{most_similar_score:.4f}")

# 按相似度从高到低输出所有文档
print("\n检索结果（按相似度排序）：")
for rank, (doc, sim) in enumerate(ranked_results, 1):
    print(f"{rank}. {doc} (相似度: {sim:.4f})")


