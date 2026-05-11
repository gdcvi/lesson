"""
 * @author: zkyuan
 * @date: 2026/5/11
 * @description: 大语言模型(LLM)文本对话 —— 使用 LangChain ChatOpenAI 调用Qwen大模型
 * 功能演示：单轮对话、多轮对话、流式输出、带系统提示词的对话、参数对比
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()


def create_llm(temperature: float = 0.7, max_tokens: int = 500):
    """创建 LangChain ChatOpenAI 实例"""
    return ChatOpenAI(
        model="qwen-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=temperature,
        max_tokens=max_tokens,
    )


def demo_single_turn():
    """示例1：单轮对话 —— 最简单的问答"""
    print("\n" + "=" * 50)
    print("【示例1】单轮对话")
    print("=" * 50)

    llm = create_llm()
    response = llm.invoke("请用一句话介绍什么是大语言模型")

    print(f"用户: 请用一句话介绍什么是大语言模型")
    print(f"Qwen: {response.content}")
    if "token_usage" in response.response_metadata:
        print(f"Token用量: {response.response_metadata['token_usage']}")


def demo_multi_turn():
    """示例2：多轮对话 —— 带上下文的连续对话"""
    print("\n" + "=" * 50)
    print("【示例2】多轮对话（带上下文记忆）")
    print("=" * 50)

    llm = create_llm(max_tokens=800)
    messages = [
        SystemMessage(content="你是一位资深的Python编程老师，回答要简洁明了。"),
    ]

    questions = [
        "Python中列表和元组有什么区别？",
        "那什么时候该用元组而不是列表呢？",
        "请用代码举个例子",
    ]

    for q in questions:
        messages.append(HumanMessage(content=q))
        response = llm.invoke(messages)
        messages.append(AIMessage(content=response.content))

        print(f"\n学生: {q}")
        print(f"老师: {response.content}")
        if "token_usage" in response.response_metadata:
            usage = response.response_metadata["token_usage"]
            total = usage.get("total_tokens", usage) if isinstance(usage, dict) else usage
            print(f"  [Token用量: {total}]")


def demo_streaming():
    """示例3：流式输出 —— 逐字输出内容"""
    print("\n" + "=" * 50)
    print("【示例3】流式输出")
    print("=" * 50)

    llm = create_llm(temperature=0.8, max_tokens=500)
    prompt = "写一首关于人工智能的五言绝句"

    print(f"\n用户: {prompt}")
    print("Qwen: ", end="", flush=True)

    collected_text = ""
    for chunk in llm.stream(prompt):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            collected_text += chunk.content

    print(f"\n\n(流式输出完毕，共 {len(collected_text)} 字)")


def demo_system_prompt():
    """示例4：带系统提示词 —— 定制AI角色"""
    print("\n" + "=" * 50)
    print("【示例4】角色扮演 —— 系统提示词")
    print("=" * 50)

    llm = create_llm(temperature=0.9, max_tokens=300)
    messages = [
        SystemMessage(content="你是一个名叫'小灵'的AI助手，说话风格活泼可爱，喜欢用emoji，每次回答不超过3句话。"),
        HumanMessage(content="你好，我叫小明，今天心情不太好"),
    ]

    response = llm.invoke(messages)
    print(f"\n用户: {messages[-1].content}")
    print(f"小灵: {response.content}")


def demo_temperature_comparison():
    """示例5：不同temperature参数对比"""
    print("\n" + "=" * 50)
    print("【示例5】不同 Temperature 参数对比")
    print("=" * 50)

    prompt = "用一句话描述春天的西湖"
    temperatures = [0.1, 1.0, 1.5]

    for temp in temperatures:
        llm = create_llm(temperature=temp, max_tokens=200)
        response = llm.invoke(prompt)
        print(f"\nTemperature={temp}: {response.content}")


if __name__ == "__main__":
    demo_single_turn()
    demo_multi_turn()
    demo_streaming()
    demo_system_prompt()
    demo_temperature_comparison()

    print("\n" + "=" * 50)
    print("所有LLM示例演示完毕")
    print("=" * 50)

# 测试运行结果：
r"""
D:\Anaconda\envs\lesson\python.exe E:\code\GitWork\gdcvi\lesson\code24\1_llm.py 

==================================================
【示例1】单轮对话
==================================================
用户: 请用一句话介绍什么是大语言模型
Qwen: 大语言模型（Large Language Model, LLM）是一种基于深度学习、通过在海量文本数据上进行大规模训练而构建的AI模型，能够理解、生成自然语言，并完成问答、翻译、写作、推理等多种语言任务。
Token用量: {'completion_tokens': 50, 'prompt_tokens': 16, 'total_tokens': 66, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}

==================================================
【示例2】多轮对话（带上下文记忆）
==================================================

学生: Python中列表和元组有什么区别？
老师: 主要区别如下：

1. **可变性**：  
   - 列表（`list`）是**可变的**，支持增删改（如 `append()`、`pop()`、`[i] = x`）。  
   - 元组（`tuple`）是**不可变的**，创建后不能修改元素或长度。

2. **语法**：  
   - 列表用方括号：`[1, 2, 3]`  
   - 元组用圆括号（单元素需加逗号）：`(1, 2, 3)` 或 `(42,)`

3. **性能与用途**：  
   - 元组更轻量，访问稍快，适合表示**固定数据结构**（如坐标 `(x, y)`、返回多个值 `return a, b`）。  
   - 列表适合需要动态操作的**有序集合**。

4. **其他**：  
   - 元组可作为字典的键（因不可变），列表不行。  
   - 两者都支持索引、切片、迭代和成员检查（`in`）。

✅ 简记：**列表可变，元组不可变；列表干活，元组存数据。**
  [Token用量: 314]

学生: 那什么时候该用元组而不是列表呢？
老师: 该用元组的典型场景（记住：**用元组当“不变的数据容器”**）：

✅ **1. 表示固定结构的数据**  
```python
point = (3, 5)          # 坐标，逻辑上不可变  
rgb = (255, 128, 0)     # 颜色值，顺序和含义固定
```

✅ **2. 函数返回多个值（Python 自动打包为元组）**  
```python
def get_name_age():
    return "Alice", 30

name, age = get_name_age()  # 自动解包 → 元组是隐式载体！
# 等价于：name, age = ("Alice", 30)
```

✅ **3. 用作字典键（因不可变）**  
```python
locations = {("Beijing", "Chaoyang"): "Office",  
             ("Shanghai", "Pudong"): "Lab"}
```

✅ **4. 保证数据安全（防误改）**  
```python
months = ("Jan", "Feb", "Mar", ...)  # 不希望被 append() 或修改
```

✅ **5. 命名元组（`collections.namedtuple`）提升可读性**  
```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 5)  # p.x, p.y 可读性强，且不可变
```

❌ **别用元组的情况**：需要增删、排序、重复修改 → 选列表。

💡 口诀：**“定值、多返、当键、防改” —— 优先元组。**
  [Token用量: 715]

学生: 请用代码举个例子
老师: 当然！下面是一个**对比示例**，清晰展示何时用元组、何时用列表：

```python
# ✅ 场景1：固定配置 → 用元组（防误改 + 可当字典键）
DB_CONFIG = ("localhost", 5432, "myapp")  # host, port, db_name
# DB_CONFIG[1] = 5433  # ❌ 报错：TypeError: 'tuple' object does not support item assignment

# ✅ 场景2：用户数据集合 → 用列表（需动态增删）
users = ["Alice", "Bob"]
users.append("Charlie")  # ✅ 正常
users.remove("Bob")      # ✅ 正常

# ✅ 场景3：返回多个值 → 自动是元组，解包很自然
def divide(a, b):
    return a // b, a % b  # 返回 (商, 余数) → 元组

q, r = divide(10, 3)  # ✅ 自动解包：q=3, r=1（本质是 q, r = (3, 1)）

# ✅ 场景4：字典键 → 必须用元组
location_map = {
    ("lat", "lon"): (39.9, 116.4),   # ✅ 合法键
    # [39.9, 116.4]: "Beijing"     # ❌ TypeError: unhashable type: 'list'
}

# ✅ 场景5：命名元组 → 更清晰、不可变
from collections import namedtuple
Person = namedtuple("Person", ["name", "age"])
p = Person("Alice", 30)
# p.age = 31  # ❌ 不可修改
print(p.name)  # ✅ 输出 "Alice" —— 比普通元组更易读
```

📌 **关键提醒**：  
> 元组不是“轻量列表”，而是**语义上表示“不变的有序数据”**；选它不是为了省内存，而是为了**表达意图 + 避免bug**。

需要我帮你判断某个具体场景该用哪个？欢迎贴代码 😊
  [Token用量: 1228]

==================================================
【示例3】流式输出
==================================================

用户: 写一首关于人工智能的五言绝句
Qwen: 《咏AI》  
玄机藏硅海，慧焰炼云台。  
未有形骸重，长随万象开。  

注：本诗以传统五绝形式咏写人工智能。“硅海”喻指芯片与数据的浩瀚基底，“云台”象征云端算力与智能平台；“慧焰”既指算法之光，亦含智慧如焰、灼灼不熄之意。后两句转写AI无形无相却赋能万物之特质——“未有形骸重”化用《庄子》“得鱼忘筌”之思，言其超越物理载体；“长随万象开”则展现其在科研、医疗、艺术等万般场景中持续拓展的蓬勃生命力。全篇凝练蕴藉，于古典语境中透出现代哲思。

(流式输出完毕，共 224 字)

==================================================
【示例4】角色扮演 —— 系统提示词
==================================================

用户: 你好，我叫小明，今天心情不太好
小灵: 小明你好呀～👋 心情像乌云☁️，但小灵会变成小太阳☀️陪你哦！  
要不我们一起深呼吸三次，再分享下发生了什么？🤗

==================================================
【示例5】不同 Temperature 参数对比
==================================================

Temperature=0.1: 春天的西湖，桃红柳绿、烟雨空濛，苏堤春晓处新芽初绽，断桥倒影轻摇于潋滟波光之中，一湖春水半城诗。

Temperature=1.0: 春天的西湖，桃红柳绿、烟雨空蒙，苏堤春晓的垂柳拂过潋滟波光，断桥边新荷初露、莺燕争暖，一湖碧水映着远山如黛与游人笑语，处处流淌着水墨诗韵与生机盎然的江南清欢。

Temperature=1.5: 春天的西湖，桃红柳绿、烟雨空蒙，断桥苏堤上莺飞草长，湖面浮光跃金，游船轻漾，一派“欲把西湖比西子，淡妆浓抹总相宜”的灵动与诗韵。

==================================================
所有LLM示例演示完毕
==================================================

Process finished with exit code 0

"""