"""
PDF文档处理示例 - Token长度切分
展示如何处理PDF格式文档，使用Token长度进行精确分割
使用通义千问embedding和Chroma内存向量库
适配LangChain 0.3版本
注意：需要安装 pypdf 或 PyMuPDF
"""
import os
from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import TokenTextSplitter

# 加载环境变量
load_dotenv()

print("=" * 80)
print("PDF文档处理 - Token长度切分")
print("=" * 80)

# 第1步：配置通义千问Embedding模型
print("\n[步骤1] 配置Embedding模型...")
embedding_function = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
print("✓ Embedding模型配置完成")

# 第2步：加载PDF文档
print("\n[步骤2] 加载PDF文档（稻鱼共生生态智能机器人监测技术_余淼.pdf）...")
try:
    from langchain_community.document_loaders import PyPDFLoader
    
    pdf_path = "../resource/稻鱼共生生态智能机器人监测技术_余淼.pdf"
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    print(f"✓ 成功加载PDF文档")
    print(f"  页数: {len(documents)}")
    print(f"  总字符数: {sum(len(doc.page_content) for doc in documents)}")
    
    # 显示前几页的预览
    print("\n前2页内容预览:")
    for i, doc in enumerate(documents[:2], 1):
        print(f"\n--- 第 {i} 页 ---")
        print(f"元数据: {doc.metadata}")
        print(f"内容: {doc.page_content[:200]}...")
        
except ImportError:
    print("⚠ 未安装 pypdf，尝试使用 PyMuPDF...")
    try:
        from langchain_community.document_loaders import PyMuPDFLoader
        
        pdf_path = "../resource/稻鱼共生生态智能机器人监测技术_余淼.pdf"
        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()
        
        print(f"✓ 成功加载PDF文档（使用PyMuPDF）")
        print(f"  页数: {len(documents)}")
        
    except ImportError:
        print("❌ 错误：未安装PDF解析库")
        print("请运行以下命令之一安装：")
        print("  pip install pypdf")
        print("  或")
        print("  pip install pymupdf")
        exit(1)

# 第3步：使用Token长度进行分割
print("\n" + "=" * 80)
print("[步骤3] 使用Token长度进行文本分割...")
print("=" * 80)

# 创建Token分割器
# Token是基于模型的词汇表单位，比字符更准确反映模型的实际输入
token_splitter = TokenTextSplitter(
    chunk_size=500,   # 每个片段的Token数量
    chunk_overlap=50  # 片段重叠的Token数
)

docs = token_splitter.split_documents(documents)
print(f"✓ 文档被分割成 {len(docs)} 个片段（基于Token）")
print(f"  平均每片段Token数: ~{sum(len(token_splitter.split_text(doc.page_content)) for doc in docs) // len(docs)}")

# 显示前几个片段
print("\n前3个片段预览:")
for i, doc in enumerate(docs[:3], 1):
    tokens = token_splitter.split_text(doc.page_content)
    print(f"\n--- 片段 {i} ({len(tokens)} tokens) ---")
    print(f"{doc.page_content[:200]}...")

# 第4步：对比不同chunk_size的效果
print("\n" + "=" * 80)
print("[步骤4] 对比不同Token大小的分割效果...")
print("=" * 80)

chunk_sizes = [200, 500, 1000]
for size in chunk_sizes:
    splitter = TokenTextSplitter(chunk_size=size, chunk_overlap=size // 10)
    temp_docs = splitter.split_documents(documents)
    print(f"Chunk Size {size:4d}: {len(temp_docs):4d} 个片段")

# 第5步：创建向量库并测试
print("\n" + "=" * 80)
print("[步骤5] 创建向量库并执行查询测试...")
db = Chroma.from_documents(docs, embedding_function)
print("✓ 向量库创建完成")

# 执行查询（根据PDF主题调整查询）
queries = [
    "稻鱼共生系统是什么?",
    "智能机器人如何监测?",
    "生态技术的特点"
]

for query in queries:
    print(f"\n{'-' * 80}")
    print(f"查询: {query}")
    print('-' * 80)
    
    results = db.similarity_search(query, k=2)
    
    for i, doc in enumerate(results, 1):
        print(f"\n结果 {i}:")
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"来源: {doc.metadata.get('source', '未知')}")
            if 'page' in doc.metadata:
                print(f"页码: {doc.metadata['page']}")
        print(f"内容: {doc.page_content[:250]}...")

print("\n" + "=" * 80)
print("PDF文档处理完成！")
print("=" * 80)
print("\n提示：Token分割更适合大模型处理，因为LLM实际接收的是Token而非字符。")
