"""文件工具函数 —— 从 code24 提取复用"""
import os
import time
import base64
import requests


def download_image(url: str, save_path: str) -> bool:
    """从URL下载图片并保存到本地"""
    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"下载图片失败: {e}")
        return False


def download_video(url: str, save_path: str) -> bool:
    """从URL下载视频并保存到本地"""
    try:
        resp = requests.get(url, timeout=300)
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"下载视频失败: {e}")
        return False


def encode_image_to_base64(image_path: str) -> str:
    """将本地图片文件编码为 base64 字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_asr_text(result) -> str:
    """从 Transcription 响应中提取识别文字，兼容多种返回格式"""
    output = result.output
    results = output.get("results") if isinstance(output, dict) else getattr(output, "results", None)
    if not results:
        return None

    first_result = results[0]
    if isinstance(first_result, dict):
        if "transcription" in first_result or "text" in first_result:
            return first_result.get("transcription") or first_result.get("text", "")

        transcription_url = first_result.get("transcription_url")
        if transcription_url:
            try:
                resp = requests.get(transcription_url, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                if "transcripts" in data:
                    return data["transcripts"][0]["text"]
                elif "text" in data:
                    return data["text"]
                else:
                    return str(data)
            except Exception as e:
                print(f"下载识别结果失败: {e}")
                return None
        return None
    else:
        return getattr(first_result, "transcription", "") or getattr(first_result, "text", "")


def get_asr_detail(result) -> dict:
    """从 ASR 响应中下载并解析详细的识别结果（含句子/词级时间戳）"""
    output = result.output
    results = output.get("results") if isinstance(output, dict) else getattr(output, "results", None)
    if not results:
        return {}

    first_result = results[0]
    if isinstance(first_result, dict):
        transcription_url = first_result.get("transcription_url")
        if transcription_url:
            try:
                resp = requests.get(transcription_url, timeout=30)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                print(f"下载详细结果失败: {e}")
    return {}


def ensure_output_dir(category: str = "images") -> str:
    """确保输出目录存在，返回带时间戳的子目录路径"""
    from config.settings import OUTPUT_DIR

    sub_dir = os.path.join(OUTPUT_DIR, category)
    os.makedirs(sub_dir, exist_ok=True)
    return sub_dir


def get_timestamp_filename(prefix: str, ext: str) -> str:
    """生成带时间戳的文件名"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{ext}"


def get_mime_type(file_path: str) -> str:
    """根据文件扩展名确定MIME类型"""
    ext = os.path.splitext(file_path)[1].lower()
    mime_map = {".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp", ".gif": "gif"}
    return mime_map.get(ext, "jpeg")


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
