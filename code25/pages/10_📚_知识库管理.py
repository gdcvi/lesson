"""知识库管理页面 —— 创建、上传文档、查看详情、删除知识库"""
import os
import time
import streamlit as st
from modules.vector_store import VectorStoreManager
from modules.document_processor import DocumentProcessor
from config.settings import TEMP_DIR, ALLOWED_DOC_EXTENSIONS, MAX_FILE_SIZE_DOC, COLORS
from utils.ui_helpers import apply_custom_css, show_api_key_check
from utils.file_utils import format_file_size

apply_custom_css()

if not show_api_key_check():
    st.stop()

vector_manager = VectorStoreManager()
doc_processor = DocumentProcessor()

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 📚 知识库管理")
    st.markdown("---")

    if st.button("🔄 刷新列表", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 统计信息")
    collections = vector_manager.list_collections()
    total_docs = sum(c.get("document_count", 0) for c in collections)
    st.metric("知识库总数", len(collections))
    st.metric("文档总数", total_docs)

    st.markdown("---")
    st.markdown("### 💡 使用提示")
    st.info("""
    1. 先创建知识库
    2. 向知识库上传文档
    3. 在 **RAG文档问答** 页面选择知识库进行问答
    - 支持 PDF/TXT/DOCX/MD/CSV/XLSX
    - 单文件建议 < 10MB
    - 文档会自动分块和向量化
    """)

# ==================== 主区域 ====================
st.title("📚 知识库管理")
st.caption("创建和管理知识库，上传文档后可在 RAG 文档问答页面进行智能检索")

# 初始化 session_state
if "kb_show_upload" not in st.session_state:
    st.session_state.kb_show_upload = {}

tab_list, tab_create = st.tabs(["📁 知识库列表", "➕ 创建新知识库"])

# ==================== Tab 1: 知识库列表 ====================
with tab_list:
    collections = vector_manager.list_collections()

    if not collections:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 60px 20px;
            background: {COLORS['primary']}08;
            border-radius: 16px;
            border: 2px dashed {COLORS['primary']}30;
            margin: 20px 0;
        ">
            <div style="font-size: 56px; margin-bottom: 16px;">📚</div>
            <div style="font-size: 20px; font-weight: 700; color: #333; margin-bottom: 8px;">
                暂无知识库
            </div>
            <div style="font-size: 14px; color: #757575;">
                请切换到 <b>"➕ 创建新知识库"</b> 标签页创建您的第一个知识库
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 知识库卡片网格
        for idx in range(0, len(collections), 3):
            row_cols = st.columns(3)
            for col_idx in range(3):
                if idx + col_idx >= len(collections):
                    break
                collection = collections[idx + col_idx]
                col_name = collection["name"]
                display_name = collection.get("display_name", col_name)
                doc_count = collection.get("document_count", 0)
                description = collection.get("description", "")

                with row_cols[col_idx]:
                    # 卡片头部
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {COLORS['primary']}20;
                        border-radius: 14px;
                        padding: 0;
                        margin-bottom: 20px;
                        background: white;
                        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
                        overflow: hidden;
                    ">
                        <div style="
                            background: linear-gradient(135deg, {COLORS['primary']}10 0%, {COLORS['primary']}05 100%);
                            padding: 20px;
                            border-bottom: 1px solid {COLORS['primary']}10;
                        ">
                            <div style="font-size: 28px; margin-bottom: 8px;">📖</div>
                            <div style="font-size: 17px; font-weight: 700; color: #212121; margin-bottom: 4px;">
                                {display_name}
                            </div>
                            <div style="font-size: 12px; color: #888;">
                                {description[:50] + '...' if len(description) > 50 else description or '无描述'}
                            </div>
                        </div>
                        <div style="padding: 16px 20px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 13px; color: #555;">
                                    📄 文档: <b>{doc_count}</b> 个片段
                                </span>
                                <span style="
                                    display: inline-block;
                                    padding: 2px 10px;
                                    border-radius: 10px;
                                    font-size: 11px;
                                    background: {COLORS['success']}15;
                                    color: {COLORS['success']};
                                    border: 1px solid {COLORS['success']}30;
                                ">✅ 正常</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 操作按钮
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("📤 上传文档", key=f"kb_upload_{col_name}", use_container_width=True):
                            st.session_state.kb_show_upload[col_name] = not st.session_state.kb_show_upload.get(col_name, False)
                    with btn_col2:
                        if st.button("🗑️ 删除", key=f"kb_delete_{col_name}", use_container_width=True, type="secondary"):
                            st.session_state[f"kb_confirm_delete_{col_name}"] = True

                    # 删除确认
                    if st.session_state.get(f"kb_confirm_delete_{col_name}", False):
                        st.warning(f"确定删除「{display_name}」？此操作不可恢复！")
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("✅ 确认删除", key=f"kb_confirm_yes_{col_name}", use_container_width=True):
                                with st.spinner("正在删除..."):
                                    if vector_manager.delete_collection(col_name):
                                        st.success("已删除")
                                        st.session_state.pop(f"kb_confirm_delete_{col_name}", None)
                                        time.sleep(0.5)
                                        st.rerun()
                                    else:
                                        st.error("删除失败")
                        with confirm_col2:
                            if st.button("❌ 取消", key=f"kb_confirm_no_{col_name}", use_container_width=True):
                                st.session_state.pop(f"kb_confirm_delete_{col_name}", None)
                                st.rerun()

                    # 上传文档区域
                    if st.session_state.kb_show_upload.get(col_name, False):
                        st.markdown(f"""
                        <div style="
                            border: 2px solid {COLORS['primary']}40;
                            border-radius: 12px;
                            padding: 16px;
                            margin: -8px 0 16px 0;
                            background: {COLORS['primary']}05;
                        ">
                            <div style="font-weight: 600; margin-bottom: 8px;">📤 向「{display_name}」上传文档</div>
                        </div>
                        """, unsafe_allow_html=True)

                        uploaded_files = st.file_uploader(
                            "选择文档文件",
                            type=[ext.lstrip('.') for ext in ALLOWED_DOC_EXTENSIONS],
                            accept_multiple_files=True,
                            key=f"kb_uploader_{col_name}",
                            label_visibility="collapsed"
                        )

                        upload_btn_col1, upload_btn_col2 = st.columns(2)
                        with upload_btn_col1:
                            if st.button("📥 开始处理", key=f"kb_process_{col_name}", use_container_width=True, type="primary"):
                                if not uploaded_files:
                                    st.error("请先选择文件")
                                else:
                                    # 检查文件大小
                                    valid = True
                                    for f in uploaded_files:
                                        if f.size > MAX_FILE_SIZE_DOC:
                                            st.error(f"文件 {f.name} 超过 10MB 限制（当前: {format_file_size(f.size)}）")
                                            valid = False
                                    if valid:
                                        with st.spinner("正在处理文档..."):
                                            try:
                                                docs, saved_files = doc_processor.process_uploaded_files(
                                                    uploaded_files, TEMP_DIR, persistent=True
                                                )
                                                if not docs:
                                                    st.error("未能从文档中提取内容")
                                                else:
                                                    success = vector_manager.add_documents(col_name, docs)
                                                    doc_processor.cleanup_temp_files(saved_files)
                                                    if success:
                                                        st.success(f"成功添加 {len(docs)} 个文档片段！")
                                                        st.session_state.kb_show_upload[col_name] = False
                                                        time.sleep(0.5)
                                                        st.rerun()
                                                    else:
                                                        st.error("添加到知识库失败")
                                            except Exception as e:
                                                st.error(f"处理失败: {str(e)}")

                        with upload_btn_col2:
                            if st.button("❌ 取消", key=f"kb_cancel_{col_name}", use_container_width=True):
                                st.session_state.kb_show_upload[col_name] = False
                                st.rerun()

        st.markdown("---")

        # ==================== 知识库详情 ====================
        st.markdown("### 🔍 知识库详情")
        name_mapping = {c.get("display_name", c["name"]): c["name"] for c in collections}
        display_names = list(name_mapping.keys())

        selected_display = st.selectbox("选择知识库查看详情", display_names, key="kb_detail_select")

        if selected_display:
            selected_col = name_mapping[selected_display]
            stats = vector_manager.get_collection_stats(selected_col)

            detail_cols = st.columns(3)
            with detail_cols[0]:
                st.metric("内部名称", selected_col)
            with detail_cols[1]:
                st.metric("文档片段数", stats.get("document_count", 0))
            with detail_cols[2]:
                st.metric("状态", "正常" if stats.get("exists") else "异常")

            st.info("提示：文档上传后会自动分块并生成向量索引。如需重新上传，请先删除知识库后重建。")

# ==================== Tab 2: 创建新知识库 ====================
with tab_create:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']}08 0%, {COLORS['success']}08 100%);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid {COLORS['primary']}15;
    ">
        <div style="font-size: 18px; font-weight: 700; margin-bottom: 6px;">📝 创建新知识库</div>
        <div style="font-size: 13px; color: #666;">
            知识库用于持久化存储文档的向量索引，创建后可反复上传文档并在 RAG 问答页面使用。
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("create_kb_form"):
        col_name, col_desc = st.columns([2, 3])

        with col_name:
            kb_name = st.text_input(
                "知识库名称 *",
                placeholder="例如：产品文档、技术资料",
                help="支持中文名称，系统会自动转换为合法格式"
            )

        with col_desc:
            kb_desc = st.text_area(
                "知识库描述",
                placeholder="简要描述这个知识库的用途和内容...",
                height=88
            )

        st.markdown("")
        submitted = st.form_submit_button("✅ 创建知识库", type="primary", use_container_width=True)

        if submitted:
            if not kb_name.strip():
                st.error("请输入知识库名称")
            else:
                # 检查是否已存在
                valid_name = vector_manager._validate_and_convert_name(kb_name.strip())
                if vector_manager.collection_exists(valid_name):
                    st.error(f"知识库「{kb_name}」已存在，请使用其他名称")
                else:
                    with st.spinner("正在创建知识库..."):
                        success = vector_manager.create_collection(kb_name.strip(), kb_desc.strip())
                    if success:
                        st.success(f"知识库「{kb_name}」创建成功！")
                        st.balloons()
                        st.markdown(f"""
                        <div style="
                            background: {COLORS['success']}10;
                            border: 1px solid {COLORS['success']}30;
                            border-radius: 10px;
                            padding: 16px;
                            margin-top: 12px;
                        ">
                            <div style="font-weight: 600; color: {COLORS['success']}; margin-bottom: 6px;">
                                下一步操作
                            </div>
                            <div style="font-size: 13px; color: #555;">
                                1. 切换到 <b>「📁 知识库列表」</b> 标签页<br>
                                2. 找到新创建的知识库，点击 <b>「📤 上传文档」</b><br>
                                3. 上传完成后，在 <b>「RAG文档问答」</b> 页面选择该知识库即可开始问答
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("创建知识库失败，请重试")
