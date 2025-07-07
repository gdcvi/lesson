"""
 * @author: zkyuan
 * @date: 2025/7/7 10:08
 * @description: 基于本地ollama的聊天机器人
"""

import requests
import json

# Ollama的API的URL
OLLAMA_API_URL = "http://localhost:11434/api/chat"

# 对话历史，用于支持多轮对话
conversation_history = []


def chat_with_ollama(prompt: str):
    """
    发送用户输入到Ollama API并流式处理响应。
    """
    # 将用户的当前输入添加到对话历史中
    conversation_history.append({"role": "user", "content": prompt})

    # 构建请求体
    payload = {
        "model": "qwen3:8b",  # 本地模型
        "messages": conversation_history,
        "stream": True  # 开启流式响应
    }

    try:
        # 使用 stream=True 来接收流式响应
        with requests.post(OLLAMA_API_URL, json=payload, stream=True) as response:
            # 检查HTTP状态码
            response.raise_for_status()

            result = ""
            print("\n🤖AI: ", end="", flush=True)

            # 逐行迭代响应内容
            for line in response.iter_lines():
                if line:
                    # 解码JSON字符串
                    chunk = json.loads(line.decode('utf-8'))

                    # 提取消息内容
                    content = chunk['message']['content']
                    # end=""打印后不换行，默认是\n
                    print(content, end="", flush=True)
                    result += content

                    # Ollama 的流式 API 在响应的最后一个数据块中会包含 "done": true 字段，表示本次对话回复已结束。
                    if chunk.get('done', False):
                        # 将完整的助手回答添加到历史记录中
                        conversation_history.append({"role": "assistant", "content": result})
                        print()

    except requests.exceptions.RequestException as e:
        print(f"\nerror-->无法连接到Ollama API: {e}")
    except json.JSONDecodeError as e:
        print(f"\nerror-->解析JSON响应失败: {e}")


if __name__ == "__main__":
    print("🤖chat with ollama🤖")
    print("输入 'exit' 或 'quit' 退出。")
    print("-" * 50)

    while True:
        user_input = input("👲你: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        chat_with_ollama(user_input)

