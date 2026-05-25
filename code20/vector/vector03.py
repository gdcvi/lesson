"""
3、向量匹配文档-RAG
"""
import os
# 依赖冲突
# pip install langchain==0.2.16
# pip install langchain-core==0.2.43
# pip install langchain-community==0.2.17
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatTongyi
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv()

# 数据导入
import pathlib

current_dir = pathlib.Path(__file__).parent
loader = TextLoader(current_dir / "测试文档.txt", encoding="UTF-8")
docs = loader.load()
# 数据切分 :  \n
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
# 创建embedding - 使用通义千问
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
# 通过向量数据库存储，暂存在内存中
vector = FAISS.from_documents(documents, embeddings)
# 查询检索
# 创建 prompt
prompt = ChatPromptTemplate.from_template("""仅根据提供的上下文回答以下问题：:
<context>
{context}
</context>
Question: {input}""")
# 创建模型 - 使用通义千问
llm = ChatTongyi(
    model="qwen-plus",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
# 创建 document 的chain 查询
document_chain = create_stuff_documents_chain(llm, prompt)

# 创建搜索chain 返回值为 VectorStoreRetriever
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
# 执行请求
response = retrieval_chain.invoke({"input": "给我讲个笑话"})
print(response["answer"])
