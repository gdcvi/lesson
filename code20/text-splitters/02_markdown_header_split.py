"""
Markdown文档处理示例 - 标题层级切分
展示如何处理Markdown格式文档，按标题层级进行智能分割
使用通义千问embedding和Chroma内存向量库
适配LangChain 0.3版本
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# 加载环境变量
load_dotenv()

print("=" * 80)
print("Markdown文档处理 - 标题层级切分")
print("=" * 80)

# 第1步：配置通义千问Embedding模型
print("\n[步骤1] 配置Embedding模型...")
embedding_function = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
print("✓ Embedding模型配置完成")

# 第2步：加载Markdown文档
print("\n[步骤2] 加载Markdown文档（数据集制作.md）...")
loader = TextLoader("../resource/数据集制作.md", encoding="UTF-8")
documents = loader.load()
print(f"✓ 成功加载文档，总长度: {len(documents[0].page_content)} 字符")

# 第3步：方法一 - 按标题层级分割
print("\n" + "=" * 80)
print("[方法一] 按Markdown标题层级分割")
print("=" * 80)

# 定义要分割的标题层级
headers_to_split_on = [
    ("#", "一级标题"),
    ("##", "二级标题"),
    ("###", "三级标题"),
    ("####", "四级标题"),
]

# 创建Markdown分割器
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False  # 保留标题在内容中
)

md_docs = markdown_splitter.split_text(documents[0].page_content)
print(f"✓ 按标题分割成 {len(md_docs)} 个片段")

# 显示前几个片段的元数据和内容预览
print("\n前3个片段:")
for i, doc in enumerate(md_docs[:3], 1):
    print(f"\n--- 片段 {i} ---")
    print(f"元数据: {doc.metadata}")
    print(f"内容预览: {doc.page_content[:200]}...")

# 第4步：方法二 - 结合标题分割和递归字符分割
print("\n" + "=" * 80)
print("[方法二] 标题分割 + 递归字符分割（混合方式）")
print("=" * 80)

# 先按标题分割，再对每个片段进行字符分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        "。",
        "！",
        "？",
        "；",
        "\uff0c",
        "\u3001",
        " ",
        "",
    ]
)

# 对每个Markdown片段进一步分割
final_docs = []
for md_doc in md_docs:
    sub_docs = text_splitter.split_text(md_doc.page_content)
    for sub_text in sub_docs:
        from langchain_core.documents import Document
        final_docs.append(Document(
            page_content=sub_text,
            metadata=md_doc.metadata
        ))

print(f"✓ 混合分割后得到 {len(final_docs)} 个片段")
print(f"  平均片段长度: {sum(len(doc.page_content) for doc in final_docs) // len(final_docs)} 字符")

# 第5步：创建向量库并测试
print("\n" + "=" * 80)
print("[步骤5] 创建向量库并执行查询测试...")
db = Chroma.from_documents(final_docs, embedding_function)
print("✓ 向量库创建完成")

# 执行查询
queries = [
    "什么是LoRA微调?",
    "全参数微调和PEFT有什么区别?",
    "Alpaca格式的数据集是什么样的?"
]

for query in queries:
    print(f"\n{'-' * 80}")
    print(f"查询: {query}")
    print('-' * 80)
    
    results = db.similarity_search(query, k=2)
    
    for i, doc in enumerate(results, 1):
        print(f"\n结果 {i}:")
        print(f"元数据: {doc.metadata}")
        print(f"内容: {doc.page_content[:250]}...")

print("\n" + "=" * 80)
print("Markdown文档处理完成！")
print("=" * 80)
