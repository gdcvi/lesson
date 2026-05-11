"""
 * @author: zkyuan
 * @date: 2026/5/11
 * @description: 音频转文字模型(STT/ASR) —— 将语音文件识别转换为文字
 * 使用 DashScope Transcription API，调用 paraformer-v2 语音识别模型
"""
import os
import time
import dashscope
from dashscope.audio.asr import Transcription
from dotenv import load_dotenv

load_dotenv()

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# 示例音频文件URL（DashScope官方提供的测试音频）
SAMPLE_AUDIO_URLS = {
    "chinese_01": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    "chinese_02": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male.wav",
}


def _extract_text(result) -> str:
    """从 Transcription 响应中提取识别文字"""
    import requests

    output = result.output
    results = output.get("results") if isinstance(output, dict) else getattr(output, "results", None)
    if not results:
        return None

    first_result = results[0]
    if isinstance(first_result, dict):
        # 直接包含识别文本
        if "transcription" in first_result or "text" in first_result:
            return first_result.get("transcription") or first_result.get("text", "")

        # 需要从 transcription_url 下载 JSON 文件获取文本
        transcription_url = first_result.get("transcription_url")
        if transcription_url:
            try:
                resp = requests.get(transcription_url, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                # 从 JSON 中提取完整文本
                if "transcripts" in data:
                    # paraformer 格式
                    return data["transcripts"][0]["text"]
                elif "text" in data:
                    return data["text"]
                else:
                    return str(data)
            except Exception as e:
                print(f"  下载识别结果失败: {e}")
                return None

        return None
    else:
        return getattr(first_result, "transcription", "") or getattr(first_result, "text", "")


def audio_to_text_sync(audio_url: str, model: str = "paraformer-v2") -> str:
    """同步方式：音频转文字（适合短音频）"""
    print(f"\n模型: {model}")
    print(f"音频URL: {audio_url[:80]}...")
    print("正在识别（同步模式）...")

    result = Transcription.call(
        model=model,
        file_urls=[audio_url],
    )

    if result.status_code == 200:
        text = _extract_text(result)
        if text:
            print(f"识别结果: {text}")
        else:
            print(f"未能提取识别文本，output: {dict(result.output) if hasattr(result.output, 'items') else result.output}")
        return text
    else:
        print(f"识别失败: status_code={result.status_code}")
        print(f"错误信息: {result.message}")
        return None


def audio_to_text_async(audio_url: str, model: str = "paraformer-v2") -> str:
    """异步方式：音频转文字（适合长音频，提交任务后轮询结果）"""
    print(f"\n模型: {model}")
    print(f"音频URL: {audio_url[:80]}...")
    print("正在提交异步识别任务...")

    task = Transcription.async_call(
        model=model,
        file_urls=[audio_url],
    )

    task_id = task.output.task_id if hasattr(task.output, 'task_id') else task.output.get("task_id")
    print(f"任务已提交, task_id: {task_id}")
    print("等待任务完成", end="", flush=True)

    result = Transcription.wait(task_id)

    if result.status_code == 200:
        text = _extract_text(result)
        if text:
            print(f"\n识别结果: {text}")
        return text
    else:
        print(f"\n识别失败: status_code={result.status_code}")
        print(f"错误信息: {result.message}")
        return None


def demo_sync_stt():
    """示例1：同步语音识别"""
    print("\n" + "=" * 50)
    print("【示例1】同步语音识别 —— 短音频")
    print("=" * 50)

    audio_to_text_sync(SAMPLE_AUDIO_URLS["chinese_01"])


def demo_async_stt():
    """示例2：异步语音识别"""
    print("\n" + "=" * 50)
    print("【示例2】异步语音识别 —— 长音频")
    print("=" * 50)

    audio_to_text_async(SAMPLE_AUDIO_URLS["chinese_02"])


def demo_multi_audio():
    """示例3：批量语音识别"""
    print("\n" + "=" * 50)
    print("【示例3】批量语音识别")
    print("=" * 50)

    for name, url in SAMPLE_AUDIO_URLS.items():
        print(f"\n--- 识别 {name} ---")
        audio_to_text_sync(url)
        time.sleep(0.3)


def demo_format_info():
    """示例4：获取识别结果详情"""
    import requests

    print("\n" + "=" * 50)
    print("【示例4】语音识别 —— 结果详情")
    print("=" * 50)

    result = Transcription.call(
        model="paraformer-v2",
        file_urls=[SAMPLE_AUDIO_URLS["chinese_01"]],
    )

    if result.status_code == 200:
        print(f"请求ID: {result.request_id}")

        # 获取完整识别文本
        text = _extract_text(result)
        print(f"识别文本: {text}")

        # 下载 transcription JSON 获取更详细的信息
        output_dict = dict(result.output) if hasattr(result.output, 'items') else result.output
        results = output_dict.get("results", [])
        if results:
            first = results[0]
            transcription_url = first.get("transcription_url")
            if transcription_url:
                try:
                    resp = requests.get(transcription_url, timeout=30)
                    resp.raise_for_status()
                    detail = resp.json()

                    # 句子级别信息
                    sentences = detail.get("sentences", [])
                    if sentences:
                        print("\n句子级别信息:")
                        for sent in sentences:
                            begin = sent.get("begin_time", "?")
                            end = sent.get("end_time", "?")
                            txt = sent.get("text", "")
                            print(f"  [{begin}ms - {end}ms] {txt}")

                    # 词级别时间戳
                    words = detail.get("words", [])
                    if words:
                        print(f"\n词级别信息 (前10个):")
                        for w in words[:10]:
                            begin = w.get("begin_time", "?")
                            end = w.get("end_time", "?")
                            txt = w.get("text", "")
                            print(f"  [{begin}ms - {end}ms] {txt}")

                except Exception as e:
                    print(f"下载详细结果失败: {e}")


if __name__ == "__main__":
    demo_sync_stt()
    demo_async_stt()
    demo_multi_audio()
    demo_format_info()

    print("\n" + "=" * 50)
    print("所有音频转文字示例演示完毕")
    print("=" * 50)

# 测试运行结果

"""
D:\Anaconda\envs\lesson\python.exe E:\code\GitWork\gdcvi\lesson\code24\6_audio2text.py 

==================================================
【示例1】同步语音识别 —— 短音频
==================================================

模型: paraformer-v2
音频URL: https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_wor...
正在识别（同步模式）...
识别结果: Hello word, 这里是阿里巴巴语音实验室。

==================================================
【示例2】异步语音识别 —— 长音频
==================================================

模型: paraformer-v2
音频URL: https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_wor...
正在提交异步识别任务...
任务已提交, task_id: 06b45e7d-670b-4344-b3d6-d0bf3fa9f8ba
等待任务完成
识别结果: Hello world, 来自阿里巴巴达摩院语音实验室。

==================================================
【示例3】批量语音识别
==================================================

--- 识别 chinese_01 ---

模型: paraformer-v2
音频URL: https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_wor...
正在识别（同步模式）...
识别结果: Hello word, 这里是阿里巴巴语音实验室。

--- 识别 chinese_02 ---

模型: paraformer-v2
音频URL: https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_wor...
正在识别（同步模式）...
识别结果: Hello world, 来自阿里巴巴达摩院语音实验室。

==================================================
【示例4】语音识别 —— 结果详情
==================================================
请求ID: bf2ec07f-2721-9625-acdd-365cf2bb3b09
识别文本: Hello word, 这里是阿里巴巴语音实验室。

==================================================
所有音频转文字示例演示完毕
==================================================

Process finished with exit code 0

"""