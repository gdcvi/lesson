"""
TXT文档处理示例 - 关键字符号切分
展示如何处理TXT格式文档，使用关键字符号进行智能分割
使用通义千问embedding和Chroma内存向量库
适配LangChain 0.3版本
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载环境变量
load_dotenv()

print("=" * 80)
print("TXT文档处理 - 关键字符号切分")
print("=" * 80)

# 第1步：配置通义千问Embedding模型
print("\n[步骤1] 配置Embedding模型...")
embedding_function = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
print("✓ Embedding模型配置完成")

# 第2步：加载TXT文档
print("\n[步骤2] 加载TXT文档（测试文件.txt - 小说文本）...")
loader = TextLoader("../resource/测试文件.txt", encoding="UTF-8")
documents = loader.load()
print(f"✓ 成功加载文档，总长度: {len(documents[0].page_content)} 字符")

# 第3步：使用关键字符号进行递归分割
print("\n[步骤3] 使用关键字符号进行文本分割...")
# 针对中文优化的分隔符列表，按优先级排列
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,           # 每个片段的目标大小
    chunk_overlap=50,         # 片段重叠，保持上下文连贯
    length_function=len,      # 长度计算函数
    is_separator_regex=False, # 分隔符不是正则表达式
    separators=[
        "\n\n",               # 双换行（段落分隔）
        "\n",                 # 单换行
        "。",                  # 中文句号
        "！",                  # 中文感叹号
        "？",                  # 中文问号
        "；",                  # 中文分号
        "\uff0c",             # 全角逗号
        "\u3001",             # 顿号
        " ",                  # 空格
        "",                   # 字符级别（最后手段）
    ]
)

docs = text_splitter.split_documents(documents)
print(f"✓ 文档被分割成 {len(docs)} 个片段")
print(f"  平均片段长度: {sum(len(doc.page_content) for doc in docs) // len(docs)} 字符")

# 显示前几个片段的预览
print("\n前3个片段预览:")
for i, doc in enumerate(docs[:3], 1):
    print(f"\n--- 片段 {i} ---")
    print(f"{doc.page_content[:150]}...")

# 第4步：创建Chroma内存向量库
print("\n" + "=" * 80)
print("[步骤4] 创建Chroma内存向量库...")
db = Chroma.from_documents(docs, embedding_function)
print("✓ 向量库创建完成（仅内存存储）")

# 第5步：执行查询测试
print("\n" + "=" * 80)
print("[步骤5] 执行相似性搜索测试...")
queries = [
    "石昊是谁?",
    "火灵儿怎么了?",
    "柳神的状态如何?"
]

for query in queries:
    print(f"\n{'-' * 80}")
    print(f"查询: {query}")
    print('-' * 80)
    
    # 执行相似性搜索
    results = db.similarity_search(query, k=2)
    
    for i, doc in enumerate(results, 1):
        print(f"\n结果 {i}:")
        print(f"{doc.page_content[:200]}...")

print("\n" + "=" * 80)
print("TXT文档处理完成！")
print("=" * 80)
