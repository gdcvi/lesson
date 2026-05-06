"""
function calling单步流程
"""
import json
import dashscope

# 工具1: 获取当前温度
def get_current_temperature(location: str, unit: str = "celsius"):
    """获取指定地点的当前温度
    Args:
        location (str): 地点，格式为"城市，州，国家"。
        unit (str): 温度单位，支持"celsius"（摄氏度）或"fahrenheit"（华氏度）。默认为"celsius"。
    Returns:
        dict: 包含温度、地点和单位的信息。
    """
    # 模拟API返回的数据
    return {
        "temperature": 26.1,
        "location": location,
        "unit": unit,
    }

# 工具2: 获取指定日期的温度
def get_temperature_date(location: str, date: str, unit: str = "celsius"):
    """获取指定地点和日期的温度
    Args:
        location (str): 地点，格式为"城市，州，国家"。
        date (str): 日期，格式为"年-月-日"。
        unit (str): 温度单位，支持"celsius"（摄氏度）或"fahrenheit"（华氏度）。默认为"celsius"。
    Returns:
        dict: 包含温度、地点、日期和单位的信息。
    """
    # 模拟API返回的数据
    return {
        "temperature": 25.9,
        "location": location,
        "date": date,
        "unit": unit,
    }

# 一个辅助函数，用于根据函数名找到对应的本地函数
def get_function_by_name(name):
    """根据函数名称获取对应的函数对象"""
    functions = {
        "get_current_temperature": get_current_temperature,
        "get_temperature_date": get_temperature_date
    }
    return functions.get(name)

# 工具描述列表 (Tools Definition)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_temperature",
            "description": "获取一个地点的当前温度。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": '地点，格式如"城市, 州, 国家"。'
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": '温度单位，默认为"celsius"。'
                    },
                },
                "required": ["location"] # 必须的参数
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_temperature_date",
            "description": "获取一个地点在特定日期的温度。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": '地点，格式如"城市, 州, 国家"。'
                    },
                    "date": {
                        "type": "string",
                        "description": '日期，格式为"年-月-日"。'
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": '温度单位，默认为"celsius"。'
                    },
                },
                "required": ["location", "date"] # 必须的参数
            },
        }
    }
]


def simple_function_call(user_message):
    """基础单步流程：一次用户提问，完成一次函数调用并得到最终回答。"""
    print(f"用户提问: {user_message}")

    try:
        # -- 步骤 1: 首次调用模型，获取函数调用指令 --
        # 模型会分析用户问题，并告诉我们是否需要调用工具
        response = dashscope.Generation.call(
            model="qwen-plus",
            messages=[{'role': 'user', 'content': user_message}],
            tools=TOOLS,
            tool_choice="auto"  # "auto" 表示让模型自己决定是否调用工具
        )

        # 检查响应状态
        if response.status_code != 200:
            print(f"API调用失败: {response.code} - {response.message}")
            return

        # 提取模型返回的消息
        assistant_message = response.output.choices[0].message

        # -- 步骤 2: 解析调用指令并执行函数 --
        # 如果模型决定调用工具，assistant_message里会包含 tool_calls 信息
        if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
            # 获取第一个工具调用指令
            tool_call = assistant_message.tool_calls[0]
            func_name = tool_call['function']['name']  # 函数名
            func_args = json.loads(tool_call['function']['arguments'])  # 函数参数

            print(f"模型决定调用工具: {func_name}")
            print(f"工具参数: {func_args}")

            # 根据函数名找到对应的本地函数并执行，获取结果
            function_to_call = get_function_by_name(func_name)
            if function_to_call:
                function_result = function_to_call(**func_args)
                print(f"工具执行结果: {function_result}")

                # -- 步骤 3: 将结果回传给模型，生成最终回答 --
                # 我们需要构建一个新的消息列表，包含完整的上下文
                final_response = dashscope.Generation.call(
                    model="qwen-plus",
                    messages=[
                        {'role': 'user', 'content': user_message},  # 用户原始问题
                        assistant_message,  # 模型的工具调用指令
                        {'role': 'tool', 'content': str(function_result), 'name': func_name}  # 工具返回的结果
                    ]
                )
                
                if final_response.status_code == 200:
                    print(f"最终回答: {final_response.output.choices[0].message.content}\n")
                else:
                    print(f"最终回答生成失败: {final_response.code} - {final_response.message}\n")
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
    print("千问LLM工具调用演示")
    print("="*50)
    
    # 检查API密钥是否配置
    if dashscope.api_key == 'your-api-key-here':
        print("\n警告: 请先在 .env 文件中配置 DASHSCOPE_API_KEY")
        print("获取API密钥: https://dashscope.console.aliyun.com/apiKey")
    else:
        # 场景1: 查询旧金山现在的温度
        print("\n场景1: 查询当前温度")
        simple_function_call("What's the temperature in San Francisco now?")
        
        # 场景2: 查询指定日期的温度
        print("\n场景2: 查询指定日期温度")
        simple_function_call("What was the temperature in Beijing on 2024-01-01?")
        
        # 场景3: 不需要工具调用的问题
        print("\n场景3: 普通对话")
        simple_function_call("Hello, how are you today?")