"""
案例6: Chroma使用Qwen嵌入模型 - 本地部署方案
学习要点:
- 使用魔搭社区的Qwen嵌入模型替代OpenAI
- 理解临时客户端(EphemeralClient)和持久化客户端的区别
- 在本地环境中运行完整的RAG流程
"""
# 安装依赖: pip install langchain-chroma chromadb langchain-huggingface modelscope
from langchain_chroma import Chroma
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 配置魔搭社区的Qwen嵌入模型
EMBEDDING_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

# 步骤1: 创建嵌入函数(使用Qwen模型,本地运行)
# 使用ModelScope下载模型
from modelscope import snapshot_download

# 从魔搭社区下载模型
model_dir = snapshot_download('qwen/Qwen3-Embedding-0.6B', cache_dir='./models')
print(f"模型已下载到: {model_dir}")

embeddings = HuggingFaceEmbeddings(
    model_name=model_dir,
    model_kwargs={'device': 'cpu'},  # 使用CPU,如有GPU可改为'cuda'
    encode_kwargs={'normalize_embeddings': True}
)

# 步骤2: 创建临时Chroma客户端(数据仅存在于内存中,程序结束后消失)
# EphemeralClient适合测试和临时使用
new_client = chromadb.EphemeralClient()
print("已创建临时Chroma客户端(数据存储在内存中)\n")

# 步骤3: 加载文本文档
loader = TextLoader("../resource/测试文件.txt", encoding="UTF-8")
documents = loader.load()

# 步骤4: 将文档分割成适当大小的片段
text_splitter = CharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=0
)
docs = text_splitter.split_documents(documents)
print(f"文档已分割成 {len(docs)} 个片段\n")

# 步骤5: 从文档创建Chroma向量数据库(使用临时客户端)
qwen_lc_client = Chroma.from_documents(
    docs, 
    embeddings, 
    client=new_client, 
    collection_name="qwen_collection"
)
print(f"向量数据库已创建,集合名称: 'qwen_collection'")
print(f"集合中包含 {qwen_lc_client._collection.count()} 个文档\n")

# 步骤6: 执行相似度搜索查询
query = "荒天帝是谁?"
results = qwen_lc_client.similarity_search(query, k=3)

# 步骤7: 打印查询结果
print("=" * 60)
print(f"查询: {query}")
print("=" * 60)
for i, doc in enumerate(results, 1):
    print(f"\n--- 结果 {i} ---")
    print(f"内容: {doc.page_content[:200]}...")
    print(f"元数据: {doc.metadata}")

print("\n" + "=" * 60)
print("提示: 本示例使用临时客户端,程序结束后数据会丢失")
print("如需持久化存储,请使用PersistentClient或persist_directory参数")
print("=" * 60)