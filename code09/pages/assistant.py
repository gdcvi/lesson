from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import streamlit as st
import json
import time
import tiktoken
import os, sys


# 计算消息列表使用的token数量
def num_tokens_from_messages(messages, model):
    """
    返回消息列表使用的token数。
    """
    try:
        # 选择对应的编码器
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found.")
        encoding = tiktoken.get_encoding("cl100k_base")

    # 定义不同模型的token参数
    tokens_per_message = 3  # 每条消息的基础token数
    tokens_per_name = 1  # 名称字段的token数

    if model == "gpt-4o":
        tokens_per_message = 4
        tokens_per_name = -1  # 对于有些大模型，名称字段不计入token

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens


# 使用缓存创建LangChain聊天模型
@st.cache_resource
def get_langchain_chat_model(url, api_key, model_name, temperature, max_tokens, stream):
    return ChatOpenAI(
        base_url=url,
        api_key=api_key,
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        streaming=stream
    )


# 将消息字典列表转换为LangChain消息对象
def convert_to_langchain_messages(messages):
    langchain_messages = []
    for msg in messages:
        if msg["role"] == "system":
            langchain_messages.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            langchain_messages.append(AIMessage(content=msg["content"]))
    return langchain_messages


# 聊天页面
def chatchat_page():
    st.title("AI智能助手")
    # 初始化参数
    api_key = (
        st.session_state.api_key
        if "api_key" in st.session_state and st.session_state.api_key != ""
        else None
    )
    if api_key is None:
        st.error("请现在home页面配置API Key")
        st.stop()

    if "base_url" in st.session_state:
        base_url = st.session_state.base_url
    else:
        base_url = "https://api.openai-hk.com/v1"

    # 获取当前脚本文件所在的目录路径
    src_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    # 读取默认配置文件
    with open(os.path.join(src_path, 'config/default.json'), 'r', encoding='utf-8') as f:
        config_defalut = json.load(f)

    # 显示配置项
    st.session_state['model_list'] = config_defalut["completions"]["models"]
    model_name = st.selectbox('Models', st.session_state.model_list, key='chat_model_name')

    # 系统提示词选项
    option = st.radio("系统提示词", ("自定义", "选择"), horizontal=True, index=0)
    if option == "自定义":
        system_prompt = st.text_input('System Prompt (点击 刷新 按钮后生效)',
                                      config_defalut["completions"]["system_prompt"])
    else:
        # 加载预设提示词
        with open(os.path.join(src_path, 'config/prompt.json'), 'r', encoding='utf-8') as f:
            masks = json.load(f)
        masks_zh = [item['name'] for item in masks['zh']]
        masks_zh_name = st.selectbox('prompts', masks_zh)
        for item in masks['zh']:
            if item['name'] == masks_zh_name:
                system_prompt = item['context']
                break

    # 是否使用默认参数
    if not st.checkbox('使用默认参数', True):
        max_tokens = st.number_input('Max Tokens', 1, 200000, config_defalut["completions"]["max_tokens"],
                                     key='max_tokens')
        temperature = st.slider('Temperature', 0.0, 1.0, config_defalut["completions"]["temperature"],
                                key='temperature')
        stream = st.checkbox('Stream', config_defalut["completions"]["stream"], key='stream')
    else:
        max_tokens = config_defalut["completions"]["max_tokens"]
        temperature = config_defalut["completions"]["temperature"]
        stream = config_defalut["completions"]["stream"]

    # 初始化聊天记录
    if 'chat_messages' not in st.session_state:
        st.session_state['chat_messages'] = [{"role": "system", "content": system_prompt}]

    # 清除历史记录
    if st.button("刷新"):
        st.session_state.chat_messages = [{"role": "system", "content": system_prompt}]

    # 显示聊天记录
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    # 处理用户输入
    if prompt := st.chat_input():
        # 显示用户的输入内容
        st.chat_message("user").write(prompt)
        with st.chat_message('assistant'):
            # 显示一个"Thinking..."的加载动画
            with st.spinner('Thinking...'):
                # 记录开始时间
                start_time = time.time()
                try:
                    # 将用户消息添加到聊天历史
                    st.session_state.chat_messages.append({"role": "user", "content": prompt})

                    # 获取LangChain聊天模型
                    chat_model = get_langchain_chat_model(
                        base_url,
                        api_key,
                        model_name,
                        temperature,
                        max_tokens,
                        stream
                    )

                    # 转换消息格式为LangChain格式
                    langchain_messages = convert_to_langchain_messages(st.session_state.chat_messages)

                    # 流式处理
                    if stream:
                        # 创建一个占位符，用于显示流式处理中的文本
                        placeholder = st.empty()
                        streaming_text = ''
                        for chunk in chat_model.stream(langchain_messages):
                            if chunk.content:
                                streaming_text += chunk.content
                                placeholder.markdown(streaming_text)
                        model_msg = streaming_text
                    # 非流式处理
                    else:
                        response = chat_model.invoke(langchain_messages)
                        model_msg = response.content
                        st.markdown(model_msg)

                    # 记录结束时间
                    end_time = time.time()

                    # 将AI回复添加到聊天历史
                    st.session_state.chat_messages.append({"role": "assistant", "content": model_msg})

                    # 计算当前对话的消耗的token数
                    if config_defalut["completions"]["num_tokens"]:
                        try:
                            num_tokens = num_tokens_from_messages(st.session_state.chat_messages, model=model_name)
                            info_num_tokens = f"use tokens: {num_tokens}"
                            st.info(info_num_tokens)
                        except Exception as e:
                            print(e)
                    # 生成当前对话耗时信息
                    if config_defalut["completions"]["use_time"]:
                        st.info(f"Use time: {round(end_time - start_time, 2)}s")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state.chat_messages.pop()  # 移除最后添加的用户消息


if __name__ == "__main__":
    chatchat_page()
