class Library:
    def __init__(self):
        """
        初始化图书列表
        创建一个空列表来存储Book对象
        """
        self.books = []
    
    def add_book(self, book):
        """
        将图书添加到图书馆
        参数：book是一个Book对象
        """
        self.books.append(book)
    
    def show_all_books(self):
        """
        显示所有图书
        遍历图书列表并显示每本书的信息
        """
        return self.books
    
    def search_book(self, keyword):
        """
        根据关键词搜索图书（书名或作者）
        参数：keyword搜索关键词
        使用lower()方法实现不区分大小写的搜索
        """
        results = []
        keyword_lower = keyword.lower()
        for book in self.books:
            if keyword_lower in book.title.lower() or keyword_lower in book.author.lower():
                results.append(book)
        return results
    
    def borrow_book(self, isbn):
        """
        借出指定ISBN的图书
        参数：isbn图书的ISBN号
        """
        for book in self.books:
            if book.isbn == isbn:
                return book.borrow()
        return False
    
    def return_book(self, isbn):
        """
        归还指定ISBN的图书
        参数：isbn图书的ISBN号
        """
        for book in self.books:
            if book.isbn == isbn:
                return book.return_book()
        return False
    
    def show_borrowed_books(self):
        """
        显示所有已借出的图书
        筛选出is_borrowed为True的图书
        """
        borrowed_books = []
        for book in self.books:
            if book.is_borrowed:
                borrowed_books.append(book)
        return borrowed_books