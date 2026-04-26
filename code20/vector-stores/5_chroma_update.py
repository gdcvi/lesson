"""
案例5: Chroma更新和删除操作 - 管理向量库数据
学习要点:
- 为文档指定自定义ID以便后续更新和删除
- 更新文档内容和元数据
- 从向量库中删除文档
- 向已有向量库添加新文档
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

# 查询问题
query = "荒天帝是谁?"

# 步骤4: 为文档创建自定义ID(便于后续更新和删除操作)
custom_ids = [f"doc_{i}" for i in range(1, len(docs) + 1)]
print(f"创建了 {len(custom_ids)} 个文档ID: {custom_ids[:3]}...\n")

# 步骤5: 使用自定义ID创建向量数据库
example_db = Chroma.from_documents(
    docs, 
    embedding_function, 
    ids=custom_ids
)
print(f"向量数据库已创建,包含 {example_db._collection.count()} 个文档\n")

# 步骤6: 执行初始查询以获取要更新的文档
results = example_db.similarity_search(query, k=1)
doc_to_update = results[0]

print("=" * 60)
print("功能1: 更新文档元数据")
print("=" * 60)
# 步骤7: 修改文档的元数据
doc_to_update.metadata.update({
    "source": "../resource/测试文件.txt",
    "updated_by": "user",
    "update_time": "2026-04-26",
    "new_value": "hello world"
})

# 步骤8: 查看更新前的元数据
doc_id = custom_ids[0]  # 假设更新第一个文档
print(f"\n更新前文档 '{doc_id}' 的元数据:")
before_update = example_db._collection.get(ids=[doc_id])
print(f"{before_update['metadatas'][0]}\n")

# 步骤9: 执行更新操作(需要找到对应的ID)
# 注意: update_document需要知道文档的ID,这里我们更新第一个文档
example_db.update_document(doc_id, doc_to_update)

# 步骤10: 查看更新后的元数据
print(f"更新后文档 '{doc_id}' 的元数据:")
after_update = example_db._collection.get(ids=[doc_id])
print(f"{after_update['metadatas'][0]}\n")

print("=" * 60)
print("功能2: 删除文档")
print("=" * 60)
# 步骤11: 删除最后一个文档
doc_count_before = example_db._collection.count()
last_doc_id = custom_ids[-1]
print(f"\n删除前文档数量: {doc_count_before}")
print(f"即将删除文档: '{last_doc_id}'")

# 执行删除操作
example_db._collection.delete(ids=[last_doc_id])

doc_count_after = example_db._collection.count()
print(f"删除后文档数量: {doc_count_after}")
print(f"文档减少了 {doc_count_before - doc_count_after} 个\n")

print("=" * 60)
print("功能3: 向已有向量库添加新文档")
print("=" * 60)
# 步骤12: 添加新文档到已有向量库(可选操作)
# new_docs = [Document(page_content="新的文档内容", metadata={"source": "new_source.txt"})]
# example_db.add_documents(new_docs)
# print(f"添加新文档后总数: {example_db._collection.count()}")
