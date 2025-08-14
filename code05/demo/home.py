"""
 * @author: zkyuan
 * @date: 2025/8/14 16:06
 * @description:
"""

import streamlit as st


def home():
    st.markdown("""
    # 这里是主页
    """)
    st.title("🏠AI人工智能")
    st.caption("这是解释性文字")

    st.markdown(
        """
        ### 1  page1  \n
         - 📝 eg1：...... \n
         - 📝 eg2：...... \n

        ### 2  page2 \n
         - 📢 ...... \n
         - 📢 ...... \n

        ### end 💬 说明

        ❌ 大bug改不了、小bug不用改。\n
         --- 
        """
    )


if __name__ == "__main__":

    home()
