"""音频生文（ASR）页面"""
import os
import time
import streamlit as st
from modules.audio_service import ASRService
from config.settings import ASR_MODELS, ALLOWED_AUDIO_EXTENSIONS, MAX_FILE_SIZE_AUDIO
from utils.ui_helpers import apply_custom_css, show_api_key_check
from utils.file_utils import format_file_size

apply_custom_css()

if not show_api_key_check():
    st.stop()

asr_service = ASRService()

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 🎤 音频生文配置")

    model_name = st.selectbox("🤖 识别模型", ASR_MODELS, key="asr_model")

    st.markdown("#### ⚙️ 识别模式")
    asr_mode = st.radio("模式", ["同步（短音频 < 60s）", "异步（长音频）"], key="asr_mode")

    st.markdown("---")
    st.markdown("#### 💡 使用提示")
    st.caption("- 支持 WAV/MP3/FLAC/M4A/OGG")
    st.caption("- 最大 100MB")
    st.caption("- 支持中英文混合识别")
    st.caption("- 同步模式适合短音频")
    st.caption("- 异步模式适合长音频，需等待")

# ==================== 主区域 ====================
st.title("🎤 AI 音频生文")
st.caption("将语音文件识别转换为文字，支持中英文")

tab_file, tab_url = st.tabs(["📁 上传文件", "🌐 音频 URL"])

audio_source = None
source_type = None

with tab_file:
    uploaded_file = st.file_uploader(
        "上传音频文件",
        type=[ext.lstrip('.') for ext in ALLOWED_AUDIO_EXTENSIONS],
        key="asr_upload",
        label_visibility="collapsed"
    )
    if uploaded_file:
        if uploaded_file.size > MAX_FILE_SIZE_AUDIO:
            st.error(f"文件大小超过 100MB 限制（当前: {format_file_size(uploaded_file.size)}）")
        else:
            st.audio(uploaded_file)
            st.caption(f"文件: {uploaded_file.name} ({format_file_size(uploaded_file.size)})")
            # 保存临时文件
            temp_dir = os.path.join(os.path.dirname(__file__), "..", "data", "temp_docs")
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, f"asr_input_{int(time.time())}_{uploaded_file.name}")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            audio_source = temp_path
            source_type = "file"

with tab_url:
    audio_url = st.text_input(
        "音频 URL",
        placeholder="https://example.com/audio.wav",
        key="asr_url"
    )
    if audio_url:
        st.caption(f"URL: {audio_url[:80]}...")
        audio_source = audio_url
        source_type = "url"

recognize_btn = st.button("🎤 开始识别", type="primary", use_container_width=True)

if recognize_btn:
    if not audio_source:
        st.error("请上传音频文件或输入音频 URL")
    elif source_type == "file":
        st.warning("当前仅支持公网可访问的音频 URL。请将音频上传到图床或 OSS 后使用 URL 模式。")
        st.info("提示：可使用阿里云 OSS 或其他文件存储服务获取音频 URL。")
    else:
        is_async = asr_mode == "异步（长音频）"
        with st.spinner(f"正在{'异步' if is_async else '同步'}识别中..."):
            start_time = time.time()
            try:
                if is_async:
                    text = asr_service.transcribe_async(audio_source, model_name)
                else:
                    result = asr_service.transcribe_with_detail(audio_source, model_name)
                    text = result.get("text", "")
                    sentences = result.get("sentences", [])

                elapsed = time.time() - start_time
                st.success(f"识别完成！耗时 {elapsed:.1f} 秒")

                st.markdown("---")
                st.markdown("### 📝 识别结果")

                if text:
                    st.markdown(f'<div style="background: #f8faff; border-radius: 12px; padding: 20px; font-size: 16px; line-height: 1.8;">{text}</div>', unsafe_allow_html=True)
                else:
                    st.warning("未能识别出文本内容")

                # 操作按钮
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📄 导出 TXT",
                        text or "",
                        f"transcript_{int(time.time())}.txt",
                        "text/plain",
                        use_container_width=True
                    )
                with col2:
                    if st.button("📋 复制文本", use_container_width=True):
                        st.toast("文本已复制到剪贴板（请手动 Ctrl+C 复制上方内容）")

                # 句子级时间戳
                if not is_async and 'result' in dir() and result.get("sentences"):
                    st.markdown("---")
                    st.markdown("### ⏱️ 时间戳详情")
                    with st.expander("展开查看句子级时间戳", expanded=True):
                        for sent in result["sentences"]:
                            begin = sent.get("begin_time", "?")
                            end = sent.get("end_time", "?")
                            txt = sent.get("text", "")
                            st.text(f"[{begin}ms - {end}ms]  {txt}")

                    words = result.get("words", [])
                    if words:
                        with st.expander("展开查看词级时间戳"):
                            for w in words[:30]:
                                begin = w.get("begin_time", "?")
                                end = w.get("end_time", "?")
                                txt = w.get("text", "")
                                st.text(f"[{begin}ms - {end}ms]  {txt}")

            except Exception as e:
                error_msg = str(e)
                if "401" in error_msg:
                    st.error("API Key 无效，请检查系统设置")
                else:
                    st.error(f"识别失败: {error_msg}")

# 清理临时文件
if source_type == "file" and audio_source and os.path.exists(audio_source):
    try:
        # 延迟清理，让用户先看到结果
        pass
    except Exception:
        pass
