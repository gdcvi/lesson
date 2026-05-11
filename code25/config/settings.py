"""全局配置管理"""
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== API 配置 ====================
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

# ==================== LLM/Vision 模型 (ChatOpenAI) ====================
LLM_MODELS = ["qwen-plus", "qwen-max", "qwen-turbo"]
VISION_MODELS = ["qwen-vl-plus", "qwen-vl-max"]

# ==================== 生成类模型 (DashScope SDK) ====================
T2I_MODELS = ["wan2.2-t2i-flash"]
I2V_MODELS = ["wanx2.1-i2v-turbo", "wanx2.1-i2v-plus"]
TTS_MODELS = ["cosyvoice-v2"]
ASR_MODELS = ["paraformer-v2"]

# ==================== TTS 音色 ====================
TTS_VOICES = {
    "longxiaochun_v2": "龙小春（女声，温柔知性）",
    "longxiaoxia_v2": "龙小夏（女声，活泼可爱）",
    "longxiaobai_v2": "龙小白（男声，阳光亲切）",
    "longlaotie_v2": "龙老铁（男声，东北口音）",
    "longcheng_v2": "龙城（男声，沉稳大气）",
    "longyue_v2": "龙悦（女声，甜美温柔）",
}

# ==================== 图片尺寸 ====================
IMAGE_SIZES = {
    "1024*1024": "方形 (1:1)",
    "720*1280": "竖屏 (9:16)",
    "1280*720": "横屏 (16:9)",
    "1024*576": "宽屏 (16:9 小)",
}

# ==================== RAG 配置 ====================
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_TOP_K = 5
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048

# ==================== 数据库/存储配置 ====================
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_bases")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "temp_docs")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "outputs")

# ==================== 文件上传限制 ====================
MAX_FILE_SIZE_IMAGE = 10 * 1024 * 1024       # 10MB
MAX_FILE_SIZE_AUDIO = 100 * 1024 * 1024      # 100MB
MAX_FILE_SIZE_DOC = 10 * 1024 * 1024         # 10MB
ALLOWED_DOC_EXTENSIONS = {'.txt', '.pdf', '.docx', '.md', '.csv', '.xlsx'}
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
ALLOWED_AUDIO_EXTENSIONS = {'.wav', '.mp3', '.flac', '.m4a', '.ogg'}

# ==================== Streamlit 配置 ====================
PAGE_TITLE = "多模态AI智能助手"
PAGE_ICON = "🤖"

# ==================== 配色方案 ====================
COLORS = {
    "primary": "#1E88E5",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336",
    "bg_light": "#F5F7FA",
    "card_border": "#E0E0E0",
}
