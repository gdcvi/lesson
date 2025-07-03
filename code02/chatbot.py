"""
 * @author: zkyuan
 * @date: 2025/7/3 14:13
 * @description: 简易聊天机器人
"""
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "D:\AI_Model\Qwen\Qwen3-0.6B"

# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 将模型设置为评估模式（评估模式和训练模式的区别在于是否进行梯度计算）
model.eval()


def chat_with_bot(prompt, chat_history=[], max_length=1000, temperature=0.7, top_p=0.9):
    # 将历史记录和当前输入拼接
    full_prompt = "\n".join(chat_history + [prompt])

    # 编码输入并生成 attention_mask
    inputs = tokenizer(full_prompt, return_tensors="pt", return_attention_mask=True)

    # 生成回复（禁用梯度计算）
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    # 解码生成的文本
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # 更新对话历史
    chat_history.append(f"你: {prompt}")
    chat_history.append(f"聊天机器人: {response}")

    return response, chat_history


if __name__ == "__main__":
    print("聊天机器人已启动！输入 '退出'、'exit'、'quit' 可以结束对话。")
    history = []
    while True:
        # 获取用户输入
        user_input = input("你: ")

        # 如果用户输入“退出”，结束对话
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("聊天机器人: 再见！")
            break

        # 生成回复
        response, history = chat_with_bot(prompt=user_input, chat_history=history, max_length=1000)
        print(f"聊天机器人: {response}")