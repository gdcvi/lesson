class Book:
    def __init__(self, title, author, isbn):
        """
        初始化书名、作者、ISBN、借阅状态(is_borrowed)
        新书默认是"可借阅"状态（is_borrowed = False）
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False
    
    def borrow(self):
        """
        将图书标记为已借出
        只有当图书当前状态是"可借阅"时才能借出
        返回：成功返回True，失败返回False
        """
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False
    
    def return_book(self):
        """
        将图书标记为可借阅
        只有当图书当前状态是"已借出"时才能归还
        返回：成功返回True，失败返回False
        """
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False
    
    def get_info(self):
        """
        返回图书信息字符串
        格式："书名 - 作者 (ISBN:编号) [可借阅/已借出]"
        """
        status = "已借出" if self.is_borrowed else "可借阅"
        return f"{self.title} - {self.author} (ISBN:{self.isbn}) [{status}]"
        
    def __str__(self):
        """返回图书信息字符串"""
        return self.get_info()