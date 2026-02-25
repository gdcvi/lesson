"""
 * @author: zkyuan
 * @date: 2026/2/25 9:53
 * @description: 自动化测试图书管理系统的主要功能
"""

import os

from book import Book
from library import Library


def test_book_class():
    """测试Book类的功能"""
    print("=== 测试Book类 ===")

    # 创建一本书
    book = Book("Python入门", "张三", "12345")
    print(f"创建图书: {book}")

    # 测试借出功能
    print(f"借出图书: {book.borrow()}")
    print(f"借出后状态: {book}")

    # 再次尝试借出（应该失败）
    print(f"重复借出: {book.borrow()}")

    # 测试归还功能
    print(f"归还图书: {book.return_book()}")
    print(f"归还后状态: {book}")

    # 再次尝试归还（应该失败）
    print(f"重复归还: {book.return_book()}")

    print()


def test_library_class():
    """测试Library类的功能"""
    print("=== 测试Library类 ===")

    library = Library("test_books.json")  # 使用测试文件

    # 添加图书
    book1 = Book("Python入门", "张三", "12345")
    book2 = Book("算法导论", "李四", "67890")
    library.add_book(book1)
    library.add_book(book2)

    # 显示所有图书
    print("\n显示所有图书:")
    library.show_all_books()

    # 搜索图书
    print("\n搜索'Python':")
    library.search_book("Python")

    print("\n搜索'李四':")
    library.search_book("李四")

    # 借出图书
    print("\n借出ISBN为12345的图书:")
    library.borrow_book("12345")

    # 显示所有图书（查看状态变化）
    print("\n借出后的所有图书:")
    library.show_all_books()

    # 显示已借出的图书
    print("\n显示已借出的图书:")
    library.show_borrowed_books()

    # 归还图书
    print("\n归还ISBN为12345的图书:")
    library.return_book("12345")

    # 再次显示所有图书
    print("\n归还后的所有图书:")
    library.show_all_books()

    print()


def test_file_storage():
    """测试文件存储功能"""
    print("=== 测试文件存储功能 ===")

    filename = "temp_test_books.json"

    # 创建图书馆并添加一些图书
    library1 = Library(filename)
    book1 = Book("测试书籍1", "作者1", "111")
    book2 = Book("测试书籍2", "作者2", "222")
    library1.add_book(book1)
    library1.add_book(book2)

    # 借出一本书
    library1.borrow_book("111")

    print("原始图书馆状态:")
    library1.show_all_books()

    # 创建新的图书馆实例，应该从文件加载相同的数据
    library2 = Library(filename)
    print("\n从文件重新加载后的状态:")
    library2.show_all_books()

    # 清理测试文件
    if os.path.exists(filename):
        os.remove(filename)
        print(f"\n已删除测试文件: {filename}")

    print()


def test_decorator():
    """测试装饰器功能"""
    print("=== 测试装饰器功能 ===")

    library = Library("decorator_test.json")

    # 添加图书，应该看到装饰器输出
    book = Book("装饰器测试", "测试作者", "999")
    library.add_book(book)

    # 借出图书，应该看到装饰器输出
    library.borrow_book("999")

    # 归还图书，应该看到装饰器输出
    library.return_book("999")

    # 清理测试文件
    if os.path.exists("decorator_test.json"):
        os.remove("decorator_test.json")

    print()


def run_manual_test():
    """手动测试，模拟用户交互"""
    print("=== 手动测试示例 ===")

    library = Library("manual_test.json")

    # 添加几本书
    books_data = [
        ("Python入门", "张三", "12345"),
        ("算法导论", "李四", "67890"),
        ("数据结构", "王五", "11111")
    ]

    for title, author, isbn in books_data:
        book = Book(title, author, isbn)
        library.add_book(book)

    print()

    # 显示所有图书
    library.show_all_books()
    print()

    # 借出一本书
    library.borrow_book("12345")
    print()

    # 查看已借出的图书
    library.show_borrowed_books()
    print()

    # 搜索图书
    library.search_book("算法")
    print()

    # 清理测试文件
    if os.path.exists("manual_test.json"):
        os.remove("manual_test.json")


if __name__ == "__main__":
    test_book_class()
    test_library_class()
    test_file_storage()
    test_decorator()
    run_manual_test()

    print("所有测试完成！")
