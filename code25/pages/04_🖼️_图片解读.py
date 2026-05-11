"""图片解读页面"""
import os
import streamlit as st
from modules.llm_service import get_llm_service
from config.settings import VISION_MODELS, ALLOWED_IMAGE_EXTENSIONS, MAX_FILE_SIZE_IMAGE
from utils.ui_helpers import apply_custom_css, show_api_key_check
from utils.file_utils import format_file_size

apply_custom_css()

if not show_api_key_check():
    st.stop()

llm_service = get_llm_service()

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 🖼️ 图片解读配置")

    model_name = st.selectbox("🤖 视觉模型", VISION_MODELS, key="vis_model")

    st.markdown("#### 📋 问题模板")
    question_templates = {
        "详细描述": "请详细描述这张图片的内容，包括主体、场景、色彩和氛围。",
        "内容分析": "请从构图、光线、色彩三个方面分析这张图片。",
        "OCR 文字提取": "这张图片中有文字吗？如果有，请把所有的文字提取出来。",
        "情感分析": "请分析这张图片传达的情感和氛围。",
        "自定义": "",
    }
    template_choice = st.selectbox("选择模板", list(question_templates.keys()), key="q_template")
    custom_question = question_templates[template_choice]

    st.markdown("---")
    st.markdown("#### 📖 使用提示")
    st.caption("- 支持 JPG/PNG/WEBP/GIF 格式")
    st.caption("- 本地图片最大 10MB")
    st.caption("- URL 图片需公网可访问")

# ==================== 主区域 ====================
st.title("🖼️ AI 图片解读")
st.caption("让 AI 看懂您的图片——支持 URL 和本地上传两种方式")

tab_url, tab_local = st.tabs(["🌐 图片 URL", "📁 本地上传"])

question = ""
image_input = None
input_mode = "url"

with tab_url:
    image_url = st.text_input(
        "输入图片 URL",
        placeholder="https://example.com/image.jpg",
        key="vis_url"
    )
    if image_url:
        try:
            st.image(image_url, caption="图片预览", use_container_width=True)
        except Exception:
            st.warning("无法预览此 URL 的图片，但仍可尝试分析")
    input_mode = "url"
    image_input = image_url

with tab_local:
    uploaded_file = st.file_uploader(
        "上传图片文件",
        type=[ext.lstrip('.') for ext in ALLOWED_IMAGE_EXTENSIONS],
        key="vis_upload"
    )
    if uploaded_file:
        if uploaded_file.size > MAX_FILE_SIZE_IMAGE:
            st.error(f"文件大小超过 10MB 限制（当前: {format_file_size(uploaded_file.size)}）")
        else:
            st.image(uploaded_file, caption=f"已上传: {uploaded_file.name}", use_container_width=True)
            # 保存临时文件
            temp_dir = os.path.join(os.path.dirname(__file__), "..", "data", "temp_docs")
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            input_mode = "local"
            image_input = temp_path

# 提问输入
st.markdown("---")
st.markdown("### ❓ 提问")

if template_choice == "自定义" or not custom_question:
    question = st.text_area(
        "请输入您的问题",
        placeholder="请描述这张图片的内容...",
        height=80,
        key="vis_question"
    )
else:
    question = st.text_area(
        "问题（可修改）",
        value=custom_question,
        height=80,
        key="vis_question_prefilled"
    )

analyze_btn = st.button("🔍 开始分析", type="primary", use_container_width=True)

if analyze_btn:
    if not question.strip():
        st.error("请输入问题")
    elif not image_input:
        st.error("请提供图片 URL 或上传本地图片")
    else:
        with st.spinner("AI 正在分析图片..."):
            try:
                if input_mode == "url":
                    result = llm_service.analyze_image_by_url(image_input, question, model_name)
                else:
                    result = llm_service.analyze_image_by_local(image_input, question, model_name)

                st.markdown("---")
                st.markdown("### 📝 分析结果")
                st.markdown(result)

                # 清理本地临时文件
                if input_mode == "local" and os.path.exists(image_input):
                    try:
                        os.remove(image_input)
                    except Exception:
                        pass

            except Exception as e:
                error_msg = str(e)
                if "401" in error_msg:
                    st.error("API Key 无效，请检查系统设置")
                else:
                    st.error(f"分析失败: {error_msg}")
