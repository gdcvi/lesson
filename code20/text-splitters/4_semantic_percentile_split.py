"""
语义分割示例 - 百分位差异切分
展示如何使用SemanticChunker基于语义相似度进行智能分割
使用通义千问embedding和Chroma内存向量库
适配LangChain 0.3版本
注意：需要安装 langchain-experimental
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

# 加载环境变量
load_dotenv()

print("=" * 80)
print("语义分割 - 百分位差异切分")
print("=" * 80)

# 第1步：配置通义千问Embedding模型
print("\n[步骤1] 配置Embedding模型...")
embedding_function = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
print("✓ Embedding模型配置完成")

# 第2步：加载文档
print("\n[步骤2] 加载测试文档...")
loader = TextLoader("../resource/测试文件.txt", encoding="UTF-8")
documents = loader.load()
print(f"✓ 成功加载文档，总长度: {len(documents[0].page_content)} 字符")

# 第3步：使用语义分割器
print("\n" + "=" * 80)
print("[步骤3] 使用SemanticChunker进行语义分割...")
print("=" * 80)

try:
    from langchain_experimental.text_splitter import SemanticChunker
    
    # 方法一：基于百分位数的分割（默认）
    print("\n[方法一] 百分位数分割（默认50%阈值）")
    print("-" * 80)
    
    semantic_splitter_percentile = SemanticChunker(
        embedding_function,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=50  # 50百分位，即中位数
    )
    
    docs_percentile = semantic_splitter_percentile.split_documents(documents)
    print(f"✓ 分割成 {len(docs_percentile)} 个语义片段")
    print(f"  平均片段长度: {sum(len(doc.page_content) for doc in docs_percentile) // len(docs_percentile)} 字符")
    
    # 显示前几个片段
    print("\n前2个片段预览:")
    for i, doc in enumerate(docs_percentile[:2], 1):
        print(f"\n--- 片段 {i} ---")
        print(f"{doc.page_content[:200]}...")
    
    # 方法二：基于标准差的分割
    print("\n" + "=" * 80)
    print("[方法二] 标准差分割（更保守的分割策略）")
    print("-" * 80)
    
    semantic_splitter_std = SemanticChunker(
        embedding_function,
        breakpoint_threshold_type="standard_deviation",
        breakpoint_threshold_amount=1.0  # 1个标准差
    )
    
    docs_std = semantic_splitter_std.split_documents(documents)
    print(f"✓ 分割成 {len(docs_std)} 个语义片段")
    print(f"  平均片段长度: {sum(len(doc.page_content) for doc in docs_std) // len(docs_std)} 字符")
    
    # 方法三：基于四分位距的分割
    print("\n" + "=" * 80)
    print("[方法三] 四分位距分割（IQR方法）")
    print("-" * 80)
    
    semantic_splitter_iqr = SemanticChunker(
        embedding_function,
        breakpoint_threshold_type="interquartile",
        breakpoint_threshold_amount=1.5  # 1.5倍IQR
    )
    
    docs_iqr = semantic_splitter_iqr.split_documents(documents)
    print(f"✓ 分割成 {len(docs_iqr)} 个语义片段")
    print(f"  平均片段长度: {sum(len(doc.page_content) for doc in docs_iqr) // len(docs_iqr)} 字符")
    
    # 对比三种方法
    print("\n" + "=" * 80)
    print("[对比] 三种语义分割方法的效果对比")
    print("=" * 80)
    print(f"{'方法':<20} {'片段数量':>10} {'平均长度':>10}")
    print("-" * 80)
    print(f"{'百分位数 (50%)':<20} {len(docs_percentile):>10} {sum(len(doc.page_content) for doc in docs_percentile) // len(docs_percentile):>10}")
    print(f"{'标准差 (1.0σ)':<20} {len(docs_std):>10} {sum(len(doc.page_content) for doc in docs_std) // len(docs_std):>10}")
    print(f"{'四分位距 (1.5×IQR)':<20} {len(docs_iqr):>10} {sum(len(doc.page_content) for doc in docs_iqr) // len(docs_iqr):>10}")
    
    # 第4步：创建向量库并测试（使用百分位数方法）
    print("\n" + "=" * 80)
    print("[步骤4] 创建向量库并执行查询测试...")
    db = Chroma.from_documents(docs_percentile, embedding_function)
    print("✓ 向量库创建完成")
    
    # 执行查询
    queries = [
        "石昊的情感变化",
        "火灵儿的状态",
        "时间长河的作用"
    ]
    
    for query in queries:
        print(f"\n{'-' * 80}")
        print(f"查询: {query}")
        print('-' * 80)
        
        results = db.similarity_search(query, k=2)
        
        for i, doc in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f"{doc.page_content[:250]}...")
    
    print("\n" + "=" * 80)
    print("语义分割完成！")
    print("=" * 80)
    print("\n提示：语义分割能更好地理解文本的逻辑结构，适合长文档处理。")
    print("      百分位数方法最常用，标准差方法更保守，IQR方法更稳健。")

except ImportError:
    print("❌ 未安装 langchain-experimental 包")
    print("\n请运行以下命令安装：")
    print("  pip install langchain-experimental")
    print("\n语义分割功能需要使用实验性的SemanticChunker")
