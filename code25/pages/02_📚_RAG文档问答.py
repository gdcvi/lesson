"""RAG 文档问答页面"""
import os
import streamlit as st
from modules.llm_service import get_llm_service
from modules.document_processor import DocumentProcessor
from modules.vector_store import VectorStoreManager
from modules.chat_engine import ChatEngine
from modules.prompt_manager import PromptManager
from config.settings import (
    ALLOWED_DOC_EXTENSIONS, MAX_FILE_SIZE_DOC, TEMP_DIR,
    DEFAULT_TOP_K, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
)
from utils.ui_helpers import apply_custom_css, show_api_key_check

apply_custom_css()

if not show_api_key_check():
    st.stop()

# 初始化 session_state
if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = []
if "rag_mode" not in st.session_state:
    st.session_state.rag_mode = "临时文档"
if "temp_documents" not in st.session_state:
    st.session_state.temp_documents = []
if "active_collection" not in st.session_state:
    st.session_state.active_collection = None

# 初始化管理器
llm_service = get_llm_service()
doc_processor = DocumentProcessor()
vector_manager = VectorStoreManager()
prompt_manager = PromptManager()

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## ⚙️ 问答配置")

    mode = st.radio("📊 问答模式", ["临时文档", "知识库"],
                    index=0 if st.session_state.rag_mode == "临时文档" else 1,
                    key="mode_radio")
    st.session_state.rag_mode = mode

    st.markdown("---")

    if mode == "临时文档":
        st.markdown("#### 📤 上传文档")
        uploaded_files = st.file_uploader(
            "支持 PDF, TXT, DOCX, MD, CSV, XLSX",
            type=[ext.lstrip('.') for ext in ALLOWED_DOC_EXTENSIONS],
            accept_multiple_files=True,
            key="temp_uploader"
        )
        if uploaded_files:
            for f in uploaded_files:
                if f.size > MAX_FILE_SIZE_DOC:
                    st.error(f"文件 {f.name} 超过 10MB 限制")
                    uploaded_files = None
                    break

        if st.button("📥 处理文档", use_container_width=True) and uploaded_files:
            with st.spinner("正在处理文档..."):
                docs, saved_files = doc_processor.process_uploaded_files(
                    uploaded_files, TEMP_DIR, persistent=False
                )
                st.session_state.temp_documents = docs
                # 清理临时文件
                doc_processor.cleanup_temp_files(saved_files)
            st.success(f"已处理 {len(docs)} 个文档片段")
        if st.session_state.temp_documents:
            st.info(f"当前文档片段: {len(st.session_state.temp_documents)} 个")

    else:
        st.markdown("#### 📚 选择知识库")
        collections = vector_manager.list_collections()
        if not collections:
            st.warning("暂无知识库，请先在知识库管理页面创建")
        else:
            col_names = [c["display_name"] for c in collections]
            selected = st.selectbox("知识库", col_names, key="kb_select")
            for c in collections:
                if c["display_name"] == selected:
                    st.session_state.active_collection = c["name"]
                    st.metric("文档数量", c["document_count"])
                    break

    st.markdown("---")
    st.markdown("#### 📝 提示词设置")
    prompts = prompt_manager.list_prompts()
    prompt_options = {"无（默认）": None}
    for p in prompts:
        prompt_options[f"{p['name']} ({p['category']})"] = p["id"]
    selected_prompt_label = st.selectbox("选择提示词模板", list(prompt_options.keys()), key="prompt_selector")
    selected_prompt_id = prompt_options[selected_prompt_label]
    if selected_prompt_id:
        prompt_data = prompt_manager.get_prompt(selected_prompt_id)
        if prompt_data:
            with st.expander("查看提示词内容"):
                st.text(prompt_data.get("system_prompt", ""))

    st.markdown("---")
    st.markdown("#### 🔧 模型参数")
    temperature = st.slider("Temperature", 0.0, 1.0, DEFAULT_TEMPERATURE, 0.05, key="rag_temp")
    top_k = st.slider("Top-K 检索", 1, 10, DEFAULT_TOP_K, key="rag_topk")

    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.rag_messages = []
        st.rerun()

# ==================== 主区域 ====================
st.title("📚 RAG 文档智能问答")
st.caption(f"当前模式：**{st.session_state.rag_mode}** | 对话轮数：{len(st.session_state.rag_messages) // 2}")

# 渲染对话历史
for msg in st.session_state.rag_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📎 引用来源"):
                for i, src in enumerate(msg["sources"], 1):
                    fname = src.get("metadata", {}).get("filename", "未知文件")
                    st.caption(f"**来源 {i}** ({fname})")
                    st.text(src["content"])

# 输入框
user_input = st.chat_input("请输入您的问题...")
if user_input:
    st.session_state.rag_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # 获取 prompt
            system_prompt = None
            if selected_prompt_id:
                prompt_data = prompt_manager.get_prompt(selected_prompt_id)
                if prompt_data:
                    system_prompt = prompt_data.get("system_prompt", "")

            # 准备消息
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            # 添加上下文（最近几轮对话）
            for m in st.session_state.rag_messages[-6:]:
                messages.append(m)

            if st.session_state.rag_mode == "临时文档":
                if st.session_state.temp_documents:
                    # 创建内存向量存储用于检索
                    from langchain_chroma import Chroma
                    from langchain_community.embeddings import DashScopeEmbeddings
                    from config.settings import DASHSCOPE_API_KEY, EMBEDDING_MODEL

                    embeddings = DashScopeEmbeddings(
                        model=EMBEDDING_MODEL,
                        dashscope_api_key=DASHSCOPE_API_KEY
                    )
                    temp_store = Chroma.from_documents(
                        st.session_state.temp_documents, embeddings,
                        persist_directory=None
                    )
                    retriever = temp_store.as_retriever(search_kwargs={"k": top_k})

                    engine = ChatEngine(temperature=temperature)
                    stream_result = engine.stream_chat_with_rag(
                        user_input, retriever, system_prompt
                    )
                    for chunk in stream_result:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

                    sources = stream_result.return_value.get("sources", []) if hasattr(stream_result, 'return_value') else []
                else:
                    full_response = "请先在侧边栏上传文档。"
                    message_placeholder.markdown(full_response)
                    sources = []
            else:
                if st.session_state.active_collection:
                    retriever = vector_manager.get_retriever(
                        st.session_state.active_collection, k=top_k
                    )
                    if retriever:
                        engine = ChatEngine(temperature=temperature)
                        stream_result = engine.stream_chat_with_rag(
                            user_input, retriever, system_prompt
                        )
                        for chunk in stream_result:
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)

                        sources = stream_result.return_value.get("sources", []) if hasattr(stream_result, 'return_value') else []
                    else:
                        full_response = "知识库加载失败，请检查或重新选择。"
                        message_placeholder.markdown(full_response)
                        sources = []
                else:
                    full_response = "请先在侧边栏选择一个知识库。"
                    message_placeholder.markdown(full_response)
                    sources = []

            # 显示引用来源
            if sources:
                with st.expander("📎 引用来源"):
                    for i, src in enumerate(sources, 1):
                        fname = src.get("metadata", {}).get("filename", "未知文件")
                        st.caption(f"**来源 {i}** ({fname})")
                        st.text(src["content"])

        except Exception as e:
            full_response = f"出错了: {str(e)}"
            message_placeholder.error(full_response)
            sources = []

        st.session_state.rag_messages.append({
            "role": "assistant",
            "content": full_response,
            "sources": sources if 'sources' in dir() else []
        })
