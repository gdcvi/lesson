"""
使用LangChain 0.3版本实现的Function Calling示例
基于通义千问(qwen)大模型
"""
import os
import json
from typing import Dict, Any
from langchain_core.tools import tool
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置API密钥
os.environ["DASHSCOPE_API_KEY"] = os.getenv("DASHSCOPE_API_KEY", "your-api-key-here")


# 定义工具函数 - 使用@tool装饰器
@tool
def get_current_temperature(location: str, unit: str = "celsius") -> Dict[str, Any]:
    """获取指定地点的当前温度
    
    Args:
        location: 地点，格式为"城市，州，国家"
        unit: 温度单位，支持"celsius"(摄氏度)或"fahrenheit"(华氏度)，默认为"celsius"
    
    Returns:
        包含温度、地点和单位的信息字典
    """
    # 模拟API返回的数据
    return {
        "temperature": 26.1,
        "location": location,
        "unit": unit,
    }


@tool
def get_temperature_date(location: str, date: str, unit: str = "celsius") -> Dict[str, Any]:
    """获取指定地点和日期的温度
    
    Args:
        location: 地点，格式为"城市，州，国家"
        date: 日期，格式为"年-月-日"
        unit: 温度单位，支持"celsius"(摄氏度)或"fahrenheit"(华氏度)，默认为"celsius"
    
    Returns:
        包含温度、地点、日期和单位的信息字典
    """
    # 模拟API返回的数据
    return {
        "temperature": 25.9,
        "location": location,
        "date": date,
        "unit": unit,
    }


# 创建工具列表，工具函数的注释很重要，大模型通过注释来判断调用哪个工具
tools = [get_current_temperature, get_temperature_date]

# 初始化工具映射表，用于根据名称查找工具
tool_map = {tool.name: tool for tool in tools}


def langchain_function_call(user_message: str):
    """使用LangChain实现的基础单步流程：一次用户提问，完成一次函数调用并得到最终回答"""
    print(f"用户提问: {user_message}")

    try:
        # -- 步骤 1: 初始化ChatTongyi模型并绑定工具 --
        llm = ChatTongyi(
            model="qwen-plus",
            temperature=0.3,
        )
        
        # 将工具绑定到LLM
        llm_with_tools = llm.bind_tools(tools)
        
        # -- 步骤 2: 首次调用模型，获取函数调用指令 --
        messages = [HumanMessage(content=user_message)]
        response = llm_with_tools.invoke(messages)
        
        # 提取模型返回的消息
        assistant_message = response
        
        # -- 步骤 3: 解析调用指令并执行函数 --
        # 如果模型决定调用工具，assistant_message里会包含 tool_calls 信息
        if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
            # 获取第一个工具调用指令
            tool_call = assistant_message.tool_calls[0]
            func_name = tool_call['name']  # 函数名
            func_args = tool_call['args']  # 函数参数
            
            print(f"模型决定调用工具: {func_name}")
            print(f"工具参数: {func_args}")
            
            # 根据函数名找到对应的本地工具并执行，获取结果
            if func_name in tool_map:
                tool_func = tool_map[func_name]
                function_result = tool_func.invoke(func_args)
                print(f"工具执行结果: {function_result}")
                
                # -- 步骤 4: 将结果回传给模型，生成最终回答 --
                # 构建完整的消息历史
                messages.extend([
                    assistant_message,  # 模型的工具调用指令
                    ToolMessage(content=str(function_result), tool_call_id=tool_call['id'])  # 工具返回的结果
                ])
                
                # 再次调用LLM获取最终回答
                final_response = llm.invoke(messages)
                print(f"最终回答: {final_response.content}\n")
            else:
                print(f"未找到函数: {func_name}\n")
        else:
            # 模型认为不需要调用工具，直接返回了答案
            print(f"最终回答: {assistant_message.content}\n")
            
    except Exception as e:
        print(f"发生错误: {str(e)}\n")


# --- 测试运行 ---
if __name__ == "__main__":
    print("="*50)
    print("LangChain版千问LLM工具调用演示")
    print("="*50)
    
    # 检查API密钥是否配置
    if os.getenv("DASHSCOPE_API_KEY") == "your-api-key-here":
        print("\n警告: 请先在 .env 文件中配置 DASHSCOPE_API_KEY")
        print("获取API密钥: https://dashscope.console.aliyun.com/apiKey")
    else:
        # 场景1: 查询旧金山现在的温度
        print("\n场景1: 查询当前温度")
        langchain_function_call("What's the temperature in San Francisco now?")
        
        # 场景2: 查询指定日期的温度
        print("\n场景2: 查询指定日期温度")
        langchain_function_call("What was the temperature in Beijing on 2024-01-01?")
        
        # 场景3: 不需要工具调用的问题
        print("\n场景3: 普通对话")
        langchain_function_call("Hello, how are you today?")
