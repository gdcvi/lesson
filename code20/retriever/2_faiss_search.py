# pip install langchain-community faiss-cpu dashscope python-dotenv
# 如果需要使用没有 AVX2 优化的 FAISS 进行初始化，请取消下面一行的注释
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

# 索引数量
print(db.index.ntotal)

query = "石昊是谁？"
docs = db.similarity_search(query)
print(docs[0].page_content)
