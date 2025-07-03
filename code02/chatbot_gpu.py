from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "D:\AI_Model\Qwen\Qwen3-0.6B"

# 检查是否有可用的 GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"使用设备: {device}")

# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 将模型移动到 GPU（如果可用）
model.to(device)

# 将模型设置为评估模式
model.eval()


def chat_with_bot(prompt, chat_history=[], max_length=1000, max_new_tokens=100, temperature=0.7, top_p=0.9):
    # 将历史记录和当前输入拼接
    full_prompt = "\n".join(chat_history + [prompt])

    # 编码输入并生成 attention_mask，并移动到 GPU
    inputs = tokenizer(full_prompt, return_tensors="pt", return_attention_mask=True).to(device)

    # 生成回复
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=max_length,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    # 解码生成的文本（需将 tensor 移回 CPU）
    response = tokenizer.decode(outputs[0].cpu(), skip_special_tokens=True)

    # 更新对话历史
    chat_history.append(f"你: {prompt}")
    chat_history.append(f"聊天机器人: {response}")

    return response, chat_history


if __name__ == "__main__":
    print("聊天机器人已启动！输入 '退出'、'exit'、'quit' 可以结束对话。")
    history = []
    while True:
        user_input = input("你: ")
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("聊天机器人: 再见！")
            break

        response, chat_history = chat_with_bot(prompt=user_input, chat_history=history, max_length=2000)
        history.append(f"你: {user_input}")
        history.append(f"聊天机器人: {response}")
        print(f"聊天机器人: {response}")
