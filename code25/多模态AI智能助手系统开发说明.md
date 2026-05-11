# 多模态 AI 智能助手系统 - 开发说明文档

## 一、项目需求分析

### 1.1 项目概述

本项目是一个基于 **阿里云 DashScope（通义千问）** 大模型生态的 **一站式多模态 AI 智能助手平台**。系统通过 Streamlit Web 界面提供八大核心能力：RAG 文档问答、文生图、图片解读、图生视频、文生音频、音频生文、Excel 数据分析和知识库管理。用户可以通过自然语言与系统交互，实现文本、图像、视频、音频等多种模态的智能处理。

### 1.2 核心功能需求

1. **知识库管理**：创建持久化向量知识库，上传文档（PDF/TXT/DOCX/MD/CSV/XLSX），自动分块并嵌入 ChromaDB
2. **RAG 文档问答**：基于持久化知识库或临时上传文档进行检索增强生成问答，支持流式输出和来源引用
3. **文生图**：使用通义万相模型从文本生成图像，支持风格预设、负面提示词、多尺寸和批量生成
4. **图片解读**：AI 视觉分析图像，支持详细描述、构图分析、OCR 文字提取、情感分析等模板
5. **图生视频**：将静态图像转换为动态视频，支持多种运动模板
6. **文生音频（TTS）**：将文本转换为自然语音，支持 6 种音色、语速调节、音量控制
7. **音频生文（ASR）**：音频文件转录，支持中英混合识别，提供句级/词级时间戳
8. **Excel 数据助手**：上传表格数据，支持预览、筛选、排序，生成交互式 Plotly 图表和统计分析

### 1.3 技术栈

| 层级 | 技术 |
|------|------|
| **Web 框架** | Streamlit（多页面应用 + 侧边栏导航） |
| **大语言模型** | Qwen-Plus / Qwen-Max / Qwen-Turbo，通过 LangChain `ChatOpenAI` 调用 DashScope 兼容接口 |
| **视觉模型** | Qwen-VL-Plus / Qwen-VL-Max |
| **文本嵌入** | `text-embedding-v3`（DashScopeEmbeddings） |
| **向量数据库** | ChromaDB（langchain-chroma），持久化存储 |
| **RAG 编排** | LangChain（ChatPromptTemplate、RunnablePassthrough、StrOutputParser、RecursiveCharacterTextSplitter） |
| **图像生成** | DashScope `ImageSynthesis` SDK（通义万相 2.2） |
| **视频生成** | DashScope `VideoSynthesis` SDK（通义万相 2.1） |
| **语音合成** | DashScope `SpeechSynthesizer`（CosyVoice v2） |
| **语音识别** | DashScope `Transcription` SDK（Paraformer v2） |
| **数据处理** | Pandas、openpyxl、PyPDF2、docx2txt |
| **数据可视化** | Plotly（交互式图表） |
| **配置管理** | python-dotenv、JSON 配置文件 |

---

## 二、整体架构说明

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      用户交互层（Streamlit）                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  app.py（主页） + pages/*.py（10 个功能页面）            │  │
│  │  - 首页导航        - RAG 文档问答    - 文生图            │  │
│  │  - 图片解读        - 图生视频        - 文生音频          │  │
│  │  - 音频生文        - 系统设置        - Excel 助手        │  │
│  │  - 知识库管理                                            │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ 调用服务模块
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      服务模块层（modules/）                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ llm_service  │ │ chat_engine  │ │document_proc │        │
│  │ LLM/视觉服务  │ │ RAG 对话引擎  │ │ 文档处理     │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ vector_store │ │ image_service│ │ video_service│        │
│  │ 向量库管理    │ │ 文生图服务    │ │ 图生视频服务  │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │audio_service │ │ model_config │ │prompt_manager│        │
│  │ TTS/ASR 服务  │ │ 模型配置管理  │ │ 提示词管理   │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└──────────────────────────┬──────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
┌────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  DashScope API │ │   ChromaDB   │ │  本地文件系统      │
│  (阿里云百炼)    │ │  向量数据库    │ │  data/outputs/    │
│  ├─ ChatOpenAI │ │  知识库持久化  │ │  图片/视频/音频    │
│  ├─ ImageSynth │ └──────────────┘ └──────────────────┘
│  ├─ VideoSynth │
│  ├─ SpeechSynth│
│  ├─ Transcribe │
│  └─ Embeddings │
└────────────────┘
```

### 2.2 核心组件说明

#### 2.2.1 配置层（config/）

**`settings.py`** — 集中配置管理，从 `.env` 加载环境变量，定义所有模型列表、TTS 音色字典、图片尺寸选项、RAG 参数（chunk_size=1000, overlap=200, top_k=5）、文件上传限制、存储路径和颜色方案常量。

**`prompts.json`** — 5 个内置提示词模板：通用问答、专业专家、创意写作、文档摘要、教学导师，每个包含 system_prompt、temperature 和 max_tokens。

#### 2.2.2 服务模块层（modules/）

**`llm_service.py`** — 核心服务类 `LLMService`，创建指向 DashScope 兼容 API 的 `ChatOpenAI` 实例。提供文本对话（流式/非流式）、视觉理解（URL/本地图片）、视频理解、多图对比、API 连接测试等功能。通过 `get_llm_service()` 获取 Streamlit 缓存的单例。

**`chat_engine.py`** — RAG 对话引擎 `ChatEngine`，封装 `LLMService` 构建 LangChain RAG 链：`chat_with_rag()` / `stream_chat_with_rag()` 从检索器获取文档，构建上下文，通过提示模板 + LLM 链返回答案和来源引用。

**`document_processor.py`** — 文档处理器 `DocumentProcessor`，使用 LangChain 加载器加载多种格式文档，通过 `RecursiveCharacterTextSplitter` 进行中文感知分块，处理上传文件、元数据标记和临时文件清理。

**`vector_store.py`** — 向量库管理器 `VectorStoreManager`，管理 ChromaDB 集合与 DashScope 嵌入：集合增删改查、文档入库、检索器工厂、中文集合名处理、元数据持久化。

**`image_service.py`** — 图像服务 `ImageService`，封装 DashScope `ImageSynthesis`，支持同步/异步图像生成，自动下载到 `data/outputs/images/`。

**`video_service.py`** — 视频服务 `VideoService`，封装 DashScope `VideoSynthesis`，提交图生视频任务，轮询完成状态，下载结果。

**`audio_service.py`** — 两个服务类：`TTSService`（语音合成，支持 6 种音色、语速、音量、格式配置）和 `ASRService`（语音识别，支持同步/异步/详细时间戳模式）。

**`model_config.py`** — 模型配置管理器 `ModelConfigManager`，持久化用户模型偏好到 JSON 文件，支持预设系统（保存/加载/列出预设）。

**`prompt_manager.py`** — 提示词管理器 `PromptManager`，加载默认提示词和自定义提示词，支持增删改查、分类过滤。

#### 2.2.3 工具层（utils/）

**`file_utils.py`** — 文件工具函数：图片下载、视频下载、Base64 编码、ASR 文本提取、时间戳获取、MIME 类型判断、文件大小格式化。

**`ui_helpers.py`** — UI 工具函数：自定义 CSS 注入、API Key 检查、卡片渲染、状态徽章、章节标题。

#### 2.2.4 页面层（pages/）

10 个 Streamlit 多页面应用，每个页面有独立的侧边栏配置和主内容区，通过 `st.switch_page()` 实现页面间导航。

### 2.3 数据流转过程

**RAG 文档问答完整流程**：

1. **用户上传文档** → `DocumentProcessor` 加载并分块
2. **文档入库** → `VectorStoreManager` 调用 DashScope Embeddings 生成向量，存入 ChromaDB
3. **用户提问** → `ChatEngine` 从 ChromaDB 检索相关文档片段
4. **构建上下文** → 将检索结果拼入提示模板
5. **LLM 生成** → 调用 DashScope Qwen 模型生成回答
6. **流式输出** → 前端 Streamlit 逐步展示回答和来源引用

**文生图完整流程**：

1. **用户输入提示词** → 选择风格预设、尺寸、数量
2. **调用 DashScope ImageSynthesis** → 提交生成任务
3. **轮询等待完成** → 获取图像 URL
4. **下载图像** → 保存到 `data/outputs/images/`
5. **前端展示** → 显示图像并提供下载按钮

### 2.4 项目目录结构

```
code25/
├── .env                          # 环境变量配置（API Key 等）
├── .env.example                  # 环境变量模板
├── app.py                        # Streamlit 主入口（首页）
├── start.py                      # CLI 启动脚本（环境检查 + 启动）
├── requirements.txt              # Python 依赖清单
│
├── config/                       # 配置层
│   ├── __init__.py
│   ├── settings.py               # 集中配置（模型列表、参数、路径）
│   └── prompts.json              # 内置提示词模板
│
├── modules/                      # 服务模块层
│   ├── __init__.py
│   ├── llm_service.py            # LLM/视觉模型服务
│   ├── chat_engine.py            # RAG 对话引擎
│   ├── document_processor.py     # 文档加载与分块
│   ├── vector_store.py           # ChromaDB 向量库管理
│   ├── image_service.py          # 文生图服务
│   ├── video_service.py          # 图生视频服务
│   ├── audio_service.py          # TTS + ASR 服务
│   ├── model_config.py           # 模型配置持久化
│   └── prompt_manager.py         # 提示词模板管理
│
├── pages/                        # 页面层（Streamlit 多页面）
│   ├── 01_首页.py                 # 功能导航首页
│   ├── 02_RAG文档问答.py         # RAG 文档问答
│   ├── 03_文生图.py              # 文本生成图像
│   ├── 04_图片解读.py            # 图像视觉理解
│   ├── 05_图生视频.py            # 图像生成视频
│   ├── 06_文生音频.py            # 文本转语音
│   ├── 07_音频生文.py            # 语音转文本
│   ├── 08_系统设置.py            # 系统配置管理
│   ├── 09_Excel助手.py           # 表格数据分析
│   └── 10_知识库管理.py          # 知识库 CRUD
│
├── utils/                        # 工具层
│   ├── __init__.py
│   ├── file_utils.py             # 文件处理工具
│   └── ui_helpers.py             # UI 渲染工具
│
└── data/                         # 数据存储目录
    ├── outputs/
    │   ├── audio/                # 生成的音频文件
    │   ├── images/               # 生成的图像文件
    │   └── videos/               # 生成的视频文件
    ├── knowledge_bases/          # ChromaDB 持久化目录
    ├── temp_docs/                # 临时上传文档
    └── cache/                    # 缓存目录
```

---

## 三、开发步骤详解

### 3.1 第一阶段：项目初始化与基础框架搭建

#### 步骤 1：环境准备

**1.1 创建项目目录结构**

```bash
mkdir -p config modules pages utils
mkdir -p data/outputs/audio data/outputs/images data/outputs/videos
mkdir -p data/knowledge_bases data/temp_docs data/cache
```

**1.2 安装依赖包**

```bash
pip install streamlit langchain langchain-openai langchain-community langchain-chroma
pip install dashscope chromadb
pip install python-dotenv httpx
pip install pandas openpyxl plotly
pip install pypdf docx2txt unstructured
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

**1.3 配置环境变量**

创建 `.env` 文件：

```env
DASHSCOPE_API_KEY="your_dashscope_api_key_here"
DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
EMBEDDING_MODEL="text-embedding-v3"
LLM_MODEL="qwen-plus"
CHROMA_DB_PATH="./data/knowledge_bases"
TEMP_DIR="./data/temp_docs"
```

创建 `.env.example` 模板文件，包含所有可配置项。

#### 步骤 2：搭建配置层

**2.1 实现 `config/settings.py`**

集中管理所有配置常量：

```python
import os
from dotenv import load_dotenv

load_dotenv()

# API 配置
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL")

# 模型列表
LLM_MODELS = ["qwen-plus", "qwen-max", "qwen-turbo"]
VISION_MODELS = ["qwen-vl-plus", "qwen-vl-max"]
T2I_MODELS = ["wanx2.1-t2i-turbo"]
I2V_MODELS = ["wanx2.1-i2v-turbo"]
TTS_MODELS = ["cosyvoice-v2"]
ASR_MODELS = ["paraformer-v2"]

# RAG 参数
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5

# 存储路径
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/knowledge_bases")
TEMP_DIR = os.getenv("TEMP_DIR", "./data/temp_docs")
```

**2.2 创建 `config/prompts.json`**

定义 5 个内置提示词模板：

```json
[
  {
    "name": "通用问答",
    "category": "general",
    "system_prompt": "你是一个有用的AI助手，请根据用户的问题提供准确、详细的回答。",
    "temperature": 0.7,
    "max_tokens": 2000
  },
  {
    "name": "专业专家",
    "category": "professional",
    "system_prompt": "你是一个专业领域的专家...",
    "temperature": 0.3,
    "max_tokens": 3000
  }
]
```

#### 步骤 3：搭建工具层

**3.1 实现 `utils/file_utils.py`**

提供文件处理基础工具：

```python
def download_image(url: str, save_path: str) -> str:
    """下载图片到指定路径"""
    pass

def encode_image_to_base64(image_path: str) -> str:
    """将图片编码为 Base64"""
    pass

def ensure_output_dir(sub_dir: str) -> str:
    """确保输出目录存在"""
    pass

def get_timestamp_filename(prefix: str, ext: str) -> str:
    """生成带时间戳的文件名"""
    pass

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    pass
```

**3.2 实现 `utils/ui_helpers.py`**

提供 Streamlit UI 工具：

```python
def apply_custom_css():
    """注入全局自定义 CSS 样式"""
    pass

def show_api_key_check():
    """检查 API Key 是否配置，未配置则跳转设置页"""
    pass

def render_card(title, content, icon):
    """渲染通用卡片组件"""
    pass

def render_feature_card(title, description, icon, page_link):
    """渲染功能导航卡片"""
    pass
```

---

### 3.2 第二阶段：核心服务模块开发

#### 步骤 4：实现 LLM 服务模块

**4.1 实现 `modules/llm_service.py`**

核心服务类，封装所有与大模型的交互：

```python
from langchain_openai import ChatOpenAI

class LLMService:
    def __init__(self):
        self.api_key = settings.DASHSCOPE_API_KEY
        self.base_url = settings.DASHSCOPE_BASE_URL

    def create_llm(self, model_name: str, temperature: float = 0.7):
        """创建文本 LLM 实例"""
        return ChatOpenAI(
            model=model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=temperature
        )

    def create_vl_llm(self, model_name: str):
        """创建视觉 LLM 实例"""
        return ChatOpenAI(model=model_name, api_key=self.api_key, base_url=self.base_url)

    def chat_stream(self, messages, model_name, temperature):
        """流式对话"""
        llm = self.create_llm(model_name, temperature)
        for chunk in llm.stream(messages):
            yield chunk.content

    def analyze_image_by_url(self, image_url, question, model_name):
        """通过 URL 分析图像"""
        pass

    def analyze_image_by_local(self, image_path, question, model_name):
        """通过本地文件分析图像（Base64 编码）"""
        pass

    def test_connection(self) -> bool:
        """测试 API 连接"""
        pass

@st.cache_resource
def get_llm_service():
    """获取缓存的 LLM 服务单例"""
    return LLMService()
```

**关键点**：
- 使用 LangChain `ChatOpenAI` 对接 DashScope 兼容接口
- 通过 `@st.cache_resource` 实现 Streamlit 缓存单例
- 流式输出使用 generator 模式

#### 步骤 5：实现文档处理模块

**5.1 实现 `modules/document_processor.py`**

```python
class DocumentProcessor:
    def load_document(self, file_path: str) -> list:
        """根据文件类型加载文档"""
        ext = os.path.splitext(file_path)[1].lower()
        loaders = {
            '.txt': TextLoader,
            '.pdf': PyPDFLoader,
            '.docx': Docx2txtLoader,
            '.csv': CSVLoader,
            '.md': UnstructuredMarkdownLoader,
        }
        # Excel 特殊处理
        if ext in ['.xlsx', '.xls']:
            return self._load_excel(file_path)
        loader = loaders[ext](file_path)
        return loader.load()

    def split_documents(self, documents, chunk_size=1000, chunk_overlap=200):
        """文档分块"""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " "]
        )
        return splitter.split_documents(documents)

    def process_uploaded_files(self, uploaded_files) -> list:
        """处理上传的文件列表"""
        pass
```

**关键点**：
- 支持 6 种文档格式
- 中文感知分隔符优先
- Excel 使用 Pandas 自定义加载

#### 步骤 6：实现向量库管理模块

**6.1 实现 `modules/vector_store.py`**

```python
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStoreManager:
    def __init__(self):
        self.embeddings = DashScopeEmbeddings(model=settings.EMBEDDING_MODEL)
        self.db_path = settings.CHROMA_DB_PATH

    def create_collection(self, name: str, description: str = ""):
        """创建新的向量集合"""
        pass

    def add_documents(self, collection_name: str, documents: list):
        """向集合中添加文档"""
        vectorstore = Chroma(
            collection_name=self._sanitize_name(collection_name),
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )
        vectorstore.add_documents(documents)

    def get_retriever(self, collection_name: str, top_k: int = 5):
        """获取检索器"""
        vectorstore = Chroma(
            collection_name=self._sanitize_name(collection_name),
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )
        return vectorstore.as_retriever(search_kwargs={"k": top_k})

    def list_collections(self) -> list:
        """列出所有集合"""
        pass

    def delete_collection(self, name: str):
        """删除集合"""
        pass
```

**关键点**：
- 使用 DashScope Embeddings 生成向量
- ChromaDB 持久化到本地磁盘
- 集合名需要处理中文字符（sanitize）

#### 步骤 7：实现 RAG 对话引擎

**7.1 实现 `modules/chat_engine.py`**

```python
class ChatEngine:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def stream_chat_with_rag(self, query, retriever, model_name, temperature, system_prompt):
        """RAG 流式对话"""
        # 1. 检索相关文档
        docs = retriever.invoke(query)

        # 2. 构建提示模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt + "\n\n参考文档：\n{context}"),
            ("human", "{question}")
        ])

        # 3. 构建 RAG 链
        chain = (
            {"context": lambda x: "\n\n".join([d.page_content for d in docs]),
             "question": RunnablePassthrough()}
            | prompt
            | self.llm_service.create_llm(model_name, temperature)
            | StrOutputParser()
        )

        # 4. 流式输出
        for chunk in chain.stream(query):
            yield chunk, docs  # 返回内容和来源文档
```

---

### 3.3 第三阶段：多模态服务模块开发

#### 步骤 8：实现图像生成服务

**8.1 实现 `modules/image_service.py`**

```python
import dashscope
from dashscope import ImageSynthesis

class ImageService:
    def __init__(self):
        dashscope.api_key = settings.DASHSCOPE_API_KEY

    def generate(self, prompt, model, size, n, style=None, negative_prompt=None):
        """同步生成图像"""
        # 拼接风格前缀
        if style:
            prompt = f"{style}风格，{prompt}"

        rsp = ImageSynthesis.call(
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            n=n,
            size=size
        )
        # 下载图像到本地
        images = []
        for result in rsp.output.results:
            path = download_image(result.url, ensure_output_dir("images"))
            images.append(path)
        return images
```

#### 步骤 9：实现视频生成服务

**9.1 实现 `modules/video_service.py`**

```python
from dashscope import VideoSynthesis

class VideoService:
    def generate(self, image_url, model, duration, prompt=None):
        """图生视频"""
        # 提交任务
        rsp = VideoSynthesis.async_call(
            model=model,
            image_url=image_url,
            prompt=prompt,
            duration=duration
        )
        # 轮询等待完成
        status = VideoSynthesis.wait(rsp.output.task_id)
        # 下载视频
        video_url = status.output.video_url
        return download_video(video_url, ensure_output_dir("videos"))
```

#### 步骤 10：实现音频服务

**10.1 实现 `modules/audio_service.py`**

```python
from dashscope import SpeechSynthesizer, Audio

class TTSService:
    def synthesize(self, text, voice, rate, volume, fmt):
        """文本转语音"""
        rsp = SpeechSynthesizer.call(
            model="cosyvoice-v2",
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            format=fmt
        )
        # 保存音频文件
        path = os.path.join(ensure_output_dir("audio"), get_timestamp_filename("tts", fmt))
        with open(path, "wb") as f:
            f.write(rsp.get_audio_data())
        return path

class ASRService:
    def transcribe(self, file_path, model):
        """语音转文本"""
        rsp = Audio.transcribe(
            model=model,
            file=file_path
        )
        return extract_asr_text(rsp)
```

---

### 3.4 第四阶段：管理模块开发

#### 步骤 11：实现模型配置管理

**11.1 实现 `modules/model_config.py`**

```python
class ModelConfigManager:
    def __init__(self):
        self.config_path = "data/model_config.json"
        self.presets_path = "data/presets.json"

    def get_config(self) -> dict:
        """获取当前模型配置"""
        pass

    def update_config(self, key: str, value):
        """更新配置项"""
        pass

    def reset_config(self):
        """重置为默认配置"""
        pass

    def save_preset(self, name: str, config: dict):
        """保存为预设"""
        pass

    def load_preset(self, name: str):
        """加载预设"""
        pass
```

#### 步骤 12：实现提示词管理

**12.1 实现 `modules/prompt_manager.py`**

```python
class PromptManager:
    def __init__(self):
        self.default_prompts = self._load_defaults()
        self.custom_prompts = self._load_custom()

    def get_all_prompts(self, category=None) -> list:
        """获取所有提示词（默认 + 自定义）"""
        pass

    def add_custom_prompt(self, name, system_prompt, temperature, max_tokens):
        """添加自定义提示词"""
        pass

    def delete_custom_prompt(self, name):
        """删除自定义提示词"""
        pass
```

---

### 3.5 第五阶段：页面开发

#### 步骤 13：实现主页

**13.1 实现 `app.py`（Streamlit 主入口）**

```python
import streamlit as st

st.set_page_config(page_title="多模态AI智能助手", layout="wide")
apply_custom_css()

# Hero Banner
st.title("多模态 AI 智能助手")

# 功能导航卡片（3 列布局）
col1, col2, col3 = st.columns(3)
with col1:
    render_feature_card("RAG 文档问答", "基于知识库的智能问答", "📚", "pages/02_RAG文档问答.py")
    # ... 更多卡片
```

**13.2 实现 `start.py`（CLI 启动脚本）**

```python
def main():
    # 1. 检查 Python 版本
    # 2. 检查 .env 文件和 API Key
    # 3. 检查并安装依赖
    # 4. 确保目录结构
    # 5. 启动 Streamlit
    os.system("streamlit run app.py --server.port 8501")
```

#### 步骤 14：实现 RAG 文档问答页面

**14.1 实现 `pages/02_RAG文档问答.py`**

侧边栏配置：
- 模式选择（临时文档 / 知识库）
- 文档上传（多文件）
- 知识库选择（下拉框）
- 提示词模板选择
- Temperature 滑块
- Top-K 滑块

主内容区：
- 聊天历史展示（`st.chat_message`）
- 用户输入框（`st.chat_input`）
- 流式输出回答
- 可展开的来源引用

```python
# 核心对话逻辑
if user_input:
    if mode == "临时文档":
        # 处理上传文档 → 创建临时向量库 → 检索问答
        docs = document_processor.process_uploaded_files(uploaded_files)
        vectorstore.add_documents("temp", docs)
        retriever = vectorstore.get_retriever("temp", top_k)
    else:
        # 使用持久化知识库
        retriever = vectorstore.get_retriever(selected_kb, top_k)

    # 流式输出
    for chunk, sources in chat_engine.stream_chat_with_rag(
        user_input, retriever, model, temperature, system_prompt
    ):
        st.write(chunk)
```

#### 步骤 15：实现文生图页面

**15.1 实现 `pages/03_文生图.py`**

侧边栏：
- 模型选择
- 图片尺寸（1:1, 9:16, 16:9）
- 批量数量（1/2/4）
- 风格预设（写实、动漫、油画、3D、水墨、赛博朋克）

主内容区：
- 正面提示词输入
- 负面提示词输入
- 生成按钮
- 图像展示网格
- 下载按钮
- 生成历史

#### 步骤 16：实现图片解读页面

**16.1 实现 `pages/04_图片解读.py`**

两种输入模式：
- **URL 模式**：输入图片 URL
- **本地上传模式**：上传图片文件（自动 Base64 编码）

侧边栏：
- 视觉模型选择
- 问题模板（详细描述、构图分析、OCR 提取、情感分析、自定义）

#### 步骤 17：实现图生视频页面

**17.1 实现 `pages/05_图生视频.py`**

- 上传源图片或输入 URL
- 侧边栏：视频模型、时长、运动模板
- 进度条展示生成状态
- 视频预览和下载

#### 步骤 18：实现音频相关页面

**18.1 实现 `pages/06_文生音频.py`**

侧边栏：TTS 模型、音色选择（6 种）、语速（0.5x-2x）、音量、输出格式（MP3/WAV）、文本模板

主内容区：文本输入、生成按钮、音频播放器、下载按钮、生成历史

**18.2 实现 `pages/07_音频生文.py`**

两种输入：文件上传 / 音频 URL
侧边栏：ASR 模型、识别模式（短音频同步 / 长音频异步）
结果展示：识别文本、时间戳详情、导出选项

#### 步骤 19：实现 Excel 助手页面

**19.1 实现 `pages/09_Excel助手.py`**

```python
# 上传 CSV/XLSX
uploaded_file = st.file_uploader("上传文件", type=["csv", "xlsx"])

# 数据概览
st.metric("总行数", df.shape[0])
st.metric("总列数", df.shape[1])

# 数据筛选
columns = st.multiselect("选择列", df.columns.tolist())
sort_by = st.selectbox("排序列", df.columns.tolist())

# Plotly 图表
chart_type = st.selectbox("图表类型", ["折线图", "柱状图", "饼图", "散点图", "面积图"])
fig = create_plotly_chart(df, chart_type, x_col, y_col)
st.plotly_chart(fig)

# 统计分析
st.dataframe(df.describe())
st.plotly_chart(create_correlation_heatmap(df))
```

#### 步骤 20：实现知识库管理页面

**20.1 实现 `pages/10_知识库管理.py`**

两个标签页：
- **知识库列表**：卡片网格展示所有集合，每个卡片有上传/删除操作
- **创建新知识库**：表单（名称、描述、上传文件）

上传流程：选择文件 → `DocumentProcessor` 处理 → `VectorStoreManager` 入库

#### 步骤 21：实现系统设置页面

**21.1 实现 `pages/08_系统设置.py`**

四个标签页：
- **API 配置**：查看/编辑/测试 DashScope API Key 和 Base URL（写回 `.env`）
- **模型设置**：配置各模态默认模型、RAG 参数，支持保存/重置
- **提示词管理**：浏览、筛选、添加、删除自定义提示词模板
- **数据管理**：查看存储统计（集合数、文档数、磁盘占用）、清理临时文件、清空知识库

---

### 3.6 第六阶段：测试与调试

#### 步骤 22：单元功能测试

逐一测试各模块核心功能：

```bash
# 测试 LLM 服务
python -c "from modules.llm_service import get_llm_service; s = get_llm_service(); print(s.test_connection())"

# 测试文档处理
python -c "from modules.document_processor import DocumentProcessor; dp = DocumentProcessor(); print(dp.load_document('test.pdf'))"

# 测试向量库
python -c "from modules.vector_store import VectorStoreManager; vm = VectorStoreManager(); print(vm.list_collections())"
```

#### 步骤 23：集成测试

启动完整系统并测试各页面功能：

```bash
python start.py
# 或直接
streamlit run app.py
```

测试用例：

| 页面 | 测试内容 |
|------|---------|
| RAG 文档问答 | 上传 PDF → 提问 → 验证回答包含文档内容 |
| 文生图 | 输入提示词 → 选择风格 → 验证图像生成 |
| 图片解读 | 上传图片 → 选择模板 → 验证分析结果 |
| 图生视频 | 上传图片 → 生成视频 → 验证视频播放 |
| 文生音频 | 输入文本 → 选择音色 → 验证音频播放 |
| 音频生文 | 上传音频 → 验证转录文本 |
| Excel 助手 | 上传 CSV → 验证图表生成 |
| 知识库管理 | 创建知识库 → 上传文档 → 验证 RAG 可用 |
| 系统设置 | 修改 API Key → 测试连接 → 验证配置持久化 |

#### 步骤 24：启动完整系统

```bash
# 方式一：使用启动脚本（推荐，自动检查环境）
python start.py

# 方式二：直接启动 Streamlit
streamlit run app.py --server.port 8501

# 访问地址
# http://localhost:8501
```

---

## 四、配置说明

### 4.1 环境变量配置

`.env` 文件配置项：

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `DASHSCOPE_API_KEY` | DashScope API 密钥 | `sk-xxxxxxxx` |
| `DASHSCOPE_BASE_URL` | API 兼容端点 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `EMBEDDING_MODEL` | 嵌入模型名称 | `text-embedding-v3` |
| `LLM_MODEL` | 默认 LLM 模型 | `qwen-plus` |
| `CHROMA_DB_PATH` | ChromaDB 存储路径 | `./data/knowledge_bases` |
| `TEMP_DIR` | 临时文件目录 | `./data/temp_docs` |

### 4.2 模型配置

系统支持通过 `data/model_config.json` 持久化用户偏好：

```json
{
  "llm_model": "qwen-plus",
  "vision_model": "qwen-vl-plus",
  "t2i_model": "wanx2.1-t2i-turbo",
  "i2v_model": "wanx2.1-i2v-turbo",
  "tts_model": "cosyvoice-v2",
  "asr_model": "paraformer-v2",
  "temperature": 0.7,
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "top_k": 5
}
```

### 4.3 提示词模板配置

`config/prompts.json` 定义内置模板，用户可通过系统设置页添加自定义模板，存储在 `data/knowledge_bases/custom_prompts.json`。

---

## 五、模块依赖关系

```
pages/*.py
    │
    ├── config/settings.py          （配置常量）
    ├── utils/ui_helpers.py         （UI 工具）
    │
    ├── modules/llm_service.py      （LLM/视觉服务）
    │       └── config/settings.py
    │
    ├── modules/chat_engine.py      （RAG 引擎）
    │       ├── modules/llm_service.py
    │       └── modules/vector_store.py
    │
    ├── modules/document_processor.py（文档处理）
    │
    ├── modules/vector_store.py     （向量库管理）
    │       └── config/settings.py
    │
    ├── modules/image_service.py    （图像生成）
    │       ├── config/settings.py
    │       └── utils/file_utils.py
    │
    ├── modules/video_service.py    （视频生成）
    │       ├── config/settings.py
    │       └── utils/file_utils.py
    │
    ├── modules/audio_service.py    （音频服务）
    │       ├── config/settings.py
    │       └── utils/file_utils.py
    │
    ├── modules/model_config.py     （模型配置）
    │
    └── modules/prompt_manager.py   （提示词管理）
```

---

## 六、总结

本项目通过 Streamlit + LangChain + DashScope 技术栈，构建了一个功能完整的多模态 AI 智能助手平台。

**核心要点**：
1. **模块化架构**：配置层、服务层、工具层、页面层四层分离，职责清晰
2. **多模态能力**：覆盖文本、图像、视频、音频四大模态的生成与理解
3. **RAG 知识库**：基于 ChromaDB 的持久化向量知识库，支持文档上传、分块、嵌入、检索全流程
4. **可配置性**：模型、提示词、RAG 参数均可通过界面配置，无需修改代码
5. **异步处理**：图像/视频生成采用异步任务 + 轮询机制，避免阻塞

**开发顺序建议**：
1. 先搭建配置层和工具层（基础依赖）
2. 再实现核心服务模块（LLM → 文档处理 → 向量库 → RAG 引擎）
3. 然后开发多模态服务（图像 → 视频 → 音频）
4. 接着实现管理模块（模型配置 → 提示词管理）
5. 最后开发页面层（从主页开始，逐个实现功能页面）
6. 全程穿插测试，每完成一个模块立即验证
