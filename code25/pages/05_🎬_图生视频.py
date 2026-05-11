"""图生视频页面"""
import os
import time
import streamlit as st
from modules.video_service import VideoService
from config.settings import I2V_MODELS, ALLOWED_IMAGE_EXTENSIONS, MAX_FILE_SIZE_IMAGE
from utils.ui_helpers import apply_custom_css, show_api_key_check
from utils.file_utils import format_file_size

apply_custom_css()

if not show_api_key_check():
    st.stop()

video_service = VideoService()

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 🎬 图生视频配置")

    model_name = st.selectbox("🤖 视频模型", I2V_MODELS, key="i2v_model")

    st.markdown("#### ⏱️ 视频时长")
    duration = st.selectbox("时长（秒）", [None, 2, 4, 6],
                            format_func=lambda x: "默认" if x is None else f"{x} 秒",
                            key="i2v_duration")

    st.markdown("#### 📝 动作模板")
    motion_templates = {
        "自定义": "",
        "风吹动": "微风吹拂，树叶轻轻摇摆，水面泛起涟漪",
        "水流": "水流缓缓流动，波纹扩散开来",
        "镜头推近": "镜头缓慢推近，画面由远及近",
        "镜头横移": "镜头从左向右缓慢移动，展现全景",
        "人物动作": "人物自然地动起来，表情生动自然",
    }
    template_choice = st.selectbox("选择模板", list(motion_templates.keys()), key="motion_template")

    st.markdown("---")
    st.markdown("#### ℹ️ 注意事项")
    st.caption("- 生成时间约 2-5 分钟")
    st.caption("- 支持 JPG/PNG 格式")
    st.caption("- 图片建议小于 5MB")
    st.caption("- 请耐心等待，不要切换页面")

# ==================== 主区域 ====================
st.title("🎬 AI 图生视频")
st.caption("上传一张静态图片，用文字描述动作，AI 为您生成动态视频")

st.markdown("### 第 1 步：📤 上传源图片")
uploaded_file = st.file_uploader(
    "选择图片文件",
    type=[ext.lstrip('.') for ext in ALLOWED_IMAGE_EXTENSIONS],
    key="i2v_upload",
    label_visibility="collapsed"
)

st.markdown("### 第 2 步：✍️ 描述动作")
if template_choice != "自定义" and motion_templates[template_choice]:
    motion_prompt = st.text_area(
        "动作描述",
        value=motion_templates[template_choice],
        height=80,
        key="i2v_prompt"
    )
else:
    motion_prompt = st.text_area(
        "动作描述",
        placeholder="请描述希望画面如何动起来...\n例如：狗开心地摇着尾巴，女孩伸手去摸狗",
        height=80,
        key="i2v_prompt_custom"
    )

# 图片预览
if uploaded_file:
    if uploaded_file.size > MAX_FILE_SIZE_IMAGE:
        st.error(f"图片过大（{format_file_size(uploaded_file.size)}），请选择小于 10MB 的图片")
    else:
        st.image(uploaded_file, caption="源图片预览", width=400)

generate_btn = st.button("🎬 生成视频", type="primary", use_container_width=True)

if generate_btn:
    if not uploaded_file:
        st.error("请先上传图片")
    elif not motion_prompt.strip():
        st.error("请输入动作描述")
    else:
        # 保存上传的图片作为临时文件
        temp_dir = os.path.join(os.path.dirname(__file__), "..", "data", "temp_docs")
        os.makedirs(temp_dir, exist_ok=True)
        temp_img_path = os.path.join(temp_dir, f"i2v_input_{int(time.time())}.{uploaded_file.name.split('.')[-1]}")
        with open(temp_img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 图生视频需要 URL，这里尝试用 base64 数据 URL
        # 由于 VideoSynthesis 需要公网 URL，这里我们引导用户使用公网图片
        st.warning("⚠️ 图生视频需要公网可访问的图片URL。请确保使用图片URL而非本地上传。")
        st.info("📋 替代方案：将图片上传到图床后，使用URL调用。或者在文生图页面先生成图片（会自动生成公网URL）。")

        # 清理临时文件
        try:
            os.remove(temp_img_path)
        except Exception:
            pass

# 如果用户提供图片URL
st.markdown("---")
st.markdown("### 🌐 或使用图片 URL")
image_url = st.text_input(
    "图片 URL（需公网可访问）",
    placeholder="https://example.com/image.jpg",
    key="i2v_url"
)

if image_url:
    st.image(image_url, caption="URL 图片预览", width=400)

    url_generate_btn = st.button("🎬 使用 URL 生成视频", type="primary", use_container_width=True)

    if url_generate_btn:
        if not motion_prompt.strip():
            st.error("请输入动作描述")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            start_time = time.time()

            try:
                status_text.info("正在提交生成任务...")
                progress_bar.progress(10)

                # 提交并等待
                result = video_service.generate(
                    img_url=image_url,
                    prompt=motion_prompt,
                    model=model_name,
                    duration=duration,
                )

                elapsed = time.time() - start_time
                progress_bar.progress(100)
                status_text.success(f"视频生成完成！耗时 {elapsed:.0f} 秒")

                if result.get("local_path") and os.path.exists(result["local_path"]):
                    st.video(result["local_path"])
                    fsize = format_file_size(result.get("file_size", 0))
                    st.caption(f"文件大小: {fsize}")
                    with open(result["local_path"], "rb") as f:
                        st.download_button(
                            "⬇ 下载视频", f.read(),
                            f"generated_video_{int(time.time())}.mp4",
                            "video/mp4"
                        )

            except Exception as e:
                progress_bar.progress(100)
                error_msg = str(e)
                if "timeout" in error_msg.lower():
                    st.error("生成超时，请重试或使用更短的时长")
                else:
                    st.error(f"生成失败: {error_msg}")
