"""音频服务模块 —— 封装 DashScope SpeechSynthesizer (TTS) + Transcription (ASR)"""
import os
import time
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
from dashscope.audio.asr import Transcription
from config.settings import DASHSCOPE_API_KEY
from utils.file_utils import extract_asr_text, get_asr_detail, ensure_output_dir, get_timestamp_filename


class TTSService:
    """文生音频（TTS）服务类"""

    def __init__(self):
        dashscope.api_key = DASHSCOPE_API_KEY

    def synthesize(self, text: str, voice: str = "longxiaochun_v2",
                   model: str = "cosyvoice-v2", speech_rate: float = 1.0,
                   volume: int = 50, audio_format=None) -> str:
        """
        文本转语音
        :return: 保存的音频文件路径
        """
        if audio_format is None:
            audio_format = AudioFormat.MP3_24000HZ_MONO_256KBPS

        synthesizer = SpeechSynthesizer(
            model=model,
            voice=voice,
            format=audio_format,
            volume=volume,
            speech_rate=speech_rate,
        )
        audio_data = synthesizer.call(text)

        if not audio_data:
            resp = synthesizer.get_response()
            raise Exception(f"语音合成失败: 未获取到音频数据, 响应={resp}")

        output_dir = ensure_output_dir("audio")
        ext = "mp3" if "MP3" in str(audio_format) else "wav"
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(output_dir, f"tts_{voice}_{timestamp}.{ext}")

        with open(save_path, "wb") as f:
            f.write(audio_data)

        return save_path


class ASRService:
    """音频转文字（ASR）服务类"""

    def __init__(self):
        dashscope.api_key = DASHSCOPE_API_KEY

    def transcribe_sync(self, audio_url: str, model: str = "paraformer-v2") -> str:
        """同步语音识别（适合短音频）"""
        result = Transcription.call(model=model, file_urls=[audio_url])

        if result.status_code != 200:
            raise Exception(f"语音识别失败: status_code={result.status_code}, message={result.message}")

        text = extract_asr_text(result)
        if not text:
            raise Exception("未能从识别结果中提取文本")
        return text

    def transcribe_async(self, audio_url: str, model: str = "paraformer-v2") -> str:
        """异步语音识别（适合长音频，含轮询）"""
        task = Transcription.async_call(model=model, file_urls=[audio_url])

        task_id = task.output.task_id if hasattr(task.output, 'task_id') else task.output.get("task_id")
        result = Transcription.wait(task_id)

        if result.status_code != 200:
            raise Exception(f"异步识别失败: status_code={result.status_code}, message={result.message}")

        text = extract_asr_text(result)
        if not text:
            raise Exception("未能从识别结果中提取文本")
        return text

    def transcribe_with_detail(self, audio_url: str, model: str = "paraformer-v2") -> dict:
        """语音识别并返回详细结果（含句子/词级时间戳）"""
        result = Transcription.call(model=model, file_urls=[audio_url])

        if result.status_code != 200:
            raise Exception(f"语音识别失败: status_code={result.status_code}, message={result.message}")

        text = extract_asr_text(result)
        detail = get_asr_detail(result)

        return {
            "text": text,
            "sentences": detail.get("sentences", []),
            "words": detail.get("words", []),
        }
