"""
 * @author: zkyuan
 * @date: 2025/8/19 10:13
 * @description: 各大模型汇总
"""
import os
import time

from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI, ChatTongyi
from langchain_openai import ChatOpenAI

load_dotenv()


# 初始化各模型
def init_models():
    # ChatGPT (OpenAI)
    chatgpt = ChatOpenAI(
        model_name="gpt-4o",
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # 通义千问
    tongyi = ChatTongyi(
        model_name="qwen-turbo",
        streaming=True,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )

    # DeepSeek (使用OpenAI兼容API)
    deepseek = ChatOpenAI(
        model_name="deepseek-chat",
        base_url='https://api.deepseek.com/v1',
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )

    # 智谱AI (GLM)
    zhipu = ChatZhipuAI(
        model="glm-4",
        streaming=True,
        api_key=os.getenv("ZHIPU_API_KEY"),
    )

    # 百度 （千帆）
    wenxin = ChatOpenAI(
        base_url="https://qianfan.baidubce.com/v2",
        api_key=os.getenv("QIANFAN_API_KEY"),
        model_name="ernie-3.5-8k",
        streaming=True,
    )

    return {
        "ChatGPT": chatgpt,
        "通义千问": tongyi,
        "DeepSeek": deepseek,
        "智谱AI": zhipu,
        "文心一言": wenxin
    }


if __name__ == "__main__":
    models = init_models()
    prompt = "用200字解释量子计算的基本原理及其应用前景"
    print(f"====== 问题 =====\n{prompt}\n")
    for name, model in models.items():
        print(f"\n🚀 开始 {name} 响应:")
        print(model.invoke(prompt))
        time.sleep(1)  # 模型间间隔

