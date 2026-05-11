"""UI 工具函数 —— 统一界面样式和组件"""
import streamlit as st
from config.settings import COLORS, DASHSCOPE_API_KEY


def apply_custom_css():
    """注入全局自定义CSS样式"""
    st.markdown(f"""
    <style>
    /* 全局字体和背景 */
    .stApp {{
        background-color: {COLORS["bg_light"]};
    }}

    /* 卡片样式 */
    .custom-card {{
        border: 1px solid {COLORS["card_border"]};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }}
    .custom-card:hover {{
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }}

    /* 功能导航卡片 */
    .feature-card {{
        border: 2px solid {COLORS["card_border"]};
        border-radius: 14px;
        padding: 28px 20px;
        margin-bottom: 16px;
        text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    .feature-card:hover {{
        border-color: {COLORS["primary"]};
        box-shadow: 0 8px 25px rgba(30,136,229,0.15);
        transform: translateY(-3px);
    }}
    .feature-icon {{
        font-size: 42px;
        margin-bottom: 12px;
    }}
    .feature-title {{
        font-size: 18px;
        font-weight: 700;
        color: #212121;
        margin-bottom: 8px;
    }}
    .feature-desc {{
        font-size: 13px;
        color: #757575;
        line-height: 1.5;
    }}

    /* 按钮优化 */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    /* 侧边栏优化 */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #f8faff 0%, #ffffff 100%);
        border-right: 1px solid {COLORS["card_border"]};
    }}

    /* 聊天气泡 */
    .chat-bubble {{
        border-radius: 12px;
        padding: 14px 18px;
        margin: 8px 0;
        line-height: 1.6;
    }}

    /* 状态指示器 */
    .status-dot {{
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
    }}
    .status-dot.active {{ background-color: {COLORS["success"]}; }}
    .status-dot.inactive {{ background-color: {COLORS["error"]}; }}

    /* 模型标签 */
    .model-tag {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
        background: #E3F2FD;
        color: {COLORS["primary"]};
    }}
    </style>
    """, unsafe_allow_html=True)


def show_api_key_check():
    """检查并提示 API Key 配置状态"""
    if not DASHSCOPE_API_KEY:
        st.error("⚠️ 未检测到 API Key！请在系统设置页面配置 **DASHSCOPE_API_KEY**，或创建 `.env` 文件。")
        if st.button("前往系统设置", key="goto_settings_from_check"):
            st.switch_page("pages/08_⚙️_系统设置.py")
        return False
    return True


def render_card(content: str, border_color: str = None, padding: str = "20px"):
    """渲染自定义卡片"""
    color = border_color or COLORS["card_border"]
    st.markdown(f"""
    <div style="
        border: 1px solid {color};
        border-radius: 12px;
        padding: {padding};
        margin-bottom: 16px;
        background: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_feature_card(icon: str, title: str, description: str, nav_page: str = None):
    """渲染功能导航卡片"""
    card_html = f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """
    return card_html


def render_status_badge(status: str, text: str):
    """渲染状态徽章"""
    color_map = {
        "success": COLORS["success"],
        "warning": COLORS["warning"],
        "error": COLORS["error"],
        "info": COLORS["primary"],
    }
    color = color_map.get(status, COLORS["primary"])
    st.markdown(f"""
    <span style="
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 500;
        background: {color}15;
        color: {color};
        border: 1px solid {color}40;
    ">{text}</span>
    """, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = "", description: str = ""):
    """渲染区域标题"""
    header = f"{icon} {title}" if icon else title
    st.markdown(f"### {header}")
    if description:
        st.caption(description)
    st.divider()


def spaced_columns(ratio: list) -> list:
    """创建等比例列布局"""
    return st.columns(ratio)
