"""
案例1: Chroma基础用法 - 内存向量库
学习要点:
- 使用Chroma创建内存中的向量数据库
- 文档加载和分割
- 使用Qwen嵌入模型进行向量化
- 执行相似度搜索查询
"""
# 安装依赖: pip install langchain-chroma langchain-huggingface modelscope
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# 配置魔搭社区的Qwen嵌入模型
EMBEDDING_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

# 步骤1: 加载文本文档
loader = TextLoader("../resource/测试文件.txt", encoding="UTF-8")
documents = loader.load()

# 步骤2: 将文档分割成适当大小的片段
text_splitter = CharacterTextSplitter(
    chunk_size=1500,  # 每个文本块的大小
    chunk_overlap=0  # 文本块之间的重叠大小
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
    model_kwargs={'device': 'cpu'},  # 使用CPU,如有GPU可改为'cuda'
    encode_kwargs={'normalize_embeddings': True}  # 标准化嵌入向量
)

# 步骤4: 从文档创建Chroma向量数据库(存储在内存中)
db = Chroma.from_documents(docs, embedding_function)

# 步骤5: 执行相似度搜索查询
query = "荒天帝是谁?"
results = db.similarity_search(query, k=3)  # 返回最相似的3个结果

# 步骤6: 打印查询结果
print(f"查询: {query}")
print("\n搜索结果:")
for i, doc in enumerate(results, 1):
    print(f"\n--- 结果 {i} ---")
    print(f"内容: {doc.page_content[:200]}...")
    print(f"元数据: {doc.metadata}")
