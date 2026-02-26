
## 任务一：创建第一个类 —— 简单的“Student”类
编写一个Python程序，定义一个Student类，并创建它的实例。
1. 在一个新文件 student.py 中定义类。
2. 类的构造函数 __init__ 接收 name (姓名) 和 scores (成绩列表) 两个参数。
3. 定义两个实例属性：self.name 和 self.scores。
4. 定义一个实例方法 get_average()，计算并返回该学生的平均成绩。
5. 在 main.py 中导入 Student 类，创建一个名为“张三”，成绩为 [85, 92, 78] 的学生对象。
6. 调用该对象的 get_average() 方法，打印出“张三”的平均分。
## 任务二：让类更强大 —— 封装与业务逻辑
增强 Student 类的功能，体现“封装”的思想，将数据和对数据的操作绑定在一起。
1. 在 Student 类中增加一个实例属性 self.grade，用于存放学生年级（如“大一”）。
2. 修改构造函数，使其能接收年级信息。
3. 增加一个实例方法 add_score(new_score)，用于向学生的 scores 列表中添加一个新成绩。
4. 增加一个实例方法 is_passing()，判断学生是否所有科目都及格（>=60），返回布尔值。
5. 在 main.py 中，对已有的“张三”对象添加一个新成绩 95，然后判断他是否所有科目都及格，并打印结果。
## 任务三：模块化组织与类的继承
我们将创建更复杂的类结构，并再次应用模块化思想。
1. 创建一个新文件 person.py。
2. 在 person.py 中定义一个基类 Person，包含 name 属性和一个 introduce() 方法，打印“大家好，我是XXX”。
3. 修改 student.py，让它从 person.py 中导入 Person 类，并让 Student 类继承自 Person。
4. 在 Student 类中，重写（Override）introduce() 方法，使其能打印“大家好，我是学生XXX，我的平均分是YYY”。（多态的雏形）
5. 在 main.py 中，创建 Student 对象，并调用其 introduce() 方法，观察与基类的不同。