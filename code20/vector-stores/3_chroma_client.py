"""
案例3: Chroma客户端使用 - 直接操作Chroma集合
学习要点:
- 使用ChromaDB的PersistentClient创建持久化客户端
- 直接操作Chroma集合(Collection)
- 将LangChain与原生Chroma客户端结合使用
"""
# 安装依赖: pip install langchain-chroma chromadb langchain-huggingface modelscope
import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 配置魔搭社区的Qwen嵌入模型
EMBEDDING_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"
# 配置集合名称
COLLECTION_NAME = "collection_1"

# 步骤1: 创建持久化Chroma客户端(数据保存在当前目录的chroma_db文件夹)
persistent_client = chromadb.PersistentClient(path="./chroma_client_db")

# 步骤2: 创建嵌入函数(使用Qwen模型)
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

# 步骤3: 获取或创建集合
collection = persistent_client.get_or_create_collection(COLLECTION_NAME)

# 步骤4: 向集合中添加文档
collection.add(
    ids=["1", "2", "3"],
    documents=["这是第一个文档", "这是第二个文档", "这是第三个文档"]
)
print(f"已添加3个文档到集合 '{COLLECTION_NAME}'")

# 步骤5: 使用LangChain包装Chroma集合,以便使用LangChain的功能
langchain_chroma = Chroma(
    client=persistent_client,
    collection_name=COLLECTION_NAME,
    embedding_function=embedding_function,
)

# 步骤6: 查询集合中的文档数量
doc_count = langchain_chroma._collection.count()
print(f"集合 '{COLLECTION_NAME}' 中共有 {doc_count} 个文档")

# 步骤7: 执行相似度搜索(可选)
query = "第一个文档"
results = langchain_chroma.similarity_search(query, k=2)
print(f"\n查询: {query}")
print("\n搜索结果:")
for i, doc in enumerate(results, 1):
    print(f"结果 {i}: {doc.page_content}")
