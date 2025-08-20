"""
 * @author: zkyuan
 * @date: 2025/8/19 16:58
 * @description: streamlit整合AI大模型
"""
import streamlit as st
import os

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def home():
    st.title("🏠鲁班大先生智能助手")
    st.caption("使用前请在侧边栏填写参数")

    if "base_url" not in st.session_state:
        st.session_state['base_url'] = os.getenv('DEEPSEEK_BASE_URL')

    if "api_key" not in st.session_state:
        st.session_state['api_key'] = os.getenv('DEEPSEEK_API_KEY')

    # 侧边栏输入
    st.session_state.base_url = st.sidebar.text_input('Base URL', st.session_state.base_url)
    st.session_state.api_key = st.sidebar.text_input('API Key', st.session_state.api_key, type='password')

    st.markdown(
        """
        **体验大模型功能**
        ## 使用说明
        * 请在侧边栏填写`API Key`，如果没有请在[OpenAI官网](https://platform.openai.com/account/api-keys)获取，如果需要使用代理，请修改`base_url`\n
        * 也可以使用其他大模型的OpenAI接口标准的base_url和api-key
        * 格式如下：\n
            ```json
            {
                "base_url" : "https://xxx",
                "api_key" : "sk-xxxx" 
            }
            ```
        * 接下来在侧边栏选择需要使用的页面。
        ---------------------------------------------------------
        """
    )
    st.markdown(
        """
        ### 💬chatchat page  \n
        该页面用于文本对话，选择模型，输入问题，得到回答。\n
        
        ### 💬assistant page  \n
        AI智能助手
        """
    )


if __name__ == "__main__":
    home()