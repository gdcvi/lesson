
import os

from dotenv import load_dotenv
# 文心一言 pip install qianfan
# from langchain_community.chat_models import QianfanChatEndpoint
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    base_url="https://qianfan.baidubce.com/v2",
    api_key=os.environ["QIANFAN_API_KEY"],
    model_name="ernie-3.5-8k",
    streaming=True,
)
messages = "你好，你是谁?"

print(model.invoke(messages))


