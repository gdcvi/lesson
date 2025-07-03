"""
 * @author: zkyuan
 * @date: 2025/7/3 14:18
 * @description: 使用transformers调用本地模型，生成回复
"""
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "D:\AI_Model\Qwen\Qwen3-0.6B"

# 1、加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

# 2、定义用户输入
prompt = "什么是大语言模型"
messages = [
    {"role": "user", "content": prompt}
]

# 3、生成可用于模型推理的文本格式模版
text = tokenizer.apply_chat_template(
    messages,
    # 不进行分词操作，仅返回原始文本
    tokenize=False,
    # 在末尾添加生成提示（如 assistant\n），表示等待模型输出
    add_generation_prompt=True,
    # 启用思考模式，表示模型正在思考，请等待模型输出
    enable_thinking=True
)

# 4、生成模型可接受的输入格式，并将其移动到与模型相同的设备（如 GPU）上
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# 5、调用模型生成结果
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=32768
)
print("generated_ids:", generated_ids)

# 对结果数据进行处理
output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
print("output_ids:", output_ids)

# 解析 Thinking 内容
try:
    # 找出列表 output_ids 中最后一个值为 151668 的元素的下标（索引）。151668 (</think>)
    index = len(output_ids) - output_ids[::-1].index(151668)  # 将列表倒序索引取反，再找第一个think，最后换算成实际索引
except ValueError:
    index = 0

# 6、解码输出
thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

print("thinking content:", thinking_content)
print("content:", content)
