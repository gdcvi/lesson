"""
4、向量相似度检索
"""
# pip install dashscope numpy
import os

import dashscope
from dotenv import load_dotenv
from numpy import dot
from numpy.linalg import norm

# 加载环境变量
load_dotenv()

# 设置通义千问 API Key
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


# 定义调用通义千问 Embedding API 的函数
def get_embedding(text):
    response = dashscope.TextEmbedding.call(
        model='text-embedding-v3',
        input=text
    )
    if response.status_code == 200:
        return response.output['embeddings'][0]['embedding']
    else:
        raise Exception(f"Embedding API 调用失败: {response.message}")


# 计算余弦相似度，参考文章：https://blog.csdn.net/Hyman_Qiu/article/details/137743190
# 定义一个函数 cosine_similarity，该函数接受两个向量 vec1 和 vec2 作为输入。
def cosine_similarity(vec1, vec2):
    # 计算并返回两个向量之间的余弦相似度，公式为：两个向量的点积除以它们范数的乘积。
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))


# 实现文本搜索功能
# 定义一个函数 search_documents，该函数接受一个查询字符串 query 和一个文档列表 documents 作为输入。
def search_documents(query, documents):
    # 调用 get_embedding 函数生成查询字符串的嵌入向量 query_embedding。
    query_embedding = get_embedding(query)
    # 对每个文档调用 get_embedding 函数生成文档的嵌入向量，存储在 document_embeddings 列表中。
    document_embeddings = [get_embedding(doc) for doc in documents]
    # 计算查询嵌入向量与每个文档嵌入向量之间的余弦相似度，存储在 similarities 列表中
    similarities = [cosine_similarity(query_embedding, doc_embedding) for doc_embedding in document_embeddings]
    # 找到相似度最高的文档的索引 most_similar_index。
    most_similar_index = similarities.index(max(similarities))
    # 返回相似度最高的文档和相似度得分。
    return documents[most_similar_index], max(similarities)


# 测试文本搜索功能
if __name__ == "__main__":
    documents = [
        "通义千问是阿里巴巴开发的强大语言模型。",
        "天空是蓝色的,阳光灿烂。",
        "人工智能正在改变世界。",
        "Python是一种流行的编程语言。"
    ]
    query = "天空"
    most_similar_document, similarity_score = search_documents(query, documents)
    print(f"最相似的文档: {most_similar_document}")
    print(f"相似性得分: {similarity_score}")
