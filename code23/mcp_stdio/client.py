# 导入所需的模块和库
import asyncio  # 异步编程支持
import os  # 操作系统接口，用于读取环境变量
import sys  # 系统相关参数和函数，用于获取命令行参数
import json  # JSON数据处理
from typing import Optional  # 类型提示，表示可选类型
from contextlib import AsyncExitStack  # 异步上下文管理器，用于资源清理

from openai import OpenAI  # OpenAI SDK，用于调用大模型API（兼容DeepSeek等）
from dotenv import load_dotenv  # 加载.env文件中的环境变量

from mcp import ClientSession, StdioServerParameters  # MCP客户端会话和服务器参数类
from mcp.client.stdio import stdio_client  # MCP标准I/O客户端实现
from openai.types.chat import ChatCompletionToolParam  # OpenAI工具调用参数类型定义

# 加载项目根目录下的 .env 文件，读取其中配置的环境变量（如API Key）
# 这样可以避免将敏感信息硬编码在代码中，提高安全性
load_dotenv()

class MCPClient:
    """
    MCP客户端类：负责连接到MCP服务器，并通过大模型调用MCP工具。
    实现了与大模型的交互、工具调用管理以及用户聊天界面。"""
    
    def __init__(self):
        """
        初始化MCP客户端实例，配置大模型API连接参数。
        当前配置使用DeepSeek API，也可切换为OpenAI或其他兼容API。
        """
        # 创建异步退出栈，用于管理资源和清理操作
        self.exit_stack = AsyncExitStack()
        
        # 从环境变量中读取DeepSeek API配置（注释掉的是OpenAI配置示例）
        # self.openai_api_key = os.getenv("OPENAI_API_KEY")  # 读取 OpenAI API Key
        self.openai_api_key = os.getenv("DEEPSEEK_API_KEY")  # 读取 DeepSeek API Key
        
        # self.base_url = os.getenv("BASE_URL_GPT")  # 读取 OpenAI BASE URL
        self.base_url = os.getenv("BASE_URL_DEEPSEEK")  # 读取 DeepSeek BASE URL
        
        # self.model = os.getenv("MODEL_GPT")  # 读取 OpenAI model名称
        self.model = os.getenv("MODEL_DEEPSEEK")  # 读取 DeepSeek model名称
        # 验证API Key是否已正确配置，如果未找到则抛出异常终止程序
        if not self.openai_api_key:
            raise ValueError("❌ 未找到 OpenAI API Key，请在 .env 文件中设置 OPENAI_API_KEY")
        
        # 创建OpenAI客户端实例，配置API密钥和服务地址（兼容DeepSeek等第三方服务）
        self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)
        
        # 初始化MCP会话对象，用于与MCP服务器通信（初始为None）
        self.session: Optional[ClientSession] = None
        
        # 再次创建异步退出栈（注意：前面的赋值被覆盖了，这是一个小bug，但不影响功能）
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        """
        连接到指定的MCP服务器脚本，并列出服务器上可用的工具。
        :param server_script_path: MCP服务器脚本的路径（.py或.js文件）
        """
        # 检查服务器脚本的文件扩展名，确定使用的运行命令
        is_python = server_script_path.endswith('.py')  # 判断是否为Python脚本
        is_js = server_script_path.endswith('.js')      # 判断是否为JavaScript脚本
        
        # 如果既不是Python也不是JavaScript脚本，则抛出异常
        if not(is_python or is_js):
            raise ValueError("服务器脚本必须是 .py 或 .js 文件")
        
        # 根据脚本类型选择执行命令：Python用"python"，JavaScript用"node"
        command = "python" if is_python else "node"
        # 创建标准I/O服务器参数对象，配置如何启动MCP服务器进程
        server_params = StdioServerParameters(
            command=command,           # 执行命令（python或node）
            args=[server_script_path], # 传递给命令的参数（服务器脚本路径）
            env=None                   # 环境变量（None表示继承当前进程的环境）
        )

        # 启动MCP服务器进程并建立标准I/O通信管道
        # stdio_client(server_params)：以子进程方式启动服务器，并通过stdin/stdout进行通信
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        
        # 解包获取标准输入输出流：stdio用于读取服务器响应，write用于向服务器发送请求
        self.stdio, self.write = stdio_transport
        
        # 创建MCP客户端会话对象，封装与服务器的交互逻辑
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        # 向MCP服务器发送初始化消息，等待服务器就绪并建立握手连接
        await self.session.initialize()

        # 调用MCP服务器的list_tools方法，获取服务器上注册的所有可用工具列表
        response = await self.session.list_tools()
        tools = response.tools
        
        # 打印已连接的工具名称列表，方便用户了解可用功能
        print("\n已连接到服务器，支持以下工具:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """
        使用大模型处理用户查询，并根据需要自动调用MCP工具（Function Calling）。
        实现了一个完整的工具调用循环：用户提问 → 大模型判断是否需要工具 → 调用工具 → 返回结果。
        :param query: 用户的自然语言查询（如“北京今天天气怎么样？”）
        :return: 大模型生成的最终回答文本
        """
        # 构建对话消息列表，初始只包含用户的查询内容
        messages = [{"role": "user", "content": query}]

        # 再次获取MCP服务器上的可用工具列表（每次处理查询时都重新获取，确保工具列表最新）
        response = await self.session.list_tools()

        print(response.tools)  # 打印工具详细信息（调试用）

        # 将MCP工具转换为OpenAI API所需的工具参数格式（ChatCompletionToolParam）
        available_tools = [
            ChatCompletionToolParam(
                type="function",  # 工具类型为函数调用
                function={
                    "name": tool.name,              # 工具名称（如"query_weather"）
                    "description": str(tool.description),  # 工具功能描述，帮助大模型理解何时调用
                    # "input_schema": tool.inputSchema  # 原始输入模式定义（已注释）
                    "parameters": tool.inputSchema  # 工具的参数schema，定义参数类型和结构
                }
            ) for tool in response.tools  # 遍历所有MCP工具进行转换
        ]
        print(available_tools)  # 打印转换后的工具参数（调试用）
        print(self.model)  # 打印当前使用的大模型名称（调试用）
        # 调用大模型API，传入用户消息和可用工具列表，让模型决定是否调用工具
        response = self.client.chat.completions.create(
            model=self.model,       # 指定使用的大模型（如deepseek-chat）
            messages=messages,      # 对话历史消息
            tools=available_tools,  # 可用工具列表，供模型选择调用
            tool_choice="auto",     # 自动决定是否需要调用工具（也可以设置为强制调用或不调用）
        )

        print(response)  # 打印大模型的完整响应对象（调试用）
        # 提取大模型响应的第一个选择项（通常只有一个）
        content = response.choices[0]
        
        # 检查大模型的结束原因：如果是"tool_calls"，说明模型决定调用工具
        if content.finish_reason == "tool_calls":
            # 解析模型返回的工具调用信息（可能同时调用多个工具，这里只处理第一个）
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name        # 要调用的工具名称（如"query_weather"）
            tool_args = json.loads(tool_call.function.arguments)  # 工具调用参数（JSON字符串转字典）
            
            # 通过MCP会话调用指定的工具，传入解析后的参数，并等待执行结果
            result = await self.session.call_tool(tool_name, tool_args)
            print(f"\n\n[Calling tool {tool_name} with args {tool_args}]\n\n")  # 打印工具调用日志

            # 将大模型的工具调用请求和工具执行结果都添加到对话历史中，形成完整的调用链
            messages.append(content.message.model_dump())  # 添加模型的工具调用请求消息
            messages.append({
                "role": "tool",                                    # 角色标记为"tool"，表示这是工具返回的结果
                "content": result.content[0].text,                 # 工具执行的文本结果（如天气信息）
                "tool_call_id": tool_call.id,                      # 工具调用ID，用于关联请求和响应
            })

            # 将包含工具结果的完整对话历史再次发送给大模型，让其生成最终的自然语言回答
            response = self.client.chat.completions.create(
                model=self.model,   # 使用相同的大模型
                messages=messages,  # 包含用户问题、工具调用、工具结果的完整对话历史
            )
            # 返回大模型基于工具结果生成的最终回答（如“北京今天天气晴朗，温度25度...”）
            return response.choices[0].message.content

        # 如果大模型没有调用工具（finish_reason不是"tool_calls"），直接返回模型的回答内容
        # 这种情况通常是简单问答，不需要调用外部工具即可回答
        return content.message.content

    async def chat_loop(self):
        """
        运行交互式聊天循环，提供命令行聊天界面。
        用户可以持续输入问题，客户端会调用大模型和MCP工具进行处理，直到用户输入'quit'退出。
        """
        print("\n🤖 MCP 客户端已启动！输入 'quit' 退出")  # 显示欢迎信息和退出提示

        # 进入无限循环，持续接收用户输入并处理，直到用户主动退出
        while True:
            try:
                # 从控制台读取用户输入，去除首尾空格
                query = input("\n你: ").strip()
                
                # 检查用户是否输入退出命令（不区分大小写）
                if query.lower() == 'quit' or query.lower() == 'exit':
                    break  # 退出聊天循环

                # 调用process_query处理用户问题（内部可能调用大模型和MCP工具）
                response = await self.process_query(query)  # 发送用户输入到大模型API进行处理
                print(f"\n🤖 OpenAI: {response}")  # 打印大模型的回答（标签仍为OpenAI，实际可能是DeepSeek）

            except Exception as e:
                # 捕获并显示处理过程中发生的任何异常（网络错误、API限制等）
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """
        清理客户端占用的资源，关闭与MCP服务器的连接。
        在程序退出时必须调用此方法，避免资源泄漏。
        """
        # 关闭异步退出栈，会自动清理所有通过enter_async_context注册的资源（如会话、连接等）
        await self.exit_stack.aclose()

async def main():
    """
    主函数：程序入口点，负责初始化客户端、连接服务器并启动聊天界面。
    使用try-finally确保即使发生异常也能正确清理资源。
    """
    # 检查命令行参数数量，必须至少提供一个参数（MCP服务器脚本路径）
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")  # 显示使用说明
        sys.exit(1)  # 以错误码1退出程序

    # 创建MCP客户端实例
    client = MCPClient()
    try:
        # 连接到指定的MCP服务器脚本（通过命令行参数传入路径）
        await client.connect_to_server(sys.argv[1])
        
        # 启动交互式聊天循环，用户可以开始提问并与大模型和MCP工具交互
        await client.chat_loop()
    finally:
        # 无论是否发生异常，都要执行清理操作，释放资源（关闭连接、会话等）
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
