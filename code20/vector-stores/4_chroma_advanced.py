"""
案例4: Chroma高级查询功能 - 相似度分数、MMR和过滤
学习要点:
- 使用similarity_search_with_score获取相似度分数(余弦距离)
- 使用MMR(最大边界相关性)搜索提高结果多样性
- 使用元数据过滤筛选特定文档
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

# 步骤4: 创建Chroma向量数据库
db = Chroma.from_documents(docs, embedding_function)

# 查询问题
query = "荒天帝是谁?"

print("=" * 60)
print("功能1: 带相似度分数的搜索")
print("=" * 60)
# 步骤5: 执行带分数的相似度搜索(返回余弦距离,分数越低越相似)
results_with_scores = db.similarity_search_with_score(query, k=3)
print(f"\n查询: {query}\n")
for i, (doc, score) in enumerate(results_with_scores, 1):
    print(f"--- 结果 {i} ---")
    print(f"相似度分数(余弦距离): {score:.4f} (越低越相似)")
    print(f"内容: {doc.page_content[:200]}...")
    print(f"元数据: {doc.metadata}\n")

print("=" * 60)
print("功能2: 使用MMR(最大边界相关性)搜索")
print("=" * 60)
# 步骤6: 使用MMR检索器进行搜索(提高结果多样性,避免冗余)
mmr_retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,           # 返回结果数量
        "fetch_k": 10,    # 初始候选集大小
        "lambda_mult": 0.5  # MMR权重(0-1),越高越重视相关性,越低越重视多样性
    }
)
mmr_results = mmr_retriever.invoke(query)
print(f"\n查询: {query}\n")
for i, doc in enumerate(mmr_results, 1):
    print(f"--- MMR结果 {i} ---")
    print(f"内容: {doc.page_content[:200]}...")
    print(f"元数据: {doc.metadata}\n")

print("=" * 60)
print("功能3: 使用元数据过滤")
print("=" * 60)
# 步骤7: 根据元数据过滤文档(例如按来源文件筛选)
filtered_docs = db.get(where={"source": "../resource/测试文件.txt"})
print(f"\n从源文件 '../resource/测试文件.txt' 中检索到 {len(filtered_docs['ids'])} 个文档")
print(f"文档ID列表: {filtered_docs['ids'][:5]}...")  # 只显示前5个
