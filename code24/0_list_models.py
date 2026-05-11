"""
 * @author: zkyuan
 * @date: 2026/5/11
 * @description: 获取千问(通义千问)API的所有可用大模型列表
 * 使用 LangChain 的 ChatOpenAI 连接 DashScope，通过底层 client 获取模型列表
"""
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 创建 LangChain ChatOpenAI 实例，指向 DashScope
llm = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def list_all_models():
    """获取并展示所有可用模型"""
    print("=" * 60)
    print("通义千问 DashScope 可用模型列表")
    print("=" * 60)

    try:
        # 通过 ChatOpenAI 的底层 OpenAI client 获取模型列表
        # ChatOpenAI.client 是 Completions 对象，root_client 才是完整的 OpenAI 客户端
        models = llm.root_client.models.list()
        model_list = list(models)

        # 按类别分组
        categories = {
            "大语言模型 (LLM)": [],
            "视觉理解模型 (Vision)": [],
            "语音模型 (Audio)": [],
            "其他模型": [],
        }

        for m in model_list:
            mid = m.id.lower()
            if "vl" in mid or "vision" in mid:
                categories["视觉理解模型 (Vision)"].append(m.id)
            elif any(x in mid for x in ("tts", "cosyvoice", "speech", "asr", "paraformer", "audio")):
                categories["语音模型 (Audio)"].append(m.id)
            elif any(x in mid for x in ("qwen", "baichuan", "llama", "deepseek")):
                categories["大语言模型 (LLM)"].append(m.id)
            else:
                categories["其他模型"].append(m.id)

        for cat, models_in_cat in categories.items():
            if models_in_cat:
                print(f"\n【{cat}】({len(models_in_cat)}个)")
                print("-" * 40)
                for name in sorted(models_in_cat):
                    print(f"  - {name}")

        print(f"\n总计: {len(model_list)} 个模型")
        print("=" * 60)

    except Exception as e:
        print(f"获取模型列表失败: {e}")
        print("请检查 DASHSCOPE_API_KEY 是否正确配置")


if __name__ == "__main__":
    list_all_models()


# 测试运行结果
"""
D:\Anaconda\envs\lesson\python.exe E:\code\GitWork\gdcvi\lesson\code24\0_list_models.py 
============================================================
通义千问 DashScope 可用模型列表
============================================================

【大语言模型 (LLM)】(170个)
----------------------------------------
  - codeqwen1.5-7b-chat
  - deepseek-r1
  - deepseek-r1-distill-llama-70b
  - deepseek-r1-distill-llama-8b
  - deepseek-r1-distill-qwen-1.5b
  - deepseek-r1-distill-qwen-14b
  - deepseek-r1-distill-qwen-32b
  - deepseek-r1-distill-qwen-7b
  - deepseek-v3
  - deepseek-v3.1
  - deepseek-v3.2
  - deepseek-v4-flash
  - deepseek-v4-pro
  - qwen-1.8b-chat
  - qwen-1.8b-longcontext-chat
  - qwen-14b-chat
  - qwen-72b-chat
  - qwen-7b-chat
  - qwen-coder-plus
  - qwen-coder-plus-1106
  - qwen-coder-plus-latest
  - qwen-coder-turbo
  - qwen-coder-turbo-0919
  - qwen-coder-turbo-latest
  - qwen-deep-research-2025-12-15
  - qwen-deep-search-planning
  - qwen-flash
  - qwen-flash-character
  - qwen-flash-character-2026-02-26
  - qwen-image-2.0
  - qwen-image-2.0-2026-03-03
  - qwen-image-2.0-pro
  - qwen-image-2.0-pro-2026-03-03
  - qwen-image-2.0-pro-2026-04-22
  - qwen-image-edit-max
  - qwen-image-edit-max-2026-01-16
  - qwen-image-edit-plus
  - qwen-image-edit-plus-2025-10-30
  - qwen-image-edit-plus-2025-12-15
  - qwen-image-max
  - qwen-image-max-2025-12-30
  - qwen-image-plus-2026-01-09
  - qwen-long
  - qwen-math-plus
  - qwen-math-plus-0919
  - qwen-math-plus-latest
  - qwen-math-turbo
  - qwen-math-turbo-0919
  - qwen-math-turbo-latest
  - qwen-max
  - qwen-max-0107
  - qwen-max-0428
  - qwen-max-0919
  - qwen-max-1201
  - qwen-max-2025-01-25
  - qwen-max-latest
  - qwen-max-longcontext
  - qwen-mt-flash
  - qwen-mt-lite
  - qwen-mt-plus
  - qwen-mt-turbo
  - qwen-omni-turbo
  - qwen-plus
  - qwen-plus-2025-01-25
  - qwen-plus-2025-04-28
  - qwen-plus-2025-07-14
  - qwen-plus-2025-09-11
  - qwen-plus-2025-11-05
  - qwen-plus-2025-12-01
  - qwen-plus-latest
  - qwen-turbo
  - qwen-turbo-0919
  - qwen-turbo-2024-11-01
  - qwen-turbo-2025-04-28
  - qwen-turbo-2025-07-15
  - qwen-turbo-latest
  - qwen1.5-0.5b-chat
  - qwen1.5-1.8b-chat
  - qwen1.5-110b-chat
  - qwen1.5-14b-chat
  - qwen1.5-32b-chat
  - qwen1.5-72b-chat
  - qwen1.5-7b-chat
  - qwen2-0.5b-instruct
  - qwen2-1.5b-instruct
  - qwen2-57b-a14b-instruct
  - qwen2-7b-instruct
  - qwen2.5-0.5b-instruct
  - qwen2.5-1.5b-instruct
  - qwen2.5-14b-instruct
  - qwen2.5-14b-instruct-1m
  - qwen2.5-32b-instruct
  - qwen2.5-3b-instruct
  - qwen2.5-72b-instruct
  - qwen2.5-7b-instruct
  - qwen2.5-7b-instruct-1m
  - qwen2.5-coder-14b-instruct
  - qwen2.5-coder-32b-instruct
  - qwen2.5-coder-7b-instruct
  - qwen2.5-math-1.5b-instruct
  - qwen2.5-math-72b-instruct
  - qwen2.5-math-7b-instruct
  - qwen3-0.6b
  - qwen3-1.7b
  - qwen3-14b
  - qwen3-235b-a22b
  - qwen3-235b-a22b-instruct-2507
  - qwen3-235b-a22b-thinking-2507
  - qwen3-30b-a3b
  - qwen3-30b-a3b-instruct-2507
  - qwen3-30b-a3b-thinking-2507
  - qwen3-32b
  - qwen3-4b
  - qwen3-8b
  - qwen3-coder-480b-a35b-instruct
  - qwen3-coder-flash
  - qwen3-coder-next
  - qwen3-coder-plus
  - qwen3-coder-plus-2025-07-22
  - qwen3-coder-plus-2025-09-23
  - qwen3-livetranslate-flash
  - qwen3-livetranslate-flash-2025-12-01
  - qwen3-livetranslate-flash-realtime
  - qwen3-livetranslate-flash-realtime-2025-09-22
  - qwen3-max
  - qwen3-max-2025-09-23
  - qwen3-max-2026-01-23
  - qwen3-max-preview
  - qwen3-next-80b-a3b-instruct
  - qwen3-next-80b-a3b-thinking
  - qwen3-omni-flash
  - qwen3-omni-flash-2025-09-15
  - qwen3-omni-flash-2025-12-01
  - qwen3-omni-flash-realtime
  - qwen3-omni-flash-realtime-2025-09-15
  - qwen3-omni-flash-realtime-2025-12-01
  - qwen3-s2s-flash-realtime-2025-09-22
  - qwen3.5-122b-a10b
  - qwen3.5-27b
  - qwen3.5-35b-a3b
  - qwen3.5-397b-a17b
  - qwen3.5-flash
  - qwen3.5-flash-2026-02-23
  - qwen3.5-omni-flash
  - qwen3.5-omni-flash-2026-03-15
  - qwen3.5-omni-flash-realtime
  - qwen3.5-omni-flash-realtime-2026-03-15
  - qwen3.5-omni-plus
  - qwen3.5-omni-plus-2026-03-15
  - qwen3.5-omni-plus-realtime
  - qwen3.5-omni-plus-realtime-2026-03-15
  - qwen3.5-plus
  - qwen3.5-plus-2026-02-15
  - qwen3.5-plus-2026-04-20
  - qwen3.6-27b
  - qwen3.6-35b-a3b
  - qwen3.6-flash
  - qwen3.6-flash-2026-04-16
  - qwen3.6-max-preview
  - qwen3.6-plus
  - qwen3.6-plus-2026-04-02
  - siliconflow/deepseek-r1-0528
  - siliconflow/deepseek-v3-0324
  - siliconflow/deepseek-v3.1-terminus
  - siliconflow/deepseek-v3.2
  - vanchin/deepseek-ocr
  - vanchin/deepseek-r1
  - vanchin/deepseek-v3
  - vanchin/deepseek-v3.1-terminus
  - vanchin/deepseek-v3.2-think

【视觉理解模型 (Vision)】(19个)
----------------------------------------
  - qwen-vl-max
  - qwen-vl-max-2025-04-02
  - qwen-vl-max-2025-04-08
  - qwen-vl-max-latest
  - qwen-vl-ocr
  - qwen-vl-ocr-2025-11-20
  - qwen-vl-ocr-latest
  - qwen-vl-plus
  - qwen-vl-plus-2025-01-25
  - qwen-vl-plus-2025-05-07
  - qwen-vl-plus-2025-08-15
  - qwen-vl-plus-latest
  - qwen2.5-vl-32b-instruct
  - qwen3-vl-flash
  - qwen3-vl-flash-2025-10-15
  - qwen3-vl-flash-2026-01-22
  - qwen3-vl-plus
  - qwen3-vl-plus-2025-09-23
  - qwen3-vl-plus-2025-12-19

【语音模型 (Audio)】(25个)
----------------------------------------
  - MiniMax/speech-02-hd
  - MiniMax/speech-02-turbo
  - MiniMax/speech-2.8-hd
  - MiniMax/speech-2.8-turbo
  - qwen-tts-2025-05-22
  - qwen3-asr-flash-2026-02-10
  - qwen3-asr-flash-realtime
  - qwen3-asr-flash-realtime-2025-10-27
  - qwen3-asr-flash-realtime-2026-02-10
  - qwen3-tts-flash
  - qwen3-tts-flash-2025-09-18
  - qwen3-tts-flash-2025-11-27
  - qwen3-tts-flash-realtime
  - qwen3-tts-flash-realtime-2025-09-18
  - qwen3-tts-flash-realtime-2025-11-27
  - qwen3-tts-instruct-flash
  - qwen3-tts-instruct-flash-2026-01-26
  - qwen3-tts-instruct-flash-realtime
  - qwen3-tts-instruct-flash-realtime-2026-01-22
  - qwen3-tts-vc-2026-01-22
  - qwen3-tts-vc-realtime-2025-11-27
  - qwen3-tts-vc-realtime-2026-01-15
  - qwen3-tts-vd-2026-01-26
  - qwen3-tts-vd-realtime-2025-12-16
  - qwen3-tts-vd-realtime-2026-01-15

【其他模型】(25个)
----------------------------------------
  - MiniMax-M2.1
  - MiniMax-M2.5
  - MiniMax/MiniMax-M2.1
  - MiniMax/MiniMax-M2.5
  - MiniMax/MiniMax-M2.7
  - glm-4.7
  - glm-5
  - glm-5.1
  - gui-plus
  - kimi-k2-thinking
  - kimi-k2.5
  - kimi-k2.6
  - kimi/kimi-k2.5
  - kimi/kimi-k2.6
  - qvq-max
  - qvq-max-2025-05-15
  - qvq-plus
  - qvq-plus-2025-05-15
  - qwq-plus
  - qwq-plus-2025-03-05
  - tongyi-xiaomi-analysis-flash
  - tongyi-xiaomi-analysis-pro
  - wan2.7-image
  - wan2.7-image-pro
  - z-image-turbo

总计: 239 个模型
============================================================

Process finished with exit code 0

"""