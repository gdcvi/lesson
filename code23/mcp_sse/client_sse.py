"""
 * @author: zkyuan
 * @date: 2026/5/8 15:37
 * @description: mcp的sse方式 客户端
"""
import asyncio
import os
import json
from typing import Optional
from contextlib import AsyncExitStack

from openai import OpenAI
from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.sse import sse_client
from openai.types.chat import ChatCompletionToolParam

# 加载 .env 文件，确保 API Key 受到保护
load_dotenv()


class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        self.openai_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("BASE_URL_DEEPSEEK")
        self.model = os.getenv("MODEL_DEEPSEEK")
        if not self.openai_api_key:
            raise ValueError("❌ 未找到 OpenAI API Key，请在 .env 文件中设置 OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_url: str):
        """连接到 MCP 服务器并列出可用工具"""
        # 使用 SSE 客户端连接到服务器
        sse_transport = await self.exit_stack.enter_async_context(
            sse_client(
                url=server_url,
                headers=None,
                timeout=5,
                sse_read_timeout=60 * 5
            )
        )

        # 拿到读写流
        self.stdio, self.write = sse_transport
        # 创建 MCP 客户端会话，与服务器交互
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        # 发送初始化消息给服务器，等待服务器就绪
        await self.session.initialize()

        # 列出 MCP 服务器上的工具
        response = await self.session.list_tools()
        tools = response.tools
        print("\n已连接到服务器，支持以下工具:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """
        使用大模型处理查询并调用可用的 MCP 工具 (Function Calling)
        """
        messages = [{"role": "system", "content": "调用工具时传入的参数为中文"}, {"role": "user", "content": query}]

        response = await self.session.list_tools()

        print(response.tools)

        available_tools = [
            ChatCompletionToolParam(
                type="function",
                function={
                    "name": tool.name,
                    "description": str(tool.description),
                    "parameters": tool.inputSchema
                }
            ) for tool in response.tools
        ]
        print(available_tools)
        print(self.model)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=available_tools,
            tool_choice="auto",
        )

        print(response)
        # 处理返回的内容
        content = response.choices[0]
        if content.finish_reason == "tool_calls":
            # 如何是需要使用工具，就解析工具
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # 执行工具
            result = await self.session.call_tool(tool_name, tool_args)
            print(f"\n\n[Calling tool {tool_name} with args {tool_args}]\n\n")

            # 将模型返回的调用哪个工具数据和工具执行完成后的数据都存入messages中
            messages.append(content.message.model_dump())
            messages.append({
                "role": "tool",
                "content": result.content[0].text,
                "tool_call_id": tool_call.id,
            })

            # 将上面的结果再返回给大模型用于生产最终的结果
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return response.choices[0].message.content

        return content.message.content

    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\n🤖 MCP 客户端已启动！输入 'quit' 或 'exit' 退出")

        while True:
            try:
                query = input("\n你: ").strip()
                if query.lower() == 'quit' or query.lower() == 'exit':
                    break

                response = await self.process_query(query)  # 发送用户输入到 OpenAI API
                print(f"\n🤖 OpenAI: {response}")

            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()


async def main():
    # 检查命令行的参数是否小于2
    if len(sys.argv) < 2:
        print("Usage: uv run client_sse.py <server_url>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys

    asyncio.run(main())

    # uv run client_sse.py  http://127.0.0.1:8080/sse
    # python client_sse.py  http://127.0.0.1:8080/sse