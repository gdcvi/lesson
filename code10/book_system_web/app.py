import streamlit as st
from library import Library
from book import Book

# 设置页面配置
st.set_page_config(
    page_title="图书管理系统",
    page_icon="📚",
    layout="wide"
)

# 初始化图书馆对象
if 'library' not in st.session_state:
    st.session_state.library = Library()

# 页面标题
st.title("📚 图书管理系统")

# 侧边栏导航
st.sidebar.header("导航")
page = st.sidebar.selectbox(
    "选择功能",
    ["首页", "查看所有图书", "添加图书", "搜索图书", "借阅图书", "归还图书", "查看已借出图书"]
)

# 主页面内容
if page == "首页":
    st.header("欢迎使用图书管理系统")
    st.write("""
    这是一个简单的图书管理系统，您可以：
    - 查看所有图书
    - 添加新图书
    - 搜索图书
    - 借阅图书
    - 归还图书
    - 查看已借出的图书
    """)
    
    # 显示统计信息
    all_books = st.session_state.library.show_all_books()
    borrowed_books = st.session_state.library.show_borrowed_books()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="总图书数", value=len(all_books))
    with col2:
        st.metric(label="已借出图书数", value=len(borrowed_books))

elif page == "查看所有图书":
    st.header("所有图书")
    
    all_books = st.session_state.library.show_all_books()
    
    if all_books:
        for i, book in enumerate(all_books, 1):
            status = "🟢 可借阅" if not book.is_borrowed else "🔴 已借出"
            st.info(f"**{i}. {book.title}** - {book.author} (ISBN: {book.isbn}) [{status}]")
    else:
        st.warning("暂无图书。")

elif page == "添加图书":
    st.header("添加图书")
    
    with st.form("add_book_form"):
        title = st.text_input("书名 *", placeholder="请输入书名")
        author = st.text_input("作者 *", placeholder="请输入作者")
        isbn = st.text_input("ISBN *", placeholder="请输入ISBN")
        
        submitted = st.form_submit_button("添加图书")
        
        if submitted:
            if title and author and isbn:
                book = Book(title, author, isbn)
                message = st.session_state.library.add_book(book)
                st.success(message)
            else:
                st.error("请填写完整的图书信息！")

elif page == "搜索图书":
    st.header("搜索图书")
    
    keyword = st.text_input("请输入搜索关键词（书名或作者）", placeholder="输入关键词...")
    
    if keyword:
        results = st.session_state.library.search_book(keyword)
        
        if results:
            st.success(f"找到 {len(results)} 本相关图书：")
            for i, book in enumerate(results, 1):
                status = "🟢 可借阅" if not book.is_borrowed else "🔴 已借出"
                st.info(f"**{i}. {book.title}** - {book.author} (ISBN: {book.isbn}) [{status}]")
        else:
            st.warning("未找到相关图书。")

elif page == "借阅图书":
    st.header("借阅图书")
    
    isbn = st.text_input("请输入要借阅的图书ISBN", placeholder="输入ISBN...")
    
    if isbn:
        if st.button("借阅图书"):
            success, message = st.session_state.library.borrow_book(isbn)
            if success:
                st.success(message)
            else:
                st.error(message)

elif page == "归还图书":
    st.header("归还图书")
    
    isbn = st.text_input("请输入要归还的图书ISBN", placeholder="输入ISBN...")
    
    if isbn:
        if st.button("归还图书"):
            success, message = st.session_state.library.return_book(isbn)
            if success:
                st.success(message)
            else:
                st.error(message)

elif page == "查看已借出图书":
    st.header("已借出的图书")
    
    borrowed_books = st.session_state.library.show_borrowed_books()
    
    if borrowed_books:
        for i, book in enumerate(borrowed_books, 1):
            st.error(f"**{i}. {book.title}** - {book.author} (ISBN: {book.isbn}) [🔴 已借出]")
    else:
        st.info("当前没有已借出的图书。")