# pip install langchain-community faiss-cpu dashscope python-dotenv
# 如果您需要使用没有 AVX2 优化的 FAISS 进行初始化，请取消下面一行的注释
# os.environ['FAISS_NO_AVX2'] = '1'

import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

# 加载环境变量
load_dotenv()

# 加载文档
loader = TextLoader("../resource/测试文件.txt", encoding="UTF-8")
documents = loader.load()

# 文本分割
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 创建通义千问 embedding 模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 创建向量数据库（内存中，不持久化）
db = FAISS.from_documents(docs, embeddings)

query = "石昊是谁？"
# 返回文档以及查询与它们之间的距离分数。返回的距离分数是 L2 距离。因此，得分越低越好。
docs_and_scores = db.similarity_search_with_score(query)
print(docs_and_scores)

# 还可以使用`similarity_search_by_vector`来搜索与给定嵌入向量相似的文档，该函数接受一个嵌入向量作为参数，而不是字符串。
embedding_vector = embeddings.embed_query(query)
docs_and_scores = db.similarity_search_by_vector(embedding_vector)
print(docs_and_scores)
