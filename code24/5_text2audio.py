"""
 * @author: zkyuan
 * @date: 2026/5/11
 * @description: 文生音频模型(TTS) —— 将文字转换为自然流畅的语音
 * 使用 DashScope SpeechSynthesizer API，调用 cosyvoice-v2 语音合成模型
 * 支持多种音色、语速、音量调节
"""
import os
import time
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
from dotenv import load_dotenv

load_dotenv()

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 常用音色列表
VOICES = {
    "longxiaochun_v2": "龙小春（女声，温柔知性）",
    "longxiaoxia_v2": "龙小夏（女声，活泼可爱）",
    "longxiaobai_v2": "龙小白（男声，阳光亲切）",
    "longlaotie_v2": "龙老铁（男声，东北口音）",
    "longcheng_v2": "龙城（男声，沉稳大气）",
    "longyue_v2": "龙悦（女声，甜美温柔）",
}


def text_to_audio(
    text: str,
    voice: str = "longxiaochun_v2",
    model: str = "cosyvoice-v2",
    speech_rate: float = 1.0,
    volume: int = 50,
    audio_format: AudioFormat = AudioFormat.MP3_24000HZ_MONO_256KBPS,
) -> str:
    """
    文本转语音
    :param text: 要合成的文本
    :param voice: 音色名称
    :param model: TTS模型
    :param speech_rate: 语速 (0.5~2.0)
    :param volume: 音量 (0~100)
    :param audio_format: 输出音频格式
    :return: 保存的音频文件路径
    """
    print(f"\n模型: {model}")
    print(f"音色: {voice} ({VOICES.get(voice, '未知')})")
    print(f"语速: {speech_rate}x | 音量: {volume}")
    print(f"文本: {text[:50]}{'...' if len(text) > 50 else ''}")

    # 创建语音合成器实例
    synthesizer = SpeechSynthesizer(
        model=model,
        voice=voice,
        format=audio_format,
        volume=volume,
        speech_rate=speech_rate,
    )

    print("正在合成语音...")
    audio_data = synthesizer.call(text)

    if audio_data:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        ext = "mp3" if "MP3" in str(audio_format) else "wav"
        save_path = os.path.join(OUTPUT_DIR, f"tts_{voice}_{timestamp}.{ext}")
        with open(save_path, "wb") as f:
            f.write(audio_data)
        file_size = os.path.getsize(save_path) / 1024
        print(f"语音合成成功! 文件: {save_path} ({file_size:.1f}KB)")
        return save_path
    else:
        print("语音合成失败: 未获取到音频数据")
        # 尝试获取错误信息
        resp = synthesizer.get_response()
        if resp:
            print(f"响应信息: {resp}")
        return None


def demo_basic_tts():
    """示例1：基础文本转语音"""
    print("\n" + "=" * 50)
    print("【示例1】基础文字转语音")
    print("=" * 50)

    text_to_audio(
        text="你好，欢迎学习大模型多模态应用实践课程。今天我们将学习如何使用通义千问大模型实现各种有趣的功能。",
        voice="longxiaochun_v2",
    )


def demo_multi_voice():
    """示例2：多音色对比 —— 同一段文字用不同音色朗读"""
    print("\n" + "=" * 50)
    print("【示例2】多音色对比")
    print("=" * 50)

    text = "今天天气真好，适合出去散步。"
    voices_to_try = ["longxiaochun_v2", "longxiaobai_v2", "longlaotie_v2"]

    for v in voices_to_try[:2]:  # 控制数量避免过长
        text_to_audio(text=text, voice=v)
        time.sleep(0.5)


def demo_speed_volume():
    """示例3：语速和音量调节"""
    print("\n" + "=" * 50)
    print("【示例3】语速和音量调节")
    print("=" * 50)

    # 快速朗读
    text_to_audio(
        text="快速朗读模式，适合用于需要快速获取信息的播客场景。",
        voice="longxiaochun_v2",
        speech_rate=1.5,
    )

    time.sleep(0.5)

    # 慢速朗读
    text_to_audio(
        text="慢速朗读模式，适合用于学习语言或者听写练习的场景。",
        voice="longxiaochun_v2",
        speech_rate=0.8,
    )


def demo_long_text():
    """示例4：长文本朗读 —— 适合文章播报"""
    print("\n" + "=" * 50)
    print("【示例4】长文本朗读")
    print("=" * 50)

    long_text = (
        "人工智能技术正在深刻地改变着我们的世界。"
        "从智能手机上的语音助手，到自动驾驶汽车，从医疗影像诊断，到金融风险预测，"
        "人工智能已经渗透到了生活的方方面面。"
        "大语言模型的出现，更是让人工智能具备了理解和生成自然语言的能力，"
        "开启了人机交互的新纪元。"
    )

    text_to_audio(text=long_text, voice="longxiaobai_v2")


if __name__ == "__main__":
    demo_basic_tts()
    demo_multi_voice()
    demo_speed_volume()
    demo_long_text()

    print("\n" + "=" * 50)
    print("所有文生音频示例演示完毕，音频文件保存在 output/ 目录")
    print("=" * 50)

# 测试运行结果
"""
D:\Anaconda\envs\lesson\python.exe E:\code\GitWork\gdcvi\lesson\code24\5_text2audio.py 

==================================================
【示例1】基础文字转语音
==================================================

模型: cosyvoice-v2
音色: longxiaochun_v2 (龙小春（女声，温柔知性）)
语速: 1.0x | 音量: 50
文本: 你好，欢迎学习大模型多模态应用实践课程。今天我们将学习如何使用通义千问大模型实现各种有趣的功能。
正在合成语音...
语音合成成功! 文件: E:\code\GitWork\gdcvi\lesson\code24\output\tts_longxiaochun_v2_20260511_152027.mp3 (178.7KB)

==================================================
【示例2】多音色对比
==================================================

模型: cosyvoice-v2
音色: longxiaochun_v2 (龙小春（女声，温柔知性）)
语速: 1.0x | 音量: 50
文本: 今天天气真好，适合出去散步。
正在合成语音...
语音合成成功! 文件: E:\code\GitWork\gdcvi\lesson\code24\output\tts_longxiaochun_v2_20260511_152028.mp3 (50.7KB)

模型: cosyvoice-v2
音色: longxiaobai_v2 (龙小白（男声，阳光亲切）)
语速: 1.0x | 音量: 50
文本: 今天天气真好，适合出去散步。
正在合成语音...
语音合成成功! 文件: E:\code\GitWork\gdcvi\lesson\code24\output\tts_longxiaobai_v2_20260511_152031.mp3 (68.5KB)

==================================================
【示例3】语速和音量调节
==================================================

模型: cosyvoice-v2
音色: longxiaochun_v2 (龙小春（女声，温柔知性）)
语速: 1.5x | 音量: 50
文本: 快速朗读模式，适合用于需要快速获取信息的播客场景。
正在合成语音...
语音合成成功! 文件: E:\code\GitWork\gdcvi\lesson\code24\output\tts_longxiaochun_v2_20260511_152034.mp3 (61.5KB)

模型: cosyvoice-v2
音色: longxiaochun_v2 (龙小春（女声，温柔知性）)
语速: 0.8x | 音量: 50
文本: 慢速朗读模式，适合用于学习语言或者听写练习的场景。
正在合成语音...
语音合成成功! 文件: E:\code\GitWork\gdcvi\lesson\code24\output\tts_longxiaochun_v2_20260511_152037.mp3 (112.6KB)

==================================================
【示例4】长文本朗读
==================================================

模型: cosyvoice-v2
音色: longxiaobai_v2 (龙小白（男声，阳光亲切）)
语速: 1.0x | 音量: 50
文本: 人工智能技术正在深刻地改变着我们的世界。从智能手机上的语音助手，到自动驾驶汽车，从医疗影像诊断，到金...
正在合成语音...
语音合成成功! 文件: E:\code\GitWork\gdcvi\lesson\code24\output\tts_longxiaobai_v2_20260511_152050.mp3 (535.4KB)

==================================================
所有文生音频示例演示完毕，音频文件保存在 output/ 目录
==================================================

Process finished with exit code 0

"""