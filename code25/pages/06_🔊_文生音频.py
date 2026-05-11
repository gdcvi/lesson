"""文生音频（TTS）页面"""
import os
import time
import streamlit as st
from modules.audio_service import TTSService
from config.settings import TTS_MODELS, TTS_VOICES
from utils.ui_helpers import apply_custom_css, show_api_key_check
from utils.file_utils import format_file_size

apply_custom_css()

if not show_api_key_check():
    st.stop()

tts_service = TTSService()

# 初始化 session_state
if "tts_history" not in st.session_state:
    st.session_state.tts_history = []

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 🔊 文生音频配置")

    model_name = st.selectbox("🤖 TTS 模型", TTS_MODELS, key="tts_model")

    st.markdown("#### 🎤 音色选择")
    voice_labels = [f"{v_id} - {v_desc}" for v_id, v_desc in TTS_VOICES.items()]
    voice_ids = list(TTS_VOICES.keys())
    selected_voice_label = st.selectbox("选择音色", voice_labels, key="tts_voice")
    selected_voice = voice_ids[voice_labels.index(selected_voice_label)]

    st.markdown("#### ⚡ 语速")
    speech_rate = st.slider("语速倍率", 0.5, 2.0, 1.0, 0.1, key="tts_speed")

    st.markdown("#### 🔊 音量")
    volume = st.slider("音量", 0, 100, 50, key="tts_volume")

    st.markdown("#### 🎵 音频格式")
    audio_format_choice = st.radio("格式", ["MP3（推荐）", "WAV"], key="tts_format")

    st.markdown("#### 📝 文本模板")
    text_templates = {
        "自定义": "",
        "新闻播报": "各位听众朋友们，大家好。今天是2026年5月11日，欢迎收听今天的新闻播报。人工智能技术正在深刻地改变着我们的世界，让我们一起来关注最新的科技动态。",
        "有声书朗读": "春天来了，万物复苏。清晨的阳光透过树叶洒在小路上，鸟儿在枝头欢快地歌唱。微风吹过，带来阵阵花香，让人心旷神怡。",
        "客服语音": "您好，欢迎致电客服中心。业务咨询请按1，订单查询请按2，投诉建议请按3，人工服务请按0。为了保证服务质量，您的通话可能会被录音。",
        "产品介绍": "这款产品采用了最新的AI技术，能够帮助您提高工作效率，节省宝贵的时间。它具有简洁易用的界面，强大的功能，以及安全可靠的数据保护机制。",
    }
    template_choice = st.selectbox("选择模板", list(text_templates.keys()), key="tts_template")

    st.markdown("---")
    st.caption("💡 提示：文本建议 5000 字以内")

# ==================== 主区域 ====================
st.title("🔊 AI 文生音频")
st.caption("将文字转换为自然流畅的语音播报")

if template_choice != "自定义" and text_templates[template_choice]:
    text_input = st.text_area(
        "✍️ 输入文本",
        value=text_templates[template_choice],
        height=200,
        key="tts_text"
    )
else:
    text_input = st.text_area(
        "✍️ 输入文本",
        placeholder="请输入要转换为语音的文字...\n支持中英文混合，建议分段输入",
        height=200,
        key="tts_text_custom"
    )

char_count = len(text_input)
st.caption(f"字符数: {char_count} / 5000")
if char_count > 5000:
    st.warning("文本过长，建议分段处理")

generate_btn = st.button("🔊 生成语音", type="primary", use_container_width=True, disabled=(char_count == 0 or char_count > 5000))

if generate_btn:
    if not text_input.strip():
        st.error("请输入文本")
    else:
        with st.spinner("正在合成语音..."):
            start_time = time.time()
            try:
                from dashscope.audio.tts_v2 import AudioFormat
                audio_format = AudioFormat.MP3_24000HZ_MONO_256KBPS
                if audio_format_choice == "WAV":
                    audio_format = AudioFormat.WAV_22050HZ_MONO_16BIT

                save_path = tts_service.synthesize(
                    text=text_input,
                    voice=selected_voice,
                    model=model_name,
                    speech_rate=speech_rate,
                    volume=volume,
                    audio_format=audio_format,
                )

                elapsed = time.time() - start_time
                st.success(f"语音合成成功！耗时 {elapsed:.1f} 秒")

                if save_path and os.path.exists(save_path):
                    st.audio(save_path)
                    fsize = format_file_size(os.path.getsize(save_path))
                    st.caption(f"文件大小: {fsize}")

                    file_ext = os.path.splitext(save_path)[1]
                    mime_type = "audio/mpeg" if file_ext == ".mp3" else "audio/wav"
                    with open(save_path, "rb") as f:
                        st.download_button(
                            f"⬇ 下载{file_ext.upper()}",
                            f.read(),
                            f"tts_{int(time.time())}{file_ext}",
                            mime_type
                        )

                    # 添加到历史
                    st.session_state.tts_history.append({
                        "text": text_input[:100],
                        "voice": voice_labels[voice_ids.index(selected_voice)],
                        "local_path": save_path,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    })

            except Exception as e:
                st.error(f"语音合成失败: {str(e)}")

# 生成历史
if st.session_state.tts_history:
    st.markdown("---")
    st.markdown("### 📋 生成历史")
    with st.expander("展开查看历史", expanded=False):
        for i, item in enumerate(reversed(st.session_state.tts_history[-10:])):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.caption(f"{item['timestamp']} — {item['text']}...")
            with c2:
                st.caption(f"音色: {item['voice']}")
            with c3:
                if item["local_path"] and os.path.exists(item["local_path"]):
                    with open(item["local_path"], "rb") as f:
                        ext = os.path.splitext(item["local_path"])[1]
                        st.download_button(
                            "⬇", f.read(),
                            f"history_{i}{ext}",
                            "audio/mpeg" if ext == ".mp3" else "audio/wav",
                            key=f"tts_hist_{i}"
                        )
        if st.button("清空历史", key="tta_clear_hist"):
            st.session_state.tts_history = []
            st.rerun()
