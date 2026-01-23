import json
from book import Book


def log_operation(func):
    """
    装饰器，用于记录操作日志
    """
    def wrapper(*args, **kwargs):
        print(f"执行操作: {func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper


class Library:
    """
    图书馆类，用于管理图书集合
    """
    
    def __init__(self, filename="books.json"):
        """
        初始化图书馆，创建空的图书列表
        
        Args:
            filename (str): 存储图书数据的文件名
        """
        self.books = []
        self.filename = filename
        self.load_from_file()
    
    def add_book(self, book):
        """
        添加图书到图书馆
        
        Args:
            book (Book): 要添加的图书对象
        """
        self.books.append(book)
        print(f"图书 '{book.title}' 添加成功！")
        self.save_to_file()
    
    def show_all_books(self):
        """
        显示所有图书
        """
        if not self.books:
            print("暂无图书。")
            return
        
        print("所有图书：")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
    
    def search_book(self, keyword):
        """
        根据关键词搜索图书（书名或作者）
        
        Args:
            keyword (str): 搜索关键词
            
        Returns:
            list: 匹配的图书列表
        """
        results = []
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                results.append(book)
        
        if results:
            print(f"找到 {len(results)} 本相关图书：")
            for i, book in enumerate(results, 1):
                print(f"{i}. {book}")
        else:
            print("未找到相关图书。")
        
        return results
    
    @log_operation
    def borrow_book(self, isbn):
        """
        借出指定ISBN的图书
        
        Args:
            isbn (str): 要借出的图书ISBN
            
        Returns:
            bool: 借书成功返回True，失败返回False
        """
        for book in self.books:
            if book.isbn == isbn:
                if book.borrow():
                    print(f"成功借出《{book.title}》")
                    self.save_to_file()  # 借出后保存状态
                    return True
                else:
                    print(f"《{book.title}》已经借出了。")
                    return False
        
        print(f"找不到ISBN为 {isbn} 的图书。")
        return False
    
    @log_operation
    def return_book(self, isbn):
        """
        归还指定ISBN的图书
        
        Args:
            isbn (str): 要归还的图书ISBN
            
        Returns:
            bool: 还书成功返回True，失败返回False
        """
        for book in self.books:
            if book.isbn == isbn:
                if book.return_book():
                    print(f"成功归还《{book.title}》")
                    self.save_to_file()  # 归还后保存状态
                    return True
                else:
                    print(f"《{book.title}》尚未借出。")
                    return False
        
        print(f"找不到ISBN为 {isbn} 的图书。")
        return False
    
    def show_borrowed_books(self):
        """
        显示所有已借出的图书
        """
        borrowed_books = [book for book in self.books if book.is_borrowed]
        
        if borrowed_books:
            print("已借出的图书：")
            for i, book in enumerate(borrowed_books, 1):
                print(f"{i}. {book}")
        else:
            print("当前没有已借出的图书。")
        
        return borrowed_books
    
    def save_to_file(self):
        """
        将图书数据保存到文件
        """
        try:
            data = []
            for book in self.books:
                data.append({
                    'title': book.title,
                    'author': book.author,
                    'isbn': book.isbn,
                    'is_borrowed': book.is_borrowed
                })
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件时出错: {e}")
    
    def load_from_file(self):
        """
        从文件加载图书数据
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for item in data:
                book = Book(item['title'], item['author'], item['isbn'])
                book.is_borrowed = item['is_borrowed']
                self.books.append(book)
        except FileNotFoundError:
            # 文件不存在则创建空文件
            self.save_to_file()
        except Exception as e:
            print(f"加载文件时出错: {e}")