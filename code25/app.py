"""多模态AI智能助手 - 主应用入口"""
import streamlit as st
from config.settings import PAGE_TITLE, PAGE_ICON, COLORS
from utils.ui_helpers import apply_custom_css, show_api_key_check

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# 侧边栏
with st.sidebar:
    st.markdown("## 🤖 多模态AI助手")
    st.markdown("---")
    if show_api_key_check():
        st.success("✅ API 已配置")
    st.markdown("---")
    st.caption("请使用上方导航菜单选择功能页面")

# ==================== Hero Banner ====================
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {COLORS['primary']} 0%, #1565C0 50%, #0D47A1 100%);
    border-radius: 16px;
    padding: 36px 48px;
    margin-bottom: 28px;
    color: white;
">
    <h1 style="font-size: 38px; font-weight: 800; margin: 0 0 10px 0;">
        🤖 多模态AI智能助手
    </h1>
    <p style="font-size: 18px; margin: 0 0 18px 0; opacity: 0.9;">
        一站式 AI 创作与交互平台，七大核心功能覆盖文本、图像、语音、视频全模态
    </p>
    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        <span style="background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 18px; font-size: 13px;">RAG 文档问答</span>
        <span style="background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 18px; font-size: 13px;">文生图</span>
        <span style="background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 18px; font-size: 13px;">图片解读</span>
        <span style="background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 18px; font-size: 13px;">图生视频</span>
        <span style="background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 18px; font-size: 13px;">文生音频</span>
        <span style="background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 18px; font-size: 13px;">音频生文</span>
        <span style="background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 18px; font-size: 13px;">数据分析</span>
        <span style="background: rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 18px; font-size: 13px;">知识库管理</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 功能卡片 ====================
st.markdown("### 🎯 功能导航")

features = [
    ("📚", "知识库管理", "创建知识库、上传文档，构建持久化 RAG 知识库", "pages/10_📚_知识库管理.py"),
    ("💬", "RAG 文档问答", "基于知识库或临时文档进行智能检索问答", "pages/02_📚_RAG文档问答.py"),
    ("🎨", "文生图", "用文字描述创作精美图片，支持多种尺寸和风格预设", "pages/03_🎨_文生图.py"),
    ("🖼️", "图片解读", "AI 看图说话，支持 URL 和本地上传，可 OCR 识别", "pages/04_🖼️_图片解读.py"),
    ("🎬", "图生视频", "让静态图片动起来，AI 生成动态视频", "pages/05_🎬_图生视频.py"),
    ("🔊", "文生音频", "文字转语音，6 种音色可选，支持语速调节", "pages/06_🔊_文生音频.py"),
    ("🎤", "音频生文", "语音转文字，支持中英文混合识别", "pages/07_🎤_音频生文.py"),
    ("📊", "Excel 助手", "上传表格文件，自动分析数据，生成可视化图表", "pages/09_📊_Excel助手.py"),
]

cols = st.columns(3)
for idx, (icon, title, desc, nav_page) in enumerate(features):
    with cols[idx % 3]:
        st.markdown(f"""
        <div style="
            border: 2px solid #e8ecf0;
            border-radius: 14px;
            padding: 26px 20px;
            margin-bottom: 14px;
            text-align: center;
            background: linear-gradient(180deg, #ffffff 0%, #fafcff 100%);
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 40px; margin-bottom: 12px;">{icon}</div>
            <div style="font-size: 17px; font-weight: 700; color: #212121; margin-bottom: 8px;">{title}</div>
            <div style="font-size: 13px; color: #757575; line-height: 1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入 →", key=f"nav_{idx}", use_container_width=True):
            st.switch_page(nav_page)

# ==================== 底部 ====================
st.markdown("---")
st.markdown("#### 🛠️ 技术栈")
tc1, tc2, tc3, tc4, tc5, tc6 = st.columns(6)
with tc1:
    st.metric("LLM", "Qwen")
with tc2:
    st.metric("视觉", "qwen-vl")
with tc3:
    st.metric("向量库", "ChromaDB")
with tc4:
    st.metric("框架", "Streamlit")
with tc5:
    st.metric("平台", "DashScope")
with tc6:
    st.metric("数据", "Pandas")

st.caption("首次使用请在 **系统设置** 页面配置 API Key。")
