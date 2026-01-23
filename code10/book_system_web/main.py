from library import Library
from book import Book


def display_menu():
    """
    显示菜单选项
    """
    print("\n=== 图书管理系统 ===")
    print("1. 添加图书")
    print("2. 查看所有图书")
    print("3. 搜索图书")
    print("4. 借阅图书")
    print("5. 归还图书")
    print("6. 查看已借出图书")
    print("0. 退出系统")
    print("=" * 20)


def main():
    """
    主函数，控制程序流程
    """
    library = Library()  # 创建Library对象，自动加载数据
    
    while True:
        display_menu()
        choice = input("请选择操作：").strip()
        
        if choice == "1":
            # 添加图书
            title = input("请输入书名：").strip()
            author = input("请输入作者：").strip()
            isbn = input("请输入ISBN：").strip()
            
            if title and author and isbn:
                book = Book(title, author, isbn)
                library.add_book(book)
            else:
                print("输入信息不完整，请重新输入。")
        
        elif choice == "2":
            # 查看所有图书
            library.show_all_books()
        
        elif choice == "3":
            # 搜索图书
            keyword = input("请输入搜索关键词（书名或作者）：").strip()
            if keyword:
                library.search_book(keyword)
            else:
                print("关键词不能为空。")
        
        elif choice == "4":
            # 借阅图书
            isbn = input("请输入要借阅的图书ISBN：").strip()
            if isbn:
                library.borrow_book(isbn)
            else:
                print("ISBN不能为空。")
        
        elif choice == "5":
            # 归还图书
            isbn = input("请输入要归还的图书ISBN：").strip()
            if isbn:
                library.return_book(isbn)
            else:
                print("ISBN不能为空。")
        
        elif choice == "6":
            # 查看已借出图书
            library.show_borrowed_books()
        
        elif choice == "0":
            # 退出系统
            print("感谢使用图书管理系统，再见！")
            break
        
        else:
            print("无效的选择，请重新输入。")
        
        # 暂停，让用户查看结果
        input("\n按回车键继续...")


if __name__ == "__main__":
    main()