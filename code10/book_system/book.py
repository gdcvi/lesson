def log_operation(func):
    """
    装饰器，用于记录操作日志
    """
    def wrapper(*args, **kwargs):
        print(f"执行操作: {func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper


class Book:
    """
    图书类，用于表示一本图书的基本信息和借阅状态
    """
    
    def __init__(self, title, author, isbn):
        """
        初始化图书
        
        Args:
            title (str): 书名
            author (str): 作者
            isbn (str): ISBN号
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False  # 默认未借出
    
    @log_operation
    def borrow(self):
        """
        借出图书
        
        Returns:
            bool: 成功返回True，如果已被借出则返回False
        """
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False
    
    @log_operation
    def return_book(self):
        """
        归还图书
        
        Returns:
            bool: 成功返回True，如果未借出则返回False
        """
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False
    
    def get_info(self):
        """
        获取图书信息字符串
        
        Returns:
            str: 包含图书信息的字符串
        """
        status = "已借出" if self.is_borrowed else "可借阅"
        return f"{self.title} - {self.author} (ISBN:{self.isbn}) [{status}]"
    
    def __str__(self):
        """
        字符串表示
        
        Returns:
            str: 图书信息字符串
        """
        return self.get_info()