"""文生图页面"""
import os
import time
import streamlit as st
from modules.image_service import ImageService
from config.settings import T2I_MODELS, IMAGE_SIZES
from utils.ui_helpers import apply_custom_css, show_api_key_check
from utils.file_utils import format_file_size

apply_custom_css()

if not show_api_key_check():
    st.stop()

# 初始化 session_state
if "t2i_history" not in st.session_state:
    st.session_state.t2i_history = []

image_service = ImageService()

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 🎨 文生图配置")

    model_name = st.selectbox("🤖 模型", T2I_MODELS, key="t2i_model")

    st.markdown("#### 📐 图片尺寸")
    size_labels = list(IMAGE_SIZES.values())
    size_keys = list(IMAGE_SIZES.keys())
    selected_size_label = st.radio("选择尺寸", size_labels, key="t2i_size")
    selected_size = size_keys[size_labels.index(selected_size_label)]

    st.markdown("#### 📊 生成数量")
    n_images = st.selectbox("数量", [1, 2, 4], key="t2i_n")

    st.markdown("#### 🎭 风格预设")
    style_presets = {
        "无（自定义）": "",
        "写实风格": "photorealistic, highly detailed, 8k resolution, ",
        "动漫风格": "anime style, studio ghibli, vibrant colors, ",
        "油画风格": "oil painting, fine art, classical style, ",
        "3D渲染": "3D render, CGI, octane render, highly detailed, ",
        "水墨画": "chinese ink wash painting, watercolor, artistic, ",
        "赛博朋克": "cyberpunk, neon lights, futuristic city, sci-fi, ",
    }
    selected_style = st.selectbox("风格", list(style_presets.keys()), key="t2i_style")

    st.markdown("---")
    st.caption("💡 提示：详细的描述能获得更好的生成效果")

# ==================== 主区域 ====================
st.title("🎨 AI 文生图")
st.caption("用文字描述，AI 为您创作精美图片")

col1, col2 = st.columns([3, 1])

with col1:
    prompt = st.text_area(
        "📝 创作描述 (Prompt)",
        placeholder="请输入您想要的画面描述，越详细越好...\n例如：一只可爱的橘猫坐在窗台上，阳光透过窗户洒在它身上，窗外是蓝天白云",
        height=120,
        key="t2i_prompt"
    )

with col2:
    negative_prompt = st.text_area(
        "🚫 负面提示词（可选）",
        placeholder="blurry, low quality, watermark, text, distorted",
        height=120,
        key="t2i_neg_prompt"
    )

    st.markdown("")

generate_btn = st.button("🎨 开始生成", type="primary", use_container_width=True)

if generate_btn:
    if not prompt.strip():
        st.error("请先输入创作描述")
    else:
        # 应用风格预设
        full_prompt = style_presets[selected_style] + prompt if style_presets[selected_style] else prompt

        with st.spinner(f"正在生成图片（{selected_size}），请稍候..."):
            start_time = time.time()
            try:
                neg = negative_prompt.strip() if negative_prompt.strip() else None
                images = image_service.generate(
                    prompt=full_prompt,
                    negative_prompt=neg,
                    size=selected_size,
                    n=n_images,
                    model=model_name,
                )
                elapsed = time.time() - start_time

                st.success(f"生成完成！耗时 {elapsed:.1f} 秒")

                # 显示图片
                if n_images == 1:
                    col_img, _ = st.columns([2, 1])
                    with col_img:
                        img = images[0]
                        if img["local_path"] and os.path.exists(img["local_path"]):
                            st.image(img["local_path"], use_container_width=True)
                            with open(img["local_path"], "rb") as f:
                                st.download_button("⬇ 下载图片", f.read(),
                                                   f"generated_{int(time.time())}.png",
                                                   "image/png")
                else:
                    cols = st.columns(min(n_images, 2))
                    for i, img in enumerate(images):
                        with cols[i % 2]:
                            if img["local_path"] and os.path.exists(img["local_path"]):
                                st.image(img["local_path"], use_container_width=True)
                                fsize = format_file_size(img.get("file_size", 0))
                                st.caption(f"图片 {i+1} · {fsize}")
                                with open(img["local_path"], "rb") as f:
                                    st.download_button(
                                        f"⬇ 下载", f.read(),
                                        f"generated_{int(time.time())}_{i}.png",
                                        "image/png", key=f"dl_{i}"
                                    )

                # 添加到历史
                for img in images:
                    st.session_state.t2i_history.append({
                        "prompt": full_prompt[:100],
                        "local_path": img["local_path"],
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    })

            except Exception as e:
                st.error(f"生成失败: {str(e)}")

# 生成历史
if st.session_state.t2i_history:
    st.markdown("---")
    st.markdown("### 📋 生成历史")
    with st.expander("展开查看历史", expanded=False):
        for i, item in enumerate(reversed(st.session_state.t2i_history[-10:])):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.caption(f"{item['timestamp']} — {item['prompt']}...")
            with c2:
                if item["local_path"] and os.path.exists(item["local_path"]):
                    with open(item["local_path"], "rb") as f:
                        st.download_button("⬇", f.read(),
                                           f"history_{i}.png", "image/png",
                                           key=f"hist_dl_{i}")
        if st.button("清空历史", key="clear_hist"):
            st.session_state.t2i_history = []
            st.rerun()
