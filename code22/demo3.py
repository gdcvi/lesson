"""
使用LangChain 0.3版本实现的Callback回调示例
基于通义千问(qwen)大模型，演示自定义回调处理器的使用
"""
import os
from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置API密钥
os.environ["DASHSCOPE_API_KEY"] = os.getenv("DASHSCOPE_API_KEY", "your-api-key-here")


# 定义一个日志处理器类，继承自BaseCallbackHandler
class LoggingHandler(BaseCallbackHandler):
    """自定义回调处理器 - 用于记录链和模型的执行过程"""
    
    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        **kwargs: Any
    ) -> None:
        """当聊天模型开始时调用的方法"""
        print("=" * 50)
        print("[LoggingHandler] 聊天模型开始执行")
        print(f"[LoggingHandler] 消息内容: {messages}")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """当LLM结束时调用的方法"""
        print(f"[LoggingHandler] LLM执行结束")
        print(f"[LoggingHandler] 响应结果: {response.generations}")
        print("=" * 50)

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """当链开始时调用的方法"""
        print("-" * 50)
        print(f"[LoggingHandler] 链开始执行: {serialized.get('name', 'Unknown')}")
        print(f"[LoggingHandler] 输入参数: {inputs}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """当链结束时调用的方法"""
        print(f"[LoggingHandler] 链执行结束")
        print(f"[LoggingHandler] 输出结果: {outputs}")
        print("-" * 50)

class LoggingHandler2(BaseCallbackHandler):
    """第二个自定义回调处理器 - 用于对比多个回调的执行顺序"""
    
    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        **kwargs: Any
    ) -> None:
        """当聊天模型开始时调用的方法"""
        print("*** [LoggingHandler2] 聊天模型启动 ***")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """当LLM结束时调用的方法"""
        print(f"*** [LoggingHandler2] LLM完成，token消耗: {response.llm_output.get('token_usage', 'N/A') if response.llm_output else 'N/A'} ***")

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """当链开始时调用的方法"""
        print(f"+++ [LoggingHandler2] 链启动: {serialized.get('name', 'Unknown')} +++")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """当链结束时调用的方法"""
        print(f"+++ [LoggingHandler2] 链完成 +++")

# 创建包含两个回调处理器实例的列表
callbacks = [LoggingHandler(), LoggingHandler2()]

# 实例化ChatTongyi对象，使用qwen-plus模型
llm = ChatTongyi(
    model="qwen-plus",
    temperature=0.3,
)

# 创建一个聊天提示模板，模板内容为"What is 1 + {number}?"
prompt = ChatPromptTemplate.from_template("What is 1 + {number}?")

# 将提示模板和LLM组合成一个链
chain = prompt | llm

# 调用链的invoke方法，传入参数number为"2"，并配置回调
print("\n开始执行链式调用...\n")
result = chain.invoke({"number": "2"}, config={"callbacks": callbacks})

print("\n最终结果:")
print(result)
