"""
 * @author: zkyuan
 * @date: 2025/8/14 15:50
 * @description: streamlit入门
"""
import streamlit as st

# 页面打印markdown
st.markdown('第一个Streamlit应用')

# 网页标题
st.title('学习streamlit框架')

# 展示一级标题
st.header('1. 安装')

# 显示文本
st.text('一条简单的命令即可安装')

st.markdown(
"""
> 在python环境中安装依赖，因为这是国外的源，所以可以安装很慢，期间也可能会安装失败，出现问题可以重复执行安装多试几次，或者是开科学上网 \n
> 安装成功后，输入命令：streamlit hello 启动streamlit，这里有streamlit的一些demo案例\n
"""
)
# 解释性文字
st.caption("下面的安装命令")
code1 = '''pip install streamlit'''
st.code(code1, language='bash')

# 一级标题
st.header('2. 使用')

# 二级标题
st.subheader('2.1 生成 Markdown 文档')

# 纯文本
st.text('导入 streamlit 后，就可以直接使用 st.markdown() 初始化')

# 代码，有高亮效果
code2 = '''
import streamlit as st
st.markdown('Streamlit Demo')
'''
st.code(code2, language='python')
