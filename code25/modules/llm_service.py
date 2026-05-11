"""LLM/Vision 服务模块 —— 封装 ChatOpenAI 调用（LLM对话 + 视觉理解）"""
import os
import base64
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from config.settings import DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL
from utils.file_utils import encode_image_to_base64, get_mime_type


class LLMService:
    """LLM 服务类，封装 ChatOpenAI 客户端（单例模式）"""

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or DASHSCOPE_API_KEY
        self.base_url = base_url or DASHSCOPE_BASE_URL

    def create_llm(self, model: str = "qwen-plus", temperature: float = 0.7,
                   max_tokens: int = 2048) -> ChatOpenAI:
        """创建文本 LLM 实例"""
        return ChatOpenAI(
            model=model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def create_vl_llm(self, model: str = "qwen-vl-plus", max_tokens: int = 1000) -> ChatOpenAI:
        """创建视觉模型实例"""
        return ChatOpenAI(
            model=model,
            api_key=self.api_key,
            base_url=self.base_url,
            max_tokens=max_tokens,
        )

    def chat(self, messages: list, model: str = "qwen-plus",
             temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """单轮/多轮对话"""
        llm = self.create_llm(model, temperature, max_tokens)
        langchain_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                langchain_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            else:
                langchain_messages.append(HumanMessage(content=content))
        response = llm.invoke(langchain_messages)
        return response.content

    def chat_stream(self, messages: list, model: str = "qwen-plus",
                    temperature: float = 0.7, max_tokens: int = 2048):
        """流式对话生成器"""
        llm = self.create_llm(model, temperature, max_tokens)
        langchain_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                langchain_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            else:
                langchain_messages.append(HumanMessage(content=content))
        for chunk in llm.stream(langchain_messages):
            if chunk.content:
                yield chunk.content

    def analyze_image_by_url(self, image_url: str, question: str,
                             model: str = "qwen-vl-plus") -> str:
        """通过图片URL进行视觉理解"""
        llm = self.create_vl_llm(model)
        message = HumanMessage(content=[
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": question},
        ])
        response = llm.invoke([message])
        return response.content

    def analyze_image_by_local(self, image_path: str, question: str,
                               model: str = "qwen-vl-plus") -> str:
        """通过本地图片（Base64）进行视觉理解"""
        llm = self.create_vl_llm(model)
        mime_type = get_mime_type(image_path)
        img_b64 = encode_image_to_base64(image_path)
        data_url = f"data:image/{mime_type};base64,{img_b64}"
        message = HumanMessage(content=[
            {"type": "image_url", "image_url": {"url": data_url}},
            {"type": "text", "text": question},
        ])
        response = llm.invoke([message])
        return response.content

    def analyze_video(self, video_url: str, question: str,
                      model: str = "qwen-vl-plus") -> str:
        """视频理解（直接传入视频URL）"""
        llm = self.create_vl_llm(model)
        message = HumanMessage(content=[
            {"type": "video_url", "video_url": {"url": video_url}},
            {"type": "text", "text": question},
        ])
        response = llm.invoke([message])
        return response.content

    def compare_images(self, question: str, *image_urls, model: str = "qwen-vl-plus") -> str:
        """多图对比分析"""
        llm = self.create_vl_llm(model)
        content = []
        for url in image_urls:
            content.append({"type": "image_url", "image_url": {"url": url}})
        content.append({"type": "text", "text": question})
        message = HumanMessage(content=content)
        response = llm.invoke([message])
        return response.content

    def test_connection(self) -> bool:
        """测试API连接是否正常"""
        try:
            response = self.chat([{"role": "user", "content": "你好"}])
            return bool(response)
        except Exception as e:
            print(f"连接测试失败: {e}")
            return False


@st.cache_resource
def get_llm_service() -> LLMService:
    """获取 LLMService 单例（Streamlit 缓存）"""
    return LLMService()
