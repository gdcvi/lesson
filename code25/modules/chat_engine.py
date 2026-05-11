"""对话引擎模块 —— 适配 LLMService"""
from typing import Optional, List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from modules.llm_service import LLMService
from config.settings import DASHSCOPE_API_KEY


class ChatEngine:
    """RAG 对话引擎类"""

    def __init__(self, model_name: str = "qwen-plus",
                 temperature: float = 0.7, max_tokens: int = 2048):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm_service = LLMService()

    def _build_rag_chain(self, context: str, prompt_template: str):
        """构建 RAG 链"""
        llm = self.llm_service.create_llm(self.model_name, self.temperature, self.max_tokens)
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = (
            {"context": lambda x: context, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain

    def chat_with_rag(self, query: str, retriever,
                      prompt_template: Optional[str] = None) -> Dict:
        """基于RAG的对话"""
        if prompt_template is None:
            prompt_template = """你是一个智能助手，请基于以下上下文信息回答用户问题。

上下文信息：
{context}

用户问题：{question}

如果上下文中没有相关信息，请诚实告知用户。请提供准确、有帮助的回答。

回答："""

        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        chain = self._build_rag_chain(context, prompt_template)
        answer = chain.invoke(query)

        sources = []
        for doc in docs:
            sources.append({
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            })

        return {"answer": answer, "sources": sources, "source_count": len(sources)}

    def stream_chat_with_rag(self, query: str, retriever,
                             prompt_template: Optional[str] = None):
        """流式输出RAG对话"""
        if prompt_template is None:
            prompt_template = """你是一个智能助手，请基于以下上下文信息回答用户问题。

上下文信息：
{context}

用户问题：{question}

如果上下文中没有相关信息，请诚实告知用户。请提供准确、有帮助的回答。

回答："""

        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        chain = self._build_rag_chain(context, prompt_template)
        for chunk in chain.stream(query):
            yield chunk

        sources = []
        for doc in docs:
            sources.append({
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            })
        return {"sources": sources, "source_count": len(sources)}

    def chat_without_rag(self, query: str, system_prompt: Optional[str] = None) -> str:
        """不使用RAG的直接对话"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})
        return self.llm_service.chat(messages, self.model_name, self.temperature, self.max_tokens)

    def test_connection(self) -> bool:
        return self.llm_service.test_connection()
