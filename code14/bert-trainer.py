# 1：环境准备
# pip install torch transformers datasets scikit-learn
# 可以自定义huggingface模型下载的位置
# setx HF_HOME "D:\huggingface"  默认位置C:\Users\HP\.cache\huggingface
from transformers import BertTokenizer, BertForSequenceClassification

# 2：加载中文 BERT 预训练模型
# 加载 分词器和 bert 中文预训练模型
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
# 注意：ChnSentiCorp数据集是二分类（正面/负面），所以num_labels应该设为2
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=2)

# 3：加载 ChnSentiCorp 数据集并进行清洗
from datasets import load_dataset
import os

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建本地数据集路径
local_dataset_path = os.path.join(current_dir, 'ChnSentiCorp')

# 从本地路径加载 ChnSentiCorp 数据集
dataset = load_dataset('parquet', 
                      data_files={
                          'train': os.path.join(local_dataset_path, 'data', 'train-00000-of-00001-02f200ca5f2a7868.parquet'),
                          'validation': os.path.join(local_dataset_path, 'data', 'validation-00000-of-00001-405befbaa3bcf1a2.parquet'),
                          'test': os.path.join(local_dataset_path, 'data', 'test-00000-of-00001-5372924f059fe767.parquet')
                      })

import re

# 定义数据清洗函数
def clean_text(text):
    # 去除标点符号
    text = re.sub(r'[^\w\s]', '', text)
    # 去除前后空格
    text = text.strip()
    return text

# 对数据集中的文本进行清洗
dataset = dataset.map(lambda x: {'text': clean_text(x['text'])})

# 4：数据预处理
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)

# 对数据集进行分词和编码
encoded_dataset = dataset.map(tokenize_function, batched=True)

# 5：训练模型
from transformers import Trainer, TrainingArguments
from sklearn.metrics import accuracy_score

# 定义评估函数
def compute_metrics(p):
    # p.predictions 是模型对输入数据的预测输出，
    preds = p.predictions.argmax(-1)  # argmax(-1) 的作用是沿着最后一个维度（通常是类别维度）取最大值对应的索引，即模型预测的类别
    # p.label_ids 是真实的标签。
    return {"accuracy": accuracy_score(p.label_ids, preds)}

# 定义训练参数
# 定义训练参数，创建一个TrainingArguments对象
training_args = TrainingArguments(
    # 指定训练输出的目录，用于保存模型和其他输出文件
    output_dir='./results',
    # 设置训练的轮数
    num_train_epochs=3,
    # 每个设备（如GPU）上的训练批次大小
    per_device_train_batch_size=2,
    # 每个设备上的评估批次大小
    per_device_eval_batch_size=2,
    # 学习率
    learning_rate=2e-5,
    # 设置评估策略为每个epoch结束后进行评估
    eval_strategy="epoch",
    # 保存策略
    save_strategy="epoch",
    # 指定日志保存的目录
    logging_dir="./logs",
    # 日志记录频率
    logging_steps=100,
    # 是否覆盖输出目录
    overwrite_output_dir=True,
    # 是否在训练过程中保存最佳模型
    load_best_model_at_end=True,
    # 早停监控指标
    metric_for_best_model="eval_accuracy",
)

print("---------------开始训练---------------")
# 使用 Trainer 进行训练 ,Trainer 是一个简单但功能齐全的 PyTorch 训练和评估循环
trainer = Trainer(
    model=model,
    args=training_args,
    # 训练集
    train_dataset=encoded_dataset['train'],
    # 评估集
    eval_dataset=encoded_dataset['validation'],
    # 计算评估指标
    compute_metrics=compute_metrics,
)

# 开始训练
trainer.train()

# 步骤 6：评估模型性能
# 在测试集上评估模型
final_metrics = trainer.evaluate(encoded_dataset['test'], metric_key_prefix="test")
print(f"最终测试结果: {final_metrics}")

"""{'eval_loss': 0.2, 'eval_accuracy': 0.85}
# eval_loss: 0.2：这是模型在测试集上的损失值。
# 损失值是一个衡量模型预测与实际标签之间差异的指标。
# 较低的损失值通常表示模型的预测更接近于真实标签。
# eval_accuracy: 0.85：这是模型在测试集上的准确率。
# 准确率是指模型正确预测的样本数量占总样本数量的比例。
# 在这个例子中，准确率为 0.85，意味着模型在测试集上有 85% 的样本被正确分类。
"""

# 7：导出模型
# 保存模型和分词器
model.save_pretrained('./sentiment_model')
tokenizer.save_pretrained('./sentiment_model')