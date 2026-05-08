# MCP 天气查询系统 - 开发说明文档

## 一、项目需求分析

### 1.1 项目概述

本项目是一个基于 **MCP (Model Context Protocol)** 协议的天气查询系统，实现了大模型与外部工具的集成。系统通过两种不同的通信方式（stdio 和 SSE）提供天气查询服务，允许用户通过自然语言询问天气情况，系统会自动调用百度地图天气 API 获取实时天气数据并返回格式化的结果。

### 1.2 核心功能需求

1. **天气查询工具**：提供 `query_weather` 工具，支持查询中国各城市的实时天气信息
2. **城市编码映射**：通过 CSV 文件实现城市名称到行政区划编码（district_id）的转换
3. **大模型集成**：使用 DeepSeek API 进行自然语言理解和函数调用（Function Calling）
4. **双协议支持**：同时支持 stdio（标准输入输出）和 SSE（Server-Sent Events）两种通信方式
5. **交互式对话**：提供命令行聊天界面，用户可以持续提问并获取天气信息

### 1.3 技术栈

- **Python 异步编程**：asyncio、httpx
- **MCP 框架**：mcp.server.fastmcp、mcp.client
- **大模型 API**：DeepSeek（兼容 OpenAI SDK）
- **Web 框架**（SSE 模式）：Starlette、Uvicorn
- **环境配置**：python-dotenv
- **数据处理**：csv、json

---

## 二、stdio 与 SSE 的概念及区别

### 2.1 什么是 stdio？

**stdio（Standard Input/Output）** 是标准输入输出的通信方式，通过进程的 stdin 和 stdout 进行数据交换。

#### 工作原理：
- 客户端以子进程方式启动服务器
- 双方通过标准输入（stdin）发送消息
- 通过标准输出（stdout）接收响应
- 使用 JSON-RPC 协议进行通信

#### 特点：
- ✅ **简单直接**：无需网络配置，本地进程间通信
- ✅ **低延迟**：无网络开销，通信效率高
- ✅ **安全性好**：不暴露网络端口，仅限本地访问
- ❌ **局限性**：只能本地使用，无法跨机器部署
- ❌ **耦合性强**：客户端需要知道服务器脚本路径

#### 适用场景：
- 本地开发和调试
- 桌面应用程序集成
- 单用户工具调用

### 2.2 什么是 SSE？

**SSE（Server-Sent Events）** 是一种基于 HTTP 的单向通信技术，允许服务器向客户端推送实时更新。

#### 工作原理：
- 服务器作为 HTTP 服务运行在指定端口（如 8080）
- 客户端通过 HTTP 请求连接到服务器的 `/sse` 端点
- 建立持久连接后，服务器可以持续向客户端推送事件
- 使用 WebSocket 类似的长连接机制，但基于 HTTP

#### 特点：
- ✅ **网络通信**：支持远程访问，可跨机器部署
- ✅ **易于扩展**：多个客户端可同时连接同一服务器
- ✅ **解耦架构**：客户端只需知道服务器 URL
- ❌ **配置复杂**：需要处理端口、防火墙等网络问题
- ❌ **资源消耗**：维持 HTTP 连接需要更多系统资源

#### 适用场景：
- 分布式系统架构
- 多用户共享服务
- 云端部署应用
- 微服务间通信

### 2.3 stdio 与 SSE 的核心区别对比

| 对比维度 | stdio | SSE |
|---------|-------|-----|
| **通信方式** | 进程间标准输入输出 | HTTP 长连接 |
| **部署范围** | 仅本地 | 本地或远程 |
| **启动方式** | 客户端启动服务器子进程 | 服务器独立运行，客户端连接 URL |
| **网络依赖** | 无需网络 | 需要网络连接 |
| **并发能力** | 一对一通信 | 一对多通信 |
| **配置复杂度** | 简单（只需脚本路径） | 复杂（需配置 URL、端口） |
| **性能** | 更高（无网络开销） | 略低（有 HTTP 开销） |
| **安全性** | 高（不暴露端口） | 需注意网络安全 |
| **典型应用** | 本地 CLI 工具 | Web 服务、云应用 |

### 2.4 本项目的实现差异

#### stdio 模式（mcp_stdio）：
```python
# 服务器端
mcp.run(transport='stdio')  # 以 stdio 方式运行

# 客户端
stdio_transport = await stdio_client(server_params)  # 启动子进程
```

#### SSE 模式（mcp_sse）：
```python
# 服务器端
app = Starlette(routes=[Route('/sse', endpoint=sse_handler)])
uvicorn.run(app, host="127.0.0.1", port=8080)  # 启动 HTTP 服务

# 客户端
sse_transport = await sse_client(url="http://127.0.0.1:8080/sse")  # 连接 URL
```

---

## 三、整体架构说明

### 3.1 系统架构图

```
┌─────────────────────────────────────────────────────┐
│                    用户交互层                         │
│  ┌──────────────────────────────────────────────┐   │
│  │         MCP Client (client.py /              │   │
│  │          client_sse.py)                      │   │
│  │  - 接收用户自然语言输入                       │   │
│  │  - 调用 DeepSeek API 进行意图识别             │   │
│  │  - 管理 Function Calling 流程                │   │
│  └──────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     │ MCP 协议通信
                     │ (stdio 或 SSE)
                     │
┌────────────────────▼────────────────────────────────┐
│                   MCP 服务层                         │
│  ┌──────────────────────────────────────────────┐   │
│  │      MCP Server (serve.py / serve_sse.py)    │   │
│  │  - 注册 query_weather 工具                    │   │
│  │  - 接收工具调用请求                           │   │
│  │  - 执行天气数据获取逻辑                       │   │
│  └──────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     │ HTTP GET 请求
                     │
┌────────────────────▼────────────────────────────────┐
│                  外部 API 层                         │
│  ┌──────────────────────────────────────────────┐   │
│  │     百度地图天气 API                          │   │
│  │  - 根据 district_id 获取实时天气              │   │
│  │  - 返回 JSON 格式天气数据                     │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

辅助组件：
┌─────────────────────────────────────────────────────┐
│  weather_district_id.csv  → 城市名 ↔ 编码映射       │
│  .env  → API Key 和环境配置                         │
│  DeepSeek API  → 大模型自然语言处理                  │
└─────────────────────────────────────────────────────┘
```

### 3.2 核心组件说明

#### 3.2.1 MCP 服务器（Server）

**职责**：
- 注册并提供 `query_weather` 工具
- 处理来自客户端的工具调用请求
- 调用百度地图 API 获取天气数据
- 格式化天气数据并返回

**关键代码结构**：
```python
# 1. 初始化 MCP 服务器
mcp = FastMCP("WeatherServer")

# 2. 定义工具函数
@mcp.tool(name="query_weather")
async def query_weather(city: str) -> str:
    data = await fetch_weather(city)
    return format_weather(data)

# 3. 启动服务器（stdio 或 SSE）
mcp.run(transport='stdio')  # stdio 模式
# 或
uvicorn.run(app, host="127.0.0.1", port=8080)  # SSE 模式
```

**核心函数**：
- `find_code()`：从 CSV 文件中查找城市编码
- `get_url()`：构建百度天气 API 请求 URL
- `fetch_weather()`：异步获取天气数据
- `format_weather()`：格式化天气数据为可读文本

#### 3.2.2 MCP 客户端（Client）

**职责**：
- 连接到 MCP 服务器（stdio 或 SSE）
- 接收用户输入的自然语言问题
- 调用 DeepSeek API 进行意图识别
- 根据模型决策调用 MCP 工具
- 将工具结果返回给模型生成最终回答

**关键代码结构**：
```python
class MCPClient:
    def __init__(self):
        # 初始化 DeepSeek 客户端
        self.client = OpenAI(api_key=api_key, base_url=base_url)
    
    async def connect_to_server(self, ...):
        # 连接到 MCP 服务器
        # stdio: stdio_client(server_params)
        # SSE: sse_client(url=server_url)
    
    async def process_query(self, query: str):
        # 1. 调用 DeepSeek API
        # 2. 检查是否需要调用工具
        # 3. 执行工具调用
        # 4. 将结果返回给模型生成最终答案
```

**核心流程**：
```
用户输入 → DeepSeek API → 判断是否需要工具 
                              ↓
                        需要工具？
                         ↙        ↘
                       是          否
                       ↓           ↓
                 调用 MCP 工具   直接返回答案
                       ↓
                 获取工具结果
                       ↓
                 再次调用 DeepSeek
                       ↓
                   返回最终答案
```

#### 3.2.3 数据流转过程

**完整调用链路**：

1. **用户输入**："北京今天的天气怎么样？"
   
2. **客户端处理**：
   - 将用户输入发送给 DeepSeek API
   - DeepSeek 分析语义，决定调用 `query_weather` 工具
   - 解析出参数：`city="北京"`

3. **MCP 协议通信**：
   - 客户端通过 MCP 协议调用服务器的 `query_weather` 工具
   - 传递参数：`{"city": "北京"}`

4. **服务器执行**：
   - `find_code()`：从 CSV 查找"北京"的编码（如 110100）
   - `get_url()`：构建 API URL
   - `fetch_weather()`：调用百度地图 API
   - `format_weather()`：格式化返回数据

5. **结果返回**：
   - 服务器返回格式化的天气字符串
   - 客户端将结果发送给 DeepSeek
   - DeepSeek 生成自然语言回复

6. **最终输出**：
   ```
   🤖 OpenAI: 北京当前的天气情况如下：
   🌍 北京, CN
   🌡 温度: 25°C
   💧 湿度: 60%
   🌬 风速: 东北风 3级
   🌤 天气: 晴
   📝 描述: 晴朗
   ```

### 3.3 项目目录结构

```
code23/
├── mcp_stdio/                    # stdio 模式实现
│   ├── serve.py                  # MCP 服务器（stdio）
│   ├── client.py                 # MCP 客户端（stdio）
│   ├── test.py                   # 测试脚本
│   ├── weather_district_id.csv   # 城市编码数据
│   ├── .env                      # 环境变量配置
│   └── README.md                 # 使用说明
│
├── mcp_sse/                      # SSE 模式实现
│   ├── serve_sse.py              # MCP 服务器（SSE）
│   ├── client_sse.py             # MCP 客户端（SSE）
│   ├── weather_district_id.csv   # 城市编码数据
│   ├── .env                      # 环境变量配置
│   └── README.md                 # 使用说明
│
└── 配置.md                        # 配置文件说明
```

---

## 四、开发步骤详解

### 4.1 第一阶段：搭建整体框架

#### 步骤 1：环境准备

**1.1 安装依赖包**

```bash
pip install mcp openai python-dotenv httpx
# SSE 模式额外需要
pip install uvicorn starlette
```

**1.2 配置环境变量**

创建 `.env` 文件：
```env
BASE_URL_DEEPSEEK="https://api.deepseek.com"
MODEL_DEEPSEEK="deepseek-chat"
DEEPSEEK_API_KEY="your_api_key_here"
ak="baidu_map_api_key_here"
```

**1.3 准备城市编码数据**

准备 `weather_district_id.csv` 文件，包含以下列：
- `district`：城市名称（如"北京"）
- `districtcode`：行政区划编码（如"110100"）

#### 步骤 2：设计服务器架构

**2.1 选择通信模式**

根据需求决定使用 stdio 还是 SSE：
- **本地开发/CLI 工具** → 选择 stdio
- **网络服务/多用户** → 选择 SSE

**2.2 服务器基本结构**

```python
# 导入必要的库
from mcp.server.fastmcp import FastMCP
import httpx
import csv

# 初始化 MCP 服务器
mcp = FastMCP("WeatherServer")

# 定义工具函数
@mcp.tool(name="query_weather")
async def query_weather(city: str) -> str:
    """查询天气的工具"""
    pass

# 启动服务器
if __name__ == "__main__":
    # stdio 模式
    mcp.run(transport='stdio')
    
    # 或 SSE 模式
    # uvicorn.run(app, host="127.0.0.1", port=8080)
```

#### 步骤 3：设计客户端架构

**3.1 客户端类结构**

```python
class MCPClient:
    def __init__(self):
        # 初始化 DeepSeek 客户端
        pass
    
    async def connect_to_server(self, ...):
        # 连接 MCP 服务器
        pass
    
    async def process_query(self, query: str):
        # 处理用户查询
        pass
    
    async def chat_loop(self):
        # 交互式聊天循环
        pass
    
    async def cleanup(self):
        # 资源清理
        pass
```

**3.2 主流程设计**

```python
async def main():
    # 1. 创建客户端实例
    client = MCPClient()
    
    try:
        # 2. 连接到服务器
        await client.connect_to_server(...)
        
        # 3. 启动聊天循环
        await client.chat_loop()
    finally:
        # 4. 清理资源
        await client.cleanup()
```

---

### 4.2 第二阶段：实现服务器端细节

#### 步骤 4：实现城市编码查找功能

```python
def find_code(csv_file_path, district_name) -> str:
    """
    根据城市名称从 CSV 文件中查找编码
    
    参数：
    - csv_file_path: CSV 文件路径
    - district_name: 城市名称（如"北京"）
    
    返回：
    - 城市编码字符串，找不到返回 None
    """
    district_map = {}
    
    with open(csv_file_path, mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            district_code = row['districtcode'].strip()
            district = row['district'].strip()
            
            if district not in district_map:
                district_map[district] = district_code
    
    return district_map.get(district_name, None)
```

**关键点**：
- 使用 `DictReader` 读取 CSV，自动将每行转换为字典
- 建立城市名到编码的映射关系（避免重复）
- 注意 UTF-8 编码以支持中文

#### 步骤 5：实现天气 API 调用

```python
def get_url(city: str) -> str:
    """构建百度天气 API URL"""
    district_code = find_code('weather_district_id.csv', city)
    url = f'https://api.map.baidu.com/weather/v1/?district_id={district_code}&data_type=now&ak=YOUR_AK'
    return url


async def fetch_weather(city: str) -> dict[str, Any] | None:
    """
    异步获取天气数据
    
    参数：
    - city: 城市名称
    
    返回：
    - 天气数据字典，出错返回包含 error 键的字典
    """
    async with httpx.AsyncClient() as client:
        try:
            url = get_url(city)
            response = await client.get(url)
            response.raise_for_status()  # 检查 HTTP 状态码
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP 错误: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"请求失败: {str(e)}"}
```

**关键点**：
- 使用 `httpx.AsyncClient` 进行异步 HTTP 请求
- 异常处理要区分 HTTP 错误和其他错误
- 返回统一的错误格式便于后续处理

#### 步骤 6：实现数据格式化

```python
def format_weather(data: dict[str, Any] | str) -> str:
    """
    将天气数据格式化为易读文本
    
    参数：
    - data: 天气数据（字典或 JSON 字符串）
    
    返回：
    - 格式化后的天气信息字符串
    """
    # 如果传入的是字符串，先解析为字典
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            return f"无法解析天气数据: {e}"
    
    # 检查是否有错误
    if "error" in data:
        return f"⚠️ {data['error']}"
    
    # 提取百度天气 API 的数据
    text = data["result"]["now"]['text']         # 天气现象
    temp = data["result"]["now"]['temp']         # 温度
    feels_like = data["result"]["now"]['feels_like']  # 体感温度
    rh = data["result"]["now"]['rh']             # 湿度
    wind_dir = data["result"]["now"]['wind_dir'] # 风向
    wind_class = data["result"]["now"]['wind_class']  # 风力等级
    
    # 构建格式化字符串
    return (
        f"🌍 城市\n"
        f"🌡 温度: {temp}°C\n"
        f"💧 湿度: {rh}%\n"
        f"🌬 风向: {wind_dir}\n"
        f"💨 风力: {wind_class}级\n"
        f"🌡 体感温度: {feels_like}°C\n"
        f"📝 描述: {text}"
    )
```

**关键点**：
- 支持字典和字符串两种输入类型
- 优先检查错误信息
- 使用 emoji 增强可读性
- 做好字段缺失的容错处理

#### 步骤 7：注册 MCP 工具

```python
@mcp.tool(name="query_weather")
async def query_weather(city: str) -> str:
    """
    查询指定城市的实时天气信息
    
    参数：
    - city: 城市名称（中文，如"北京"）
    
    返回：
    - 格式化后的天气信息字符串
    """
    print(f"调用了query_weather工具，参数为：{city}")
    data = await fetch_weather(city)
    return format_weather(data)
```

**关键点**：
- 使用 `@mcp.tool()` 装饰器注册工具
- 工具名称要与客户端期望的一致
- 添加清晰的 docstring 帮助大模型理解工具用途

#### 步骤 8：启动服务器

**stdio 模式**：
```python
if __name__ == "__main__":
    mcp.run(transport='stdio')
```

**SSE 模式**：
```python
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
import uvicorn

sse_transport = SseServerTransport('/messages/')

async def sse_handler(request):
    async with sse_transport.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp._mcp_server.run(streams[0], streams[1], mcp._mcp_server.create_initialization_options())

app = Starlette(
    debug=True,
    routes=[
        Route('/sse', endpoint=sse_handler),
        Mount('/messages/', app=sse_transport.handle_post_message)
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
```

---

### 4.3 第三阶段：实现客户端细节

#### 步骤 9：初始化客户端

```python
class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        
        # 从环境变量读取配置
        self.openai_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("BASE_URL_DEEPSEEK")
        self.model = os.getenv("MODEL_DEEPSEEK")
        
        # 验证 API Key
        if not self.openai_api_key:
            raise ValueError("❌ 未找到 API Key，请在 .env 文件中设置")
        
        # 创建 OpenAI 客户端（兼容 DeepSeek）
        self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)
        
        # MCP 会话对象
        self.session: Optional[ClientSession] = None
```

**关键点**：
- 使用 `AsyncExitStack` 管理异步资源
- 从 `.env` 文件读取敏感信息
- 验证必要配置是否存在

#### 步骤 10：连接服务器

**stdio 模式**：
```python
async def connect_to_server(self, server_script_path: str):
    """连接到 stdio 模式的 MCP 服务器"""
    # 检查文件类型
    is_python = server_script_path.endswith('.py')
    if not is_python:
        raise ValueError("服务器脚本必须是 .py 文件")
    
    # 配置服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=[server_script_path],
        env=None
    )
    
    # 建立 stdio 连接
    stdio_transport = await self.exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    self.stdio, self.write = stdio_transport
    
    # 创建会话并初始化
    self.session = await self.exit_stack.enter_async_context(
        ClientSession(self.stdio, self.write)
    )
    await self.session.initialize()
    
    # 列出可用工具
    response = await self.session.list_tools()
    print("\n已连接到服务器，支持以下工具:", [tool.name for tool in response.tools])
```

**SSE 模式**：
```python
async def connect_to_server(self, server_url: str):
    """连接到 SSE 模式的 MCP 服务器"""
    # 建立 SSE 连接
    sse_transport = await self.exit_stack.enter_async_context(
        sse_client(
            url=server_url,
            headers=None,
            timeout=5,
            sse_read_timeout=300
        )
    )
    self.stdio, self.write = sse_transport
    
    # 创建会话并初始化（同 stdio）
    self.session = await self.exit_stack.enter_async_context(
        ClientSession(self.stdio, self.write)
    )
    await self.session.initialize()
    
    # 列出可用工具
    response = await self.session.list_tools()
    print("\n已连接到服务器，支持以下工具:", [tool.name for tool in response.tools])
```

**关键点**：
- stdio 需要指定脚本路径，SSE 需要指定 URL
- 使用 `enter_async_context` 确保资源正确清理
- 初始化后立即列出工具验证连接成功

#### 步骤 11：实现工具调用逻辑

```python
async def process_query(self, query: str) -> str:
    """
    处理用户查询，支持 Function Calling
    
    流程：
    1. 调用 DeepSeek API，传入可用工具列表
    2. 检查模型是否决定调用工具
    3. 如果需要，执行工具调用
    4. 将工具结果返回给模型生成最终答案
    """
    messages = [{"role": "user", "content": query}]
    
    # 获取可用工具列表
    response = await self.session.list_tools()
    
    # 转换为 OpenAI 工具格式
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
    
    # 第一次调用：让模型决定是否使用工具
    response = self.client.chat.completions.create(
        model=self.model,
        messages=messages,
        tools=available_tools,
        tool_choice="auto",  # 自动决定是否调用工具
    )
    
    content = response.choices[0]
    
    # 检查是否需要调用工具
    if content.finish_reason == "tool_calls":
        # 解析工具调用信息
        tool_call = content.message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        
        print(f"\n[Calling tool {tool_name} with args {tool_args}]\n")
        
        # 执行工具调用
        result = await self.session.call_tool(tool_name, tool_args)
        
        # 将工具调用和结果添加到对话历史
        messages.append(content.message.model_dump())
        messages.append({
            "role": "tool",
            "content": result.content[0].text,
            "tool_call_id": tool_call.id,
        })
        
        # 第二次调用：让模型基于工具结果生成最终答案
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        
        return response.choices[0].message.content
    
    # 如果不需要工具，直接返回模型答案
    return content.message.content
```

**关键点**：
- 工具调用是一个两轮对话过程
- 第一轮：模型决定是否需要工具
- 第二轮：模型基于工具结果生成答案
- 必须正确维护 `messages` 对话历史

#### 步骤 12：实现聊天循环

```python
async def chat_loop(self):
    """运行交互式聊天循环"""
    print("\n🤖 MCP 客户端已启动！输入 'quit' 退出")
    
    while True:
        try:
            # 读取用户输入
            query = input("\n你: ").strip()
            
            # 检查退出条件
            if query.lower() in ['quit', 'exit']:
                break
            
            # 处理查询并显示结果
            response = await self.process_query(query)
            print(f"\n🤖 OpenAI: {response}")
        
        except Exception as e:
            print(f"\n⚠️ 发生错误: {str(e)}")
```

#### 步骤 13：资源清理

```python
async def cleanup(self):
    """清理资源，关闭连接"""
    await self.exit_stack.aclose()
```

**关键点**：
- 必须在程序退出时调用
- 关闭所有通过 `enter_async_context` 打开的资源

#### 步骤 14：主函数入口

```python
async def main():
    """程序入口"""
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
    
    # 创建客户端
    client = MCPClient()
    
    try:
        # 连接服务器
        await client.connect_to_server(sys.argv[1])
        
        # 启动聊天
        await client.chat_loop()
    finally:
        # 确保资源清理
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 4.4 第四阶段：测试与调试

#### 步骤 15：编写测试脚本

创建 `test.py` 用于验证配置：

```python
"""测试脚本：验证配置是否正确"""
import asyncio
from serve import query_weather_1

async def test():
    print("=" * 50)
    print("测试 1：检查依赖库")
    try:
        import mcp, openai, httpx, dotenv
        print("✅ 所有依赖库已安装")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        return
    
    print("\n" + "=" * 50)
    print("测试 2：检查环境变量")
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key:
        print(f"✅ API Key 已配置: {api_key[:10]}...")
    else:
        print("❌ 未找到 DEEPSEEK_API_KEY")
        return
    
    print("\n" + "=" * 50)
    print("测试 3：测试天气 API")
    try:
        result = await query_weather_1("北京")
        print("✅ 天气 API 调用成功")
        print(f"结果预览: {result[:100]}...")
    except Exception as e:
        print(f"❌ 天气 API 调用失败: {e}")
        return
    
    print("\n" + "=" * 50)
    print("🎉 所有测试通过！可以正式使用了")

if __name__ == "__main__":
    asyncio.run(test())
```

#### 步骤 16：运行测试

```bash
# 1. 运行测试脚本
python test.py

# 预期输出：
# ==================================================
# 测试 1：检查依赖库
# ✅ 所有依赖库已安装
# 
# ==================================================
# 测试 2：检查环境变量
# ✅ API Key 已配置: sk-a3c6097e...
# 
# ==================================================
# 测试 3：测试天气 API
# ✅ 天气 API 调用成功
# 结果预览: 🌍 北京, CN
# 🌡 温度: 25°C
# ...
# 
# ==================================================
# 🎉 所有测试通过！可以正式使用了
```

#### 步骤 17：启动完整系统

**stdio 模式**：

终端 1（启动服务器）：
```bash
cd mcp_stdio
python serve.py
```

终端 2（启动客户端）：
```bash
cd mcp_stdio
python client.py serve.py
```

**SSE 模式**：

终端 1（启动服务器）：
```bash
cd mcp_sse
python serve_sse.py
# 服务器运行在 http://127.0.0.1:8080
```

终端 2（启动客户端）：
```bash
cd mcp_sse
python client_sse.py http://127.0.0.1:8080/sse
```

#### 步骤 18：功能测试

启动客户端后，尝试以下测试用例：

```
你: 北京今天的天气怎么样？
🤖 OpenAI: 北京当前的天气情况如下：
🌍 北京, CN
🌡 温度: 25°C
💧 湿度: 60%
...

你: 上海现在的气温是多少？
🤖 OpenAI: 上海当前的气温是 28°C...

你: 广州的天气情况
🤖 OpenAI: 广州当前的天气情况...

你: quit
```

---

## 五、配置说明

### 5.1 stdio 模式配置

在 MCP 客户端配置文件（如 Claude Desktop 配置）中添加：

**使用 uv 运行**：
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "E:\\code\\GitWork\\gdcvi\\lesson\\code23\\mcp_stdio\\serve.py"
      ]
    }
  }
}
```

**使用 conda 环境**：
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "D:\\Anaconda\\envs\\lesson\\python.exe",
      "args": ["E:\\code\\GitWork\\gdcvi\\lesson\\code23\\mcp_stdio\\serve.py"]
    }
  }
}
```

### 5.2 SSE 模式配置

**第一步**：启动服务器
```bash
python serve_sse.py
```

**第二步**：在配置文件中添加：
```json
{
  "mcpServers": {
    "weather-server-sse": {
      "url": "http://127.0.0.1:8080/sse"
    }
  }
}
```

**注意**：确保配置的端口与服务器启动时的端口一致（默认 8080）。

---

## 八、总结

本项目通过 MCP 协议实现了大模型与外部天气 API 的集成，展示了两种不同的通信方式（stdio 和 SSE）的实现方法。

**核心要点**：
1. **MCP 协议**：标准化的工具调用协议，使大模型能够调用外部工具
2. **stdio vs SSE**：根据使用场景选择合适的通信方式
3. **Function Calling**：大模型通过语义理解自动决定何时调用工具
4. **异步编程**：使用 asyncio 提高并发性能
5. **模块化设计**：服务器、客户端、工具函数分离，便于维护和扩展

**学习价值**：
- 理解 MCP 协议的工作原理
- 掌握大模型工具调用的实现方法
- 学习异步 HTTP 请求和 Web 服务开发
- 实践完整的项目开发流程

