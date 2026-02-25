# 图书管理系统 - Streamlit Web版

## 项目介绍
这是一个使用Streamlit构建的Web版图书管理系统，提供图形化界面来管理图书的借阅与归还。

## 功能说明
1. 添加图书 - 可以添加新书，包括书名、作者、ISBN
2. 查看所有图书 - 显示图书馆中的所有图书及其借阅状态
3. 搜索图书 - 根据书名或作者搜索图书
4. 借阅图书 - 将指定ISBN的图书标记为已借出
5. 归还图书 - 将指定ISBN的图书标记为可借阅
6. 查看已借出图书 - 显示所有已借出的图书

## 安装与运行

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动Web应用
```bash
streamlit run app.py
```

启动后，浏览器会自动打开应用界面，如果没有自动打开，可以访问 http://localhost:8501

## 技术特点
- Web界面：使用Streamlit构建直观的用户界面
- 模块化设计：分为book、library、app三个模块
- 面向对象编程：使用Book和Library两个类
- 数据持久化：自动将图书数据保存到books.json文件中
- 装饰器应用：为关键操作添加日志记录功能