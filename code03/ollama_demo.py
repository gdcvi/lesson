import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"
payload = {
    "model": "qwen3:8b",
    "messages":  [{"role": "user", "content": "怎么做西红柿炒蛋"}],
    "stream": False  # 流式响应
}

response = requests.post(OLLAMA_API_URL, json=payload, stream=False)
# 检查HTTP状态码
response.raise_for_status()
print(response)

response_json = response.json()
# 提取消息内容
content = response_json['message']['content']
print(response_json)
print(content)

