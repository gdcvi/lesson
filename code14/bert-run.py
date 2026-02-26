from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# 设置具体包含 config.json 的目录
# 官方模型
# model_dir = r"C:\Users\HP\.cache\huggingface\hub\models--bert-base-chinese\snapshots\c30a6ed22ab4564dc1e3b2ecbf6e766b0611a33f"  # 默认位置在C盘，替换为实际路径
# model_dir = r"D:\huggingface\hub\models--bert-base-chinese\snapshots\8f23c25b06e129b6c986331a13d8d025a92cf0ea"  # 手动修改后的位置，我改为D盘了。替换为实际路径
# 自己训练的模型
model_dir = r"./sentiment_model"

# 加载模型和分词器
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# 创建标签映射
label_mapping = {0: "负面", 1: "正面"}

# 使用加载的模型和分词器创建分类任务的 pipeline
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device="cpu")

# 执行分类任务并美化输出
print("=== 情感分析结果 ===")

test_sentences = [
    "我今天心情很好",
    "你好，我是福州第一温柔",
    "我今天很生气",
    "你好坏哦，我好喜欢",
    "你好坏",
    "你好帅"
]

for i, sentence in enumerate(test_sentences, 1):
    result = classifier(sentence)[0]
    # 转换标签
    label_id = int(result['label'].split('_')[1])
    chinese_label = label_mapping[label_id]
    score = result['score']
    
    print(f"{i}. 文本: {sentence}")
    print(f"   预测: {chinese_label} (置信度: {score:.4f})")
    print()
"""
=== 情感分析结果 ===
Device set to use cpu
1. 文本: 我今天心情很好
   预测: 正面 (置信度: 0.9999)

2. 文本: 你好，我是福州第一温柔
   预测: 正面 (置信度: 0.9991)

3. 文本: 我今天很生气
   预测: 负面 (置信度: 0.9997)

4. 文本: 你好坏哦，我好喜欢
   预测: 正面 (置信度: 0.9892)

5. 文本: 你好坏
   预测: 负面 (置信度: 0.9984)

6. 文本: 你好帅
   预测: 正面 (置信度: 0.9977)
"""