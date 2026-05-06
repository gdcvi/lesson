# MCP 天气查询系统 - 启动指南

## 📋 项目简介

这是一个基于 MCP (Model Context Protocol) 的天气查询示例项目，包含：
- **MCP 服务器**：提供天气查询工具
- **MCP 客户端**：与大模型交互并调用天气查询工具
- **城市编码数据**：用于将城市名转换为 API 所需的 district_id

## 🛠️ 环境准备

### 1. 安装依赖

```bash
pip install mcp openai python-dotenv httpx
```

### 2. 配置文件

项目已包含 `.env` 文件，配置了 DeepSeek API：

```env
BASE_URL_DEEPSEEK="https://api.deepseek.com"
MODEL_DEEPSEEK="deepseek-chat"
DEEPSEEK_API_KEY="sk-a3c....6093f34"
```

**注意**：如需使用自己的 API Key，请修改 `.env` 文件中的 `DEEPSEEK_API_KEY`。

### 3. API Key 配置

项目已配置以下 API Key：
- **百度地图 API Key**：已在 `serve.py` 中配置（`gY1JIf....lvPX`）
- **DeepSeek API Key**：已在 `.env` 文件中配置

如需更换，请修改相应位置。

## 🚀 启动步骤

### 前置检查：运行测试脚本

在正式启动前，建议先运行测试脚本验证配置是否正确：

```bash
python test.py
```

测试脚本会自动检查：
- ✅ 依赖库是否安装
- ✅ 环境变量配置是否正确
- ✅ 天气 API 是否正常工作

如果所有测试通过，就可以正式使用了！

### 方式一：命令行启动（推荐）

#### 第一步：启动 MCP 服务器

打开第一个终端窗口：

```bash
cd E:\code\GitWork\gdcvi\lesson\code23\mcp_stdio
python serve.py
```

服务器启动后，会等待客户端连接（不会有明显输出）。

#### 第二步：启动 MCP 客户端

打开**第二个终端窗口**：

```bash
cd E:\code\GitWork\gdcvi\lesson\code23\mcp_stdio
python client.py serve.py
```

客户端启动后会显示：
```
已连接到服务器，支持以下工具: ['query_weather']

🤖 MCP 客户端已启动！输入 'quit' 退出
```

### 方式二：使用批处理脚本启动

创建 `start.bat` 文件（Windows）：

```batch
@echo off
echo 正在启动 MCP 服务器...
start cmd /k "cd /d %~dp0 && python serve.py"
timeout /t 3 /nobreak >nul
echo 正在启动 MCP 客户端...
start cmd /k "cd /d %~dp0 && python client.py serve.py"
```

然后双击运行 `start.bat` 即可同时启动服务器和客户端。

## 💬 测试示例

客户端启动后，您可以输入以下测试问题：

### 基础天气查询

```
你: 北京今天的天气怎么样？
```

预期输出：
```
🤖 OpenAI: 北京当前的天气情况如下：
🌍 北京, CN
🌡 温度: 25°C
💧 湿度: 60%
🌬 风速: 3 m/s
🌤 天气: 晴
💨 风向: 北风
🌡 体感温度: 26°C
📝 描述: 晴朗
```

### 更多测试用例

```
你: 上海现在的气温是多少？
你: 广州的天气情况
你: 深圳今天下雨吗？
你: 成都的温度和湿度
```

### 退出程序

```
你: quit
```

或

```
你: exit
```


## 📁 项目结构

```
mcp_stdio/
├── serve.py                      # MCP 服务器端代码
├── client.py                     # MCP 客户端代码
├── weather_district_id.csv       # 城市编码数据文件
├── .env                          # 环境变量配置文件
└── README.md                     # 本说明文档
```

## 🔧 核心功能说明

### 服务器端 (serve.py)

- 使用 `FastMCP` 创建 MCP 服务器
- 提供 `query_weather` 工具
- 通过百度地图 API 获取实时天气数据
- 使用 CSV 文件进行城市名称到编码的映射

### 客户端 (client.py)

- 连接到 MCP 服务器
- 使用 DeepSeek API 进行函数调用
- 自动识别用户意图并调用天气查询工具
- 返回格式化的自然语言回复

### 工作流程

1. 用户输入天气查询问题
2. 客户端将问题发送给 DeepSeek API
3. DeepSeek 识别需要调用 `query_weather` 工具
4. 客户端通过 MCP 协议调用服务器的天气查询功能
5. 服务器通过百度地图 API 获取天气数据
6. 数据返回给 DeepSeek 生成自然语言回复
7. 最终结果展示给用户
