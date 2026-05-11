"""系统设置页面"""
import os
import streamlit as st
from modules.llm_service import get_llm_service
from modules.vector_store import VectorStoreManager
from modules.prompt_manager import PromptManager
from modules.model_config import ModelConfigManager
from config.settings import (
    DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL,
    LLM_MODELS, VISION_MODELS, T2I_MODELS, I2V_MODELS, TTS_MODELS, TTS_VOICES, ASR_MODELS
)
from utils.ui_helpers import apply_custom_css, show_api_key_check

apply_custom_css()

# 初始化管理器
llm_service = get_llm_service()
vector_manager = VectorStoreManager()
prompt_manager = PromptManager()
model_config = ModelConfigManager()

st.title("⚙️ 系统设置")

tab_api, tab_model, tab_prompts, tab_data = st.tabs([
    "🔑 API 配置", "🤖 模型设置", "📝 提示词管理", "💾 数据管理"
])

# ==================== Tab 1: API 配置 ====================
with tab_api:
    st.markdown("### 🔑 API 密钥配置")

    # 显示当前状态
    api_status_col1, api_status_col2 = st.columns(2)
    with api_status_col1:
        if DASHSCOPE_API_KEY:
            masked_key = DASHSCOPE_API_KEY[:8] + "..." + DASHSCOPE_API_KEY[-4:] if len(DASHSCOPE_API_KEY) > 12 else "***"
            st.success(f"当前状态: 已配置 ({masked_key})")
        else:
            st.error("当前状态: 未配置")
    with api_status_col2:
        base_url_status = "已配置" if DASHSCOPE_BASE_URL else "使用默认"
        st.info(f"Base URL: {DASHSCOPE_BASE_URL or '默认'}")

    st.markdown("---")
    with st.form("api_config_form"):
        new_api_key = st.text_input(
            "DASHSCOPE_API_KEY",
            value=DASHSCOPE_API_KEY,
            type="password",
            placeholder="sk-...",
            help="从阿里云 DashScope 控制台获取"
        )
        new_base_url = st.text_input(
            "Base URL",
            value=DASHSCOPE_BASE_URL,
            placeholder="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        col_save, col_test = st.columns(2)
        with col_save:
            save_btn = st.form_submit_button("💾 保存配置", use_container_width=True)
        with col_test:
            test_btn = st.form_submit_button("🔍 测试连接", use_container_width=True)

        if save_btn:
            if new_api_key:
                env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
                env_content = ""
                if os.path.exists(env_path):
                    with open(env_path, "r", encoding="utf-8") as f:
                        env_content = f.read()

                lines = env_content.split("\n")
                new_lines = []
                found_key = False
                found_url = False
                for line in lines:
                    if line.startswith("DASHSCOPE_API_KEY="):
                        new_lines.append(f"DASHSCOPE_API_KEY={new_api_key}")
                        found_key = True
                    elif line.startswith("DASHSCOPE_BASE_URL="):
                        new_lines.append(f"DASHSCOPE_BASE_URL={new_base_url}")
                        found_url = True
                    else:
                        new_lines.append(line)
                if not found_key:
                    new_lines.append(f"DASHSCOPE_API_KEY={new_api_key}")
                if not found_url:
                    new_lines.append(f"DASHSCOPE_BASE_URL={new_base_url}")

                with open(env_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_lines))

                st.success("配置已保存！请重启应用使新配置生效。")
                st.rerun()

        if test_btn:
            with st.spinner("正在测试连接..."):
                try:
                    # 使用临时 key 测试
                    from modules.llm_service import LLMService
                    test_service = LLMService(api_key=new_api_key or DASHSCOPE_API_KEY)
                    if test_service.test_connection():
                        st.success("连接测试成功！API 正常工作。")
                    else:
                        st.error("连接测试失败，请检查 API Key。")
                except Exception as e:
                    st.error(f"连接测试异常: {str(e)}")

    st.markdown("---")
    st.caption("📖 [获取 API Key](https://dashscope.console.aliyun.com/apiKey)")

# ==================== Tab 2: 模型设置 ====================
with tab_model:
    st.markdown("### 🤖 默认模型设置")

    config = model_config.get_config()

    with st.form("model_config_form"):
        st.markdown("#### LLM / 视觉模型")
        col1, col2, col3 = st.columns(3)
        with col1:
            llm_model = st.selectbox("LLM 默认模型", LLM_MODELS,
                                     index=LLM_MODELS.index(config.get("llm_model", "qwen-plus")) if config.get("llm_model") in LLM_MODELS else 0)
        with col2:
            vision_model = st.selectbox("视觉默认模型", VISION_MODELS,
                                        index=VISION_MODELS.index(config.get("vision_model", "qwen-vl-plus")) if config.get("vision_model") in VISION_MODELS else 0)
        with col3:
            temperature = st.slider("默认 Temperature", 0.0, 1.5, config.get("temperature", 0.7), 0.05)

        st.markdown("#### 生成类模型")
        col4, col5, col6 = st.columns(3)
        with col4:
            t2i_model = st.selectbox("文生图默认模型", T2I_MODELS,
                                     index=T2I_MODELS.index(config.get("t2i_model", "wan2.2-t2i-flash")) if config.get("t2i_model") in T2I_MODELS else 0)
        with col5:
            i2v_model = st.selectbox("图生视频默认模型", I2V_MODELS,
                                     index=I2V_MODELS.index(config.get("i2v_model", "wanx2.1-i2v-turbo")) if config.get("i2v_model") in I2V_MODELS else 0)
        with col6:
            asr_model = st.selectbox("语音识别默认模型", ASR_MODELS,
                                     index=ASR_MODELS.index(config.get("asr_model", "paraformer-v2")) if config.get("asr_model") in ASR_MODELS else 0)

        st.markdown("#### TTS / RAG 设置")
        col7, col8 = st.columns(2)
        with col7:
            tts_voice_labels = list(TTS_VOICES.values())
            tts_voice_keys = list(TTS_VOICES.keys())
            default_voice = config.get("tts_voice", "longxiaochun_v2")
            tts_idx = tts_voice_keys.index(default_voice) if default_voice in tts_voice_keys else 0
            tts_voice = st.selectbox("TTS 默认音色", tts_voice_labels, index=tts_idx)
            tts_voice_key = tts_voice_keys[tts_voice_labels.index(tts_voice)]
        with col8:
            max_tokens = st.number_input("默认 Max Tokens", 100, 8192, config.get("max_tokens", 2048), 100)

        st.markdown("#### RAG 检索设置")
        col9, col10, col11 = st.columns(3)
        with col9:
            top_k = st.number_input("默认 Top-K", 1, 20, config.get("top_k", 5))
        with col10:
            chunk_size = st.number_input("默认 Chunk Size", 100, 5000, config.get("chunk_size", 1000), 100)
        with col11:
            chunk_overlap = st.number_input("默认 Chunk Overlap", 0, 1000, config.get("chunk_overlap", 200), 50)

        col_save, col_reset = st.columns(2)
        with col_save:
            save_config_btn = st.form_submit_button("💾 保存默认设置", use_container_width=True)
        with col_reset:
            reset_btn = st.form_submit_button("🔄 恢复出厂设置", use_container_width=True)

        if save_config_btn:
            model_config.update_config(
                llm_model=llm_model,
                vision_model=vision_model,
                t2i_model=t2i_model,
                i2v_model=i2v_model,
                asr_model=asr_model,
                tts_voice=tts_voice_key,
                temperature=temperature,
                max_tokens=max_tokens,
                top_k=top_k,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            st.success("设置已保存！")
            st.rerun()

        if reset_btn:
            model_config.reset_to_default()
            st.success("已恢复出厂设置！")
            st.rerun()

# ==================== Tab 3: 提示词管理 ====================
with tab_prompts:
    st.markdown("### 📝 提示词管理")

    categories = ["全部"] + prompt_manager.get_categories()
    filter_cat = st.selectbox("按分类筛选", categories, key="prompt_filter")
    filter_val = None if filter_cat == "全部" else filter_cat

    prompts = prompt_manager.list_prompts(category=filter_val)

    if not prompts:
        st.info("暂无提示词模板")
    else:
        for p in prompts:
            with st.expander(f"{p['name']} ({p['category']}) {'⭐ 内置' if not p.get('is_custom') else '📝 自定义'}"):
                st.text(f"Temperature: {p.get('temperature', 0.7)}")
                st.text(f"Max Tokens: {p.get('max_tokens', 2048)}")
                st.text_area("内容", p.get("system_prompt", ""), height=150,
                             key=f"prompt_content_{p['id']}", disabled=not p.get('is_custom'))
                if p.get("is_custom"):
                    if st.button("🗑️ 删除此提示词", key=f"del_{p['id']}"):
                        prompt_manager.delete_custom_prompt(p["id"])
                        st.success("已删除")
                        st.rerun()

    st.markdown("---")
    st.markdown("#### ➕ 添加自定义提示词")
    with st.form("add_prompt_form"):
        new_id = st.text_input("ID（英文标识）", placeholder="my_custom_prompt")
        new_name = st.text_input("名称", placeholder="我的自定义提示词")
        new_category = st.selectbox("分类", ["custom", "general", "professional", "creative", "education"])
        new_content = st.text_area("提示词内容", height=120)
        new_temp = st.slider("Temperature", 0.0, 1.5, 0.7, 0.05, key="new_prompt_temp")
        new_tokens = st.number_input("Max Tokens", 100, 4096, 2048, 100, key="new_prompt_tokens")

        if st.form_submit_button("✅ 添加", use_container_width=True):
            if new_id and new_name and new_content:
                if prompt_manager.save_custom_prompt(new_id, new_name, new_content, new_category, new_temp, new_tokens):
                    st.success(f"提示词 '{new_name}' 添加成功！")
                    st.rerun()
                else:
                    st.error("添加失败")
            else:
                st.error("请填写 ID、名称和内容")

# ==================== Tab 4: 数据管理 ====================
with tab_data:
    st.markdown("### 💾 数据管理")

    st.markdown("#### 📊 存储信息")
    col1, col2, col3 = st.columns(3)
    with col1:
        collections = vector_manager.list_collections()
        total_docs = sum(c["document_count"] for c in collections)
        st.metric("知识库数量", len(collections))
    with col2:
        st.metric("文档总数", total_docs)
    with col3:
        # 计算存储大小
        db_path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_bases")
        total_size = 0
        if os.path.exists(db_path):
            for root, dirs, files in os.walk(db_path):
                for f in files:
                    fp = os.path.join(root, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
        st.metric("存储大小", f"{total_size / 1024 / 1024:.1f} MB" if total_size > 0 else "0 MB")

    st.markdown("---")
    st.markdown("#### 🗑️ 数据清理")

    col_clear1, col_clear2 = st.columns(2)
    with col_clear1:
        if st.button("清理临时文件", use_container_width=True):
            temp_dir = os.path.join(os.path.dirname(__file__), "..", "data", "temp_docs")
            if os.path.exists(temp_dir):
                for f in os.listdir(temp_dir):
                    try:
                        os.remove(os.path.join(temp_dir, f))
                    except Exception:
                        pass
            st.success("临时文件已清理")

    with col_clear2:
        st.warning("⚠️ 危险操作")
        confirm = st.checkbox("确认清空所有知识库数据")
        if st.button("清空所有知识库", type="secondary", use_container_width=True, disabled=not confirm):
            for c in vector_manager.list_collections():
                vector_manager.delete_collection(c["name"])
            st.success("所有知识库已清空")
            st.rerun()
