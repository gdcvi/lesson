"""首页 - 项目介绍和使用指南"""
import streamlit as st
from utils.ui_helpers import apply_custom_css, show_api_key_check
from config.settings import COLORS

apply_custom_css()

# ==================== Hero Banner ====================
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {COLORS['primary']} 0%, #1565C0 50%, #0D47A1 100%);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 24px;
    color: white;
">
    <h1 style="font-size: 36px; font-weight: 800; margin: 0 0 12px 0; letter-spacing: -0.5px;">
        🤖 多模态AI智能助手
    </h1>
    <p style="font-size: 18px; margin: 0 0 20px 0; opacity: 0.9; line-height: 1.6;">
        基于阿里云 DashScope 通义千问大模型，集成 RAG 文档问答、文生图、图片解读、<br>
        图生视频、文生音频、音频识别、数据分析等七大核心功能。
    </p>
    <div style="display: flex; gap: 12px; flex-wrap: wrap;">
        <span style="background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px;">LLM 对话</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px;">RAG 检索</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px;">文生图</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px;">图片解读</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px;">图生视频</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px;">TTS/ASR</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px;">数据分析</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px;">知识库管理</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not show_api_key_check():
    st.stop()

# ==================== 功能导航卡片 ====================
st.markdown("### 🎯 核心功能")

features = [
    ("📚", "知识库管理", "创建知识库、上传文档，构建持久化 RAG 知识库", "pages/10_📚_知识库管理.py"),
    ("💬", "RAG 文档问答", "基于知识库或临时文档进行智能检索问答，支持流式输出和引用来源", "pages/02_📚_RAG文档问答.py"),
    ("🎨", "文生图", "用文字描述创作精美图片，支持方形/竖屏/横屏多种尺寸，写实/动漫/油画等风格预设", "pages/03_🎨_文生图.py"),
    ("🖼️", "图片解读", "AI 视觉理解，支持 URL 和本地上传，可进行详细描述、OCR 文字提取、情感分析", "pages/04_🖼️_图片解读.py"),
    ("🎬", "图生视频", "上传静态图片并描述动作，AI 生成动态视频，支持多种动作模板", "pages/05_🎬_图生视频.py"),
    ("🔊", "文生音频", "文字转自然语音，6 种音色可选，支持语速(0.5-2x)、音量(0-100)调节", "pages/06_🔊_文生音频.py"),
    ("🎤", "音频生文", "语音转文字，支持 WAV/MP3/FLAC 等格式，中英文混合识别", "pages/07_🎤_音频生文.py"),
    ("📊", "Excel 助手", "上传 CSV/Excel 文件，自动解析数据，生成折线图、柱状图、饼图等可视化图表", "pages/09_📊_Excel助手.py"),
]

# 使用 3 列布局展示卡片
cols = st.columns(3)
for idx, (icon, title, desc, nav_page) in enumerate(features):
    with cols[idx % 3]:
        st.markdown(f"""
        <div style="
            border: 2px solid #e8ecf0;
            border-radius: 14px;
            padding: 28px 22px;
            margin-bottom: 16px;
            text-align: center;
            background: linear-gradient(180deg, #ffffff 0%, #fafcff 100%);
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            transition: all 0.3s ease;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 44px; margin-bottom: 14px;">{icon}</div>
            <div style="font-size: 18px; font-weight: 700; color: #212121; margin-bottom: 10px;">{title}</div>
            <div style="font-size: 13px; color: #757575; line-height: 1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("进入 →", key=f"home_nav_{idx}", use_container_width=True,
                  on_click=lambda p=nav_page: st.session_state.update({"_nav": p}))

# ==================== 快速开始 ====================
st.markdown("---")
st.markdown("### 🚀 快速开始")

step_cols = st.columns(3, gap="large")

with step_cols[0]:
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 28px 20px;
        background: white;
        border-radius: 14px;
        border: 1px solid #e8ecf0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    ">
        <div style="
            width: 48px; height: 48px; border-radius: 50%;
            background: {COLORS['primary']}; color: white;
            font-size: 22px; font-weight: 800;
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 16px auto;
        ">1</div>
        <div style="font-size: 17px; font-weight: 700; margin-bottom: 8px; color: #212121;">配置 API Key</div>
        <div style="font-size: 13px; color: #757575; line-height: 1.6;">
            访问 <a href="https://dashscope.console.aliyun.com/" target="_blank" style="color: {COLORS['primary']};">阿里云 DashScope</a>
            获取 API Key，在系统设置页面填入并保存。
        </div>
    </div>
    """, unsafe_allow_html=True)

with step_cols[1]:
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 28px 20px;
        background: white;
        border-radius: 14px;
        border: 1px solid #e8ecf0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    ">
        <div style="
            width: 48px; height: 48px; border-radius: 50%;
            background: {COLORS['success']}; color: white;
            font-size: 22px; font-weight: 800;
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 16px auto;
        ">2</div>
        <div style="font-size: 17px; font-weight: 700; margin-bottom: 8px; color: #212121;">选择功能模块</div>
        <div style="font-size: 13px; color: #757575; line-height: 1.6;">
            从上方卡片或左侧导航菜单选择您需要的功能页面。
        </div>
    </div>
    """, unsafe_allow_html=True)

with step_cols[2]:
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 28px 20px;
        background: white;
        border-radius: 14px;
        border: 1px solid #e8ecf0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    ">
        <div style="
            width: 48px; height: 48px; border-radius: 50%;
            background: {COLORS['warning']}; color: white;
            font-size: 22px; font-weight: 800;
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 16px auto;
        ">3</div>
        <div style="font-size: 17px; font-weight: 700; margin-bottom: 8px; color: #212121;">开始创作</div>
        <div style="font-size: 13px; color: #757575; line-height: 1.6;">
            按各页面的引导输入内容，AI 即刻为您生成结果。
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== 技术栈 ====================
st.markdown("---")
st.markdown("### 🛠️ 技术栈")

tech_data = [
    ("🤖", "大语言模型", "通义千问 Qwen-Plus/Max", "#1E88E5"),
    ("👁️", "视觉模型", "Qwen-VL-Plus/Max", "#9C27B0"),
    ("🗄️", "向量数据库", "ChromaDB + Embedding", "#FF9800"),
    ("🌐", "Web 框架", "Streamlit 1.28+", "#4CAF50"),
    ("🔌", "API 平台", "阿里云 DashScope", "#F44336"),
    ("📊", "数据处理", "Pandas + LangChain", "#00BCD4"),
]

tech_cols = st.columns(6)
for i, (icon, name, detail, color) in enumerate(tech_data):
    with tech_cols[i]:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 18px 8px;
            background: {color}08;
            border-radius: 12px;
            border: 1px solid {color}25;
        ">
            <div style="font-size: 30px; margin-bottom: 8px;">{icon}</div>
            <div style="font-size: 13px; font-weight: 700; color: #333;">{name}</div>
            <div style="font-size: 11px; color: #888; margin-top: 4px;">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

# ==================== 支持格式 ====================
st.markdown("---")
st.markdown("### 📁 支持的文件格式")

fmt_cols = st.columns(5, gap="medium")
formats = [
    ("📄", "文档", "PDF / TXT / DOCX / MD / CSV / XLSX", COLORS["primary"]),
    ("🖼️", "图片", "JPG / PNG / WEBP / GIF", COLORS["success"]),
    ("🎵", "音频", "WAV / MP3 / FLAC / M4A / OGG", COLORS["warning"]),
    ("🎬", "视频", "MP4 / AVI / MOV", COLORS["error"]),
    ("📊", "表格", "CSV / XLSX / XLS", "#9C27B0"),
]
for i, (icon, name, detail, color) in enumerate(formats):
    with fmt_cols[i]:
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 20px 12px;
            background: white;
            border-radius: 12px;
            border: 2px solid {color}30;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        ">
            <div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>
            <div style="font-size: 14px; font-weight: 700; color: #333; margin-bottom: 6px;">{name}</div>
            <div style="font-size: 12px; color: #777; line-height: 1.5;">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

# 底部
st.markdown("<br>", unsafe_allow_html=True)
st.caption("💡 提示：首次使用请在 **系统设置** 页面配置 API Key。如需帮助，请查看上方快速开始指南。")
