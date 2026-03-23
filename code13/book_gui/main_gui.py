import tkinter as tk
from tkinter import ttk, messagebox
from book import Book
from library import Library


class BookManagerGUI:
    def __init__(self, root):
        """初始化图书管理系统 GUI"""
        self.root = root
        self.root.title("图书管理系统")
        self.root.geometry("900x600")
        
        # 创建图书馆对象
        self.library = Library()
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Status.TLabel', font=('Arial', 10))
        
        # 创建主框架
        self.create_main_interface()
        
    def create_main_interface(self):
        """创建主界面"""
        # 顶部标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = ttk.Label(
            title_frame, 
            text="📚 图书管理系统", 
            style='Title.TLabel'
        )
        title_label.pack()
        
        # 创建左右分栏
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左侧面板 - 操作区
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # 右侧面板 - 图书列表区
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # 创建左侧操作面板
        self.create_left_panel(left_frame)
        
        # 创建右侧显示面板
        self.create_right_panel(right_frame)
        
    def create_left_panel(self, parent):
        """创建左侧操作面板"""
        # 添加图书区域
        add_frame = ttk.LabelFrame(parent, text="添加图书", padding=10)
        add_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_frame, text="书名:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.title_entry = ttk.Entry(add_frame, width=25)
        self.title_entry.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(add_frame, text="作者:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.author_entry = ttk.Entry(add_frame, width=25)
        self.author_entry.grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(add_frame, text="ISBN:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.isbn_entry = ttk.Entry(add_frame, width=25)
        self.isbn_entry.grid(row=2, column=1, pady=2, padx=5)
        
        self.add_btn = ttk.Button(add_frame, text="添加图书", command=self.add_book)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # 搜索图书区域
        search_frame = ttk.LabelFrame(parent, text="搜索图书", padding=10)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="关键词:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.grid(row=0, column=1, pady=2, padx=5)
        
        self.search_btn = ttk.Button(search_frame, text="搜索", command=self.search_books)
        self.search_btn.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.clear_search_btn = ttk.Button(
            search_frame, 
            text="显示全部", 
            command=self.show_all_books
        )
        self.clear_search_btn.grid(row=2, column=0, columnspan=2, pady=2)
        
        # 借阅管理区域
        borrow_frame = ttk.LabelFrame(parent, text="借阅管理", padding=10)
        borrow_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(borrow_frame, text="ISBN:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.borrow_isbn_entry = ttk.Entry(borrow_frame, width=25)
        self.borrow_isbn_entry.grid(row=0, column=1, pady=2, padx=5)
        
        self.borrow_btn = ttk.Button(borrow_frame, text="借书", command=self.borrow_book)
        self.borrow_btn.grid(row=1, column=0, pady=5)
        
        self.return_btn = ttk.Button(borrow_frame, text="还书", command=self.return_book)
        self.return_btn.grid(row=1, column=1, pady=5)
        
        # 功能按钮区域
        action_frame = ttk.LabelFrame(parent, text="功能菜单", padding=10)
        action_frame.pack(fill=tk.X, pady=5)
        
        self.show_all_btn = ttk.Button(
            action_frame, 
            text="查看所有图书", 
            command=self.show_all_books
        )
        self.show_all_btn.pack(fill=tk.X, pady=2)
        
        self.show_borrowed_btn = ttk.Button(
            action_frame, 
            text="查看已借出图书", 
            command=self.show_borrowed_books
        )
        self.show_borrowed_btn.pack(fill=tk.X, pady=2)
        
    def create_right_panel(self, parent):
        """创建右侧显示面板"""
        # 图书列表
        list_frame = ttk.LabelFrame(parent, text="图书列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建树形视图
        columns = ('序号', '书名', '作者', 'ISBN', '状态')
        self.book_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # 设置列标题
        self.book_tree.heading('序号', text='序号')
        self.book_tree.heading('书名', text='书名')
        self.book_tree.heading('作者', text='作者')
        self.book_tree.heading('ISBN', text='ISBN')
        self.book_tree.heading('状态', text='状态')
        
        # 设置列宽
        self.book_tree.column('序号', width=50, anchor=tk.CENTER)
        self.book_tree.column('书名', width=200, anchor=tk.W)
        self.book_tree.column('作者', width=100, anchor=tk.W)
        self.book_tree.column('ISBN', width=120, anchor=tk.CENTER)
        self.book_tree.column('状态', width=80, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.book_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 状态栏
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(
            status_frame, 
            text="总图书数：0 | 可借阅：0 | 已借出：0", 
            style='Status.TLabel'
        )
        self.status_label.pack()
        
    def add_book(self):
        """添加图书"""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        
        if not title or not author or not isbn:
            messagebox.showwarning("警告", "请填写完整的图书信息！")
            return
        
        # 检查 ISBN 是否已存在
        for book in self.library.books:
            if book.isbn == isbn:
                messagebox.showwarning("警告", f"ISBN {isbn} 已存在！")
                return
        
        # 创建并添加图书
        new_book = Book(title, author, isbn)
        self.library.add_book(new_book)
        
        # 清空输入框
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        
        messagebox.showinfo("成功", f"图书 '{title}' 添加成功！")
        self.show_all_books()
        
    def search_books(self):
        """搜索图书"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入搜索关键词！")
            return
        
        results = self.library.search_book(keyword)
        self.display_books(results)
        self.update_status(f"搜索到 {len(results)} 本图书")
        
    def show_all_books(self):
        """显示所有图书"""
        all_books = self.library.show_all_books()
        self.display_books(all_books)
        self.search_entry.delete(0, tk.END)
        self.update_status()
        
    def show_borrowed_books(self):
        """显示已借出图书"""
        borrowed_books = self.library.show_borrowed_books()
        self.display_books(borrowed_books)
        self.search_entry.delete(0, tk.END)
        self.update_status(f"已借出图书：{len(borrowed_books)} 本")
        
    def borrow_book(self):
        """借书"""
        isbn = self.borrow_isbn_entry.get().strip()
        if not isbn:
            messagebox.showwarning("警告", "请输入图书 ISBN！")
            return
        
        success = self.library.borrow_book(isbn)
        if success:
            messagebox.showinfo("成功", f"ISBN {isbn} 的图书已借出！")
            self.show_all_books()
        else:
            messagebox.showerror("失败", f"借书失败！请检查 ISBN 是否正确或图书已借出。")
            
    def return_book(self):
        """还书"""
        isbn = self.borrow_isbn_entry.get().strip()
        if not isbn:
            messagebox.showwarning("警告", "请输入图书 ISBN！")
            return
        
        success = self.library.return_book(isbn)
        if success:
            messagebox.showinfo("成功", f"ISBN {isbn} 的图书已归还！")
            self.show_all_books()
        else:
            messagebox.showerror("失败", f"还书失败！请检查 ISBN 是否正确或图书未借出。")
            
    def display_books(self, books):
        """在树形视图中显示图书"""
        # 清空现有数据
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        # 添加新数据
        for idx, book in enumerate(books, 1):
            status = "已借出" if book.is_borrowed else "可借阅"
            self.book_tree.insert('', tk.END, values=(
                idx,
                book.title,
                book.author,
                book.isbn,
                status
            ))
            
        # 更新状态栏
        total = len(books)
        borrowed = sum(1 for book in books if book.is_borrowed)
        available = total - borrowed
        self.update_status(f"总图书数：{total} | 可借阅：{available} | 已借出：{borrowed}")
        
    def update_status(self, custom_text=None):
        """更新状态栏信息"""
        if custom_text:
            self.status_label.config(text=custom_text)
        else:
            total = len(self.library.books)
            borrowed = sum(1 for book in self.library.books if book.is_borrowed)
            available = total - borrowed
            self.status_label.config(
                text=f"总图书数：{total} | 可借阅：{available} | 已借出：{borrowed}"
            )


def main():
    """主函数"""
    root = tk.Tk()
    app = BookManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
