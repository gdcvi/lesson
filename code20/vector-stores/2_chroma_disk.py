"""
案例2: Chroma持久化存储 - 磁盘向量库
学习要点:
- 将向量数据库保存到磁盘实现持久化存储
- 从磁盘加载已保存的向量数据库
- 避免重复计算嵌入向量,提高性能
"""
# 安装依赖: pip install langchain-chroma langchain-huggingface modelscope
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import os

# 配置魔搭社区的Qwen嵌入模型
EMBEDDING_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"
# 配置持久化存储路径
PERSIST_DIRECTORY = "./chroma_db_disk"

# 步骤1: 加载文本文档
loader = TextLoader("../resource/测试文件.txt", encoding="UTF-8")
documents = loader.load()

# 步骤2: 将文档分割成适当大小的片段
text_splitter = CharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=0
)
docs = text_splitter.split_documents(documents)

# 步骤3: 创建嵌入函数(使用Qwen模型)
# 使用ModelScope下载模型
from modelscope import snapshot_download

# 从魔搭社区下载模型
model_dir = snapshot_download('qwen/Qwen3-Embedding-0.6B', cache_dir='./models')
print(f"模型已下载到: {model_dir}")

embedding_function = HuggingFaceEmbeddings(
    model_name=model_dir,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# 查询问题
query = "Pixar公司是做什么的?"

# 步骤4: 创建向量数据库并保存到磁盘
db_save = Chroma.from_documents(
    docs, 
    embedding_function, 
    persist_directory=PERSIST_DIRECTORY
)
print(f"向量数据库已保存到: {PERSIST_DIRECTORY}")

# 步骤5: 从磁盘加载向量数据库
db_load = Chroma(
    persist_directory=PERSIST_DIRECTORY, 
    embedding_function=embedding_function
)
print(f"向量数据库已从磁盘加载")

# 步骤6: 执行相似度搜索查询
results = db_load.similarity_search(query, k=3)

# 步骤7: 打印查询结果
print(f"\n查询: {query}")
print("\n搜索结果:")
for i, doc in enumerate(results, 1):
    print(f"\n--- 结果 {i} ---")
    print(f"内容: {doc.page_content[:200]}...")
    print(f"元数据: {doc.metadata}")
