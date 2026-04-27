"""
多种切分方式对比示例
对比Token长度、关键字符号、百分位差异等多种切分方式的效果
使用通义千问embedding和Chroma内存向量库
适配LangChain 0.3版本
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import (
    TokenTextSplitter,
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter
)

# 加载环境变量
load_dotenv()

print("=" * 80)
print("多种切分方式对比实验")
print("=" * 80)

# 第1步：配置Embedding模型
print("\n[步骤1] 配置Embedding模型...")
embedding_function = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
print("✓ Embedding模型配置完成")

# 第2步：加载文档
print("\n[步骤2] 加载测试文档（数据集制作.md）...")
loader = TextLoader("../resource/数据集制作.md", encoding="UTF-8")
documents = loader.load()
text_content = documents[0].page_content
print(f"✓ 文档总长度: {len(text_content)} 字符")

# 第3步：不同切分方式对比
print("\n" + "=" * 80)
print("[步骤3] 应用不同的切分方式...")
print("=" * 80)

# 方法1：Token长度切分
print("\n[方法1] Token长度切分")
print("-" * 80)
token_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
token_docs = token_splitter.split_documents(documents)
print(f"片段数量: {len(token_docs)}")
print(f"平均长度: {sum(len(doc.page_content) for doc in token_docs) // len(token_docs)} 字符")

# 方法2：关键字符号切分（递归字符分割）
print("\n[方法2] 关键字符号切分（RecursiveCharacterTextSplitter）")
print("-" * 80)
char_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "；", "\uff0c", "\u3001", " ", ""]
)
char_docs = char_splitter.split_documents(documents)
print(f"片段数量: {len(char_docs)}")
print(f"平均长度: {sum(len(doc.page_content) for doc in char_docs) // len(char_docs)} 字符")

# 方法3：固定字符切分
print("\n[方法3] 固定字符切分（CharacterTextSplitter）")
print("-" * 80)
fixed_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50, separator="\n")
fixed_docs = fixed_splitter.split_documents(documents)
print(f"片段数量: {len(fixed_docs)}")
print(f"平均长度: {sum(len(doc.page_content) for doc in fixed_docs) // len(fixed_docs)} 字符")

# 方法4：语义分割（如果可用）
print("\n[方法4] 语义分割（SemanticChunker - 百分位差异）")
print("-" * 80)
try:
    from langchain_experimental.text_splitter import SemanticChunker
    
    semantic_splitter = SemanticChunker(
        embedding_function,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=50
    )
    semantic_docs = semantic_splitter.split_documents(documents)
    print(f"片段数量: {len(semantic_docs)}")
    print(f"平均长度: {sum(len(doc.page_content) for doc in semantic_docs) // len(semantic_docs)} 字符")
    
    methods = [
        ("Token长度", token_docs),
        ("关键字符号", char_docs),
        ("固定字符", fixed_docs),
        ("语义分割", semantic_docs)
    ]
except ImportError:
    print("⚠ langchain-experimental未安装，跳过语义分割")
    methods = [
        ("Token长度", token_docs),
        ("关键字符号", char_docs),
        ("固定字符", fixed_docs)
    ]

# 第4步：对比总结
print("\n" + "=" * 80)
print("[对比总结] 各切分方式效果对比")
print("=" * 80)
print(f"{'切分方式':<20} {'片段数量':>10} {'平均长度':>10} {'总片段大小':>12}")
print("-" * 80)
for name, docs in methods:
    total_size = sum(len(doc.page_content) for doc in docs)
    avg_length = total_size // len(docs)
    print(f"{name:<18} {len(docs):>10} {avg_length:>10} {total_size:>10}")

# 第5步：向量检索效果对比
print("\n" + "=" * 80)
print("[步骤5] 向量检索效果对比测试")
print("=" * 80)

test_query = "什么是LoRA微调?"
print(f"\n测试查询: {test_query}\n")

for name, docs in methods:
    print(f"-{'-' * 78}")
    print(f"方法: {name}")
    print('-' * 80)
    
    # 创建向量库
    db = Chroma.from_documents(docs, embedding_function)
    
    # 执行搜索
    results = db.similarity_search_with_score(test_query, k=2)
    
    for i, (doc, score) in enumerate(results, 1):
        print(f"\n结果 {i} (相似度分数: {score:.4f}):")
        print(f"{doc.page_content[:200]}...")
    print()

# 第6步：不同chunk_size的影响
print("\n" + "=" * 80)
print("[步骤6] 不同Chunk Size对Token切分的影响")
print("=" * 80)

chunk_sizes = [200, 500, 1000, 2000]
print(f"{'Chunk Size':>12} {'片段数量':>10} {'平均长度':>10}")
print("-" * 80)

for size in chunk_sizes:
    splitter = TokenTextSplitter(chunk_size=size, chunk_overlap=size // 10)
    temp_docs = splitter.split_documents(documents)
    avg_len = sum(len(doc.page_content) for doc in temp_docs) // len(temp_docs)
    print(f"{size:>12} {len(temp_docs):>10} {avg_len:>10}")

print("\n" + "=" * 80)
print("对比实验完成！")
print("=" * 80)
print("\n总结与建议：")
print("1. Token切分：最适合LLM处理，精确控制输入长度")
print("2. 关键字符号：保持语义完整性，适合中文文本")
print("3. 固定字符：简单直接，但可能切断句子")
print("4. 语义分割：最智能，但计算成本高，需要额外依赖")
print("\n选择建议：")
print("- 通用场景：推荐使用关键字符号切分（RecursiveCharacterTextSplitter）")
print("- LLM应用：推荐使用Token切分，更符合模型实际输入")
print("- 长文档：推荐使用语义分割，保持逻辑完整性")
print("- 简单场景：可以使用固定字符切分")
