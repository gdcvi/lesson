"""
图书管理系统 GUI 测试脚本
用于测试各个模块的功能是否正常
"""

from book import Book
from library import Library


def test_book_class():
    """测试 Book 类"""
    print("=" * 50)
    print("测试 Book 类")
    print("=" * 50)
    
    # 创建测试图书
    book = Book("Python 编程入门", "张三", "1234567890")
    
    # 测试初始状态
    assert book.title == "Python 编程入门"
    assert book.author == "张三"
    assert book.isbn == "1234567890"
    assert book.is_borrowed == False
    print("✓ 图书初始化成功")
    
    # 测试借书
    result = book.borrow()
    assert result == True
    assert book.is_borrowed == True
    print("✓ 借书操作成功")
    
    # 测试重复借书
    result = book.borrow()
    assert result == False
    print("✓ 重复借书检测成功")
    
    # 测试还书
    result = book.return_book()
    assert result == True
    assert book.is_borrowed == False
    print("✓ 还书操作成功")
    
    # 测试重复还书
    result = book.return_book()
    assert result == False
    print("✓ 重复还书检测成功")
    
    # 测试获取信息
    info = book.get_info()
    assert "Python 编程入门" in info
    assert "张三" in info
    assert "1234567890" in info
    print(f"✓ 图书信息格式化成功：{info}")
    
    print("\n")


def test_library_class():
    """测试 Library 类"""
    print("=" * 50)
    print("测试 Library 类")
    print("=" * 50)
    
    # 创建图书馆
    library = Library()
    
    # 测试添加图书
    book1 = Book("Python 基础", "李四", "1111111111")
    book2 = Book("算法导论", "王五", "2222222222")
    book3 = Book("数据结构", "赵六", "3333333333")
    
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    
    assert len(library.books) == 3
    print("✓ 添加图书成功")
    
    # 测试搜索 - 按书名
    results = library.search_book("Python")
    assert len(results) == 1
    assert results[0].title == "Python 基础"
    print("✓ 按书名搜索成功")
    
    # 测试搜索 - 按作者
    results = library.search_book("王五")
    assert len(results) == 1
    assert results[0].author == "王五"
    print("✓ 按作者搜索成功")
    
    # 测试搜索 - 不区分大小写
    results = library.search_book("python")
    assert len(results) == 1
    print("✓ 不区分大小写搜索成功")
    
    # 测试借书
    success = library.borrow_book("1111111111")
    assert success == True
    assert book1.is_borrowed == True
    print("✓ 借书操作成功")
    
    # 测试借不存在的书
    success = library.borrow_book("9999999999")
    assert success == False
    print("✓ 借不存在的书检测成功")
    
    # 测试还书
    success = library.return_book("1111111111")
    assert success == True
    assert book1.is_borrowed == False
    print("✓ 还书操作成功")
    
    # 测试查看已借出图书
    library.borrow_book("1111111111")
    library.borrow_book("2222222222")
    borrowed = library.show_borrowed_books()
    assert len(borrowed) == 2
    print("✓ 查看已借出图书成功")
    
    print(f"\n所有图书列表:")
    all_books = library.show_all_books()
    for idx, book in enumerate(all_books, 1):
        print(f"  {idx}. {book.get_info()}")
    print("\n")


def main():
    """运行所有测试"""
    print("\n")
    print("🎯 开始测试图书管理系统模块")
    print("\n")
    
    try:
        test_book_class()
        test_library_class()
        
        print("=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)
        print("\n")
        print("提示：现在可以运行 python main_gui.py 启动图形界面")
        print("\n")
        
    except AssertionError as e:
        print(f"\n❌ 测试失败：{e}")
        print("\n")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        print("\n")


if __name__ == "__main__":
    main()
