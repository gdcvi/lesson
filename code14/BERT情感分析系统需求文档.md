# BERT中文情感分析系统 - 需求规格说明书

## 1. 项目概述

### 1.1 项目名称
BERT中文情感分析微调与推理系统

### 1.2 项目描述
本项目基于预训练的中文BERT模型（bert-base-chinese），使用ChnSentiCorp数据集进行情感分析任务的专项微调，实现中文文本的正面/负面情感二分类功能。系统包含两个核心模块：
- **训练模块**：加载预训练模型、处理数据集、执行微调训练、评估模型性能、导出模型文件
- **推理模块**：加载微调后的模型、对输入文本进行情感预测、输出可视化结果

### 1.3 技术栈
- **深度学习框架**：PyTorch (torch)
- **自然语言处理库**：Hugging Face Transformers
- **数据处理库**：Hugging Face Datasets
- **机器学习工具**：scikit-learn（用于准确率计算）
- **正则表达式**：re（用于文本清洗）
- **操作系统接口**：os（用于路径处理）

---

## 2. 功能需求

### 2.1 训练模块（bert-trainer.py）

#### 2.1.1 环境准备与依赖安装
**功能描述**：确保系统已安装必要的Python包

**依赖清单**：
```bash
pip install torch transformers datasets scikit-learn
```

**HuggingFace缓存配置**（可选）：
- 默认缓存位置：`C:\Users\<用户名>\.cache\huggingface`
- 自定义缓存位置命令：`setx HF_HOME "D:\huggingface"`

#### 2.1.2 加载预训练模型和分词器
**功能描述**：从HuggingFace模型库或本地缓存加载中文BERT预训练模型

**技术要求**：
- 使用 `BertTokenizer.from_pretrained('bert-base-chinese')` 加载分词器
- 使用 `BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=2)` 加载模型
- **关键参数**：`num_labels=2`（因为ChnSentiCorp是二分类任务：正面/负面）

**代码示例**：
```python
from transformers import BertTokenizer, BertForSequenceClassification

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=2)
```

#### 2.1.3 加载ChnSentiCorp数据集
**功能描述**：从本地Parquet文件加载ChnSentiCorp中文情感分析数据集

**数据集结构**：
- 数据集来源：https://huggingface.co/datasets/lansinuote/ChnSentiCorp
- 数据格式：Parquet格式
- 数据划分：
  - 训练集（train）：`data/train-00000-of-00001-02f200ca5f2a7868.parquet`
  - 验证集（validation）：`data/validation-00000-of-00001-405befbaa3bcf1a2.parquet`
  - 测试集（test）：`data/test-00000-of-00001-5372924f059fe767.parquet`

**目录结构要求**：
```
code14/
└── ChnSentiCorp/
    └── data/
        ├── train-00000-of-00001-02f200ca5f2a7868.parquet
        ├── validation-00000-of-00001-405befbaa3bcf1a2.parquet
        └── test-00000-of-00001-5372924f059fe767.parquet
```

**加载方式**：
- 使用相对路径动态获取数据集位置（基于当前脚本所在目录）
- 使用 `load_dataset('parquet', data_files={...})` 加载

**代码示例**：
```python
import os
from datasets import load_dataset

current_dir = os.path.dirname(os.path.abspath(__file__))
local_dataset_path = os.path.join(current_dir, 'ChnSentiCorp')

dataset = load_dataset('parquet',
                       data_files={
                           'train': os.path.join(local_dataset_path, 'data',
                                                 'train-00000-of-00001-02f200ca5f2a7868.parquet'),
                           'validation': os.path.join(local_dataset_path, 'data',
                                                      'validation-00000-of-00001-405befbaa3bcf1a2.parquet'),
                           'test': os.path.join(local_dataset_path, 'data',
                                                'test-00000-of-00001-5372924f059fe767.parquet')
                       })
```

#### 2.1.4 数据清洗
**功能描述**：对数据集中的文本进行预处理，去除噪声

**清洗规则**：
1. 去除所有标点符号（保留字母、数字、空格、下划线）
2. 去除文本前后的空白字符

**实现方式**：
- 使用正则表达式 `re.sub(r'[^\w\s]', '', text)` 去除标点
- 使用 `text.strip()` 去除前后空格

**代码示例**：
```python
import re

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

dataset = dataset.map(lambda x: {'text': clean_text(x['text'])})
```

#### 2.1.5 数据预处理（分词与编码）
**功能描述**：将文本转换为BERT模型可接受的输入格式

**处理要求**：
- 使用之前加载的tokenizer对文本进行分词
- 设置最大序列长度：128
- 启用填充（padding='max_length'）：将所有序列填充到相同长度
- 启用截断（truncation=True）：超过128长度的文本将被截断
- 批量处理（batched=True）：提高处理效率

**代码示例**：
```python
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)

encoded_dataset = dataset.map(tokenize_function, batched=True)
```

#### 2.1.6 定义评估指标
**功能描述**：定义模型性能评估函数，计算准确率

**评估逻辑**：
- 从模型预测输出中提取预测类别（使用argmax获取概率最大的类别索引）
- 与真实标签对比，计算准确率

**代码示例**：
```python
from sklearn.metrics import accuracy_score

def compute_metrics(p):
    preds = p.predictions.argmax(-1)
    return {"accuracy": accuracy_score(p.label_ids, preds)}
```

#### 2.1.7 配置训练参数
**功能描述**：设置模型训练的超参数和训练策略

**训练参数配置**：
| 参数名 | 值 | 说明 |
|--------|-----|------|
| output_dir | './results' | 训练输出目录，保存模型检查点 |
| num_train_epochs | 3 | 训练轮数 |
| per_device_train_batch_size | 2 | 训练批次大小（每个GPU/CPU） |
| per_device_eval_batch_size | 2 | 评估批次大小（每个GPU/CPU） |
| learning_rate | 2e-5 | 学习率（2×10⁻⁵） |
| eval_strategy | "epoch" | 评估策略：每个epoch结束后评估 |
| save_strategy | "epoch" | 保存策略：每个epoch结束后保存 |
| logging_dir | "./logs" | 日志保存目录 |
| logging_steps | 100 | 每100步记录一次日志 |
| overwrite_output_dir | True | 覆盖已存在的输出目录 |
| load_best_model_at_end | True | 训练结束时加载最佳模型 |
| metric_for_best_model | "eval_accuracy" | 最佳模型的评判指标 |

**代码示例**：
```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    learning_rate=2e-5,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=100,
    overwrite_output_dir=True,
    load_best_model_at_end=True,
    metric_for_best_model="eval_accuracy",
)
```

#### 2.1.8 执行模型训练
**功能描述**：使用Trainer API进行模型训练

**训练配置**：
- 模型：之前加载的BERT模型
- 训练参数：上述配置的training_args
- 训练数据集：encoded_dataset['train']
- 验证数据集：encoded_dataset['validation']
- 评估函数：compute_metrics

**代码示例**：
```python
from transformers import Trainer

print("---------------开始训练---------------")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset['train'],
    eval_dataset=encoded_dataset['validation'],
    compute_metrics=compute_metrics,
)

trainer.train()
```

#### 2.1.9 模型评估
**功能描述**：在测试集上评估最终模型性能

**评估要求**：
- 使用测试集（encoded_dataset['test']）进行评估
- 设置metric_key_prefix="test"以区分测试结果
- 输出最终测试指标（loss和accuracy）

**预期输出示例**：
```
最终测试结果: {'test_loss': 0.2, 'test_accuracy': 0.85}
```

**代码示例**：
```python
final_metrics = trainer.evaluate(encoded_dataset['test'], metric_key_prefix="test")
print(f"最终测试结果: {final_metrics}")
```

#### 2.1.10 模型导出
**功能描述**：保存微调后的模型和分词器到指定目录

**保存要求**：
- 保存目录：`./sentiment_model`
- 保存内容：
  - 模型文件（model.safetensors或pytorch_model.bin）
  - 配置文件（config.json）
  - 分词器文件（vocab.txt, tokenizer_config.json, special_tokens_map.json等）

**代码示例**：
```python
model.save_pretrained('./sentiment_model')
tokenizer.save_pretrained('./sentiment_model')
```

**输出目录结构**：
```
sentiment_model/
├── config.json
├── model.safetensors
├── special_tokens_map.json
├── tokenizer_config.json
└── vocab.txt
```

---

### 2.2 推理模块（bert-run.py）

#### 2.2.1 加载微调后的模型
**功能描述**：从本地目录加载训练好的情感分析模型和分词器

**加载要求**：
- 模型路径：`./sentiment_model`（相对于脚本位置）
- 使用 `AutoModelForSequenceClassification.from_pretrained()` 加载模型
- 使用 `AutoTokenizer.from_pretrained()` 加载分词器

**代码示例**：
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_dir = r"./sentiment_model"
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
```

#### 2.2.2 创建标签映射
**功能描述**：建立数字标签到中文情感标签的映射关系

**映射规则**：
- 0 → "负面"
- 1 → "正面"

**代码示例**：
```python
label_mapping = {0: "负面", 1: "正面"}
```

#### 2.2.3 创建分类Pipeline
**功能描述**：使用HuggingFace Pipeline API简化推理流程

**Pipeline配置**：
- 任务类型："text-classification"
- 模型：加载的情感分析模型
- 分词器：加载的分词器
- 设备："cpu"（可根据实际情况改为"cuda"使用GPU）

**代码示例**：
```python
from transformers import pipeline

classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device="cpu")
```

#### 2.2.4 执行情感分析推理
**功能描述**：对输入的中文文本进行情感分类预测

**测试样例**：
```python
test_sentences = [
    "我今天心情很好",
    "你好，我是福州第一温柔",
    "我今天很生气",
    "你好坏哦，我好喜欢",
    "你好坏",
    "你好帅"
]
```

**推理逻辑**：
1. 遍历测试句子列表
2. 对每个句子调用classifier进行分类
3. 从返回结果中提取标签和置信度分数
4. 将LABEL_0/LABEL_1转换为中文标签（负面/正面）
5. 格式化输出结果

**输出格式要求**：
```
=== 情感分析结果 ===
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
```

**代码示例**：
```python
print("=== 情感分析结果 ===")

for i, sentence in enumerate(test_sentences, 1):
    result = classifier(sentence)[0]
    # 转换标签：从 "LABEL_0" 提取数字 0
    label_id = int(result['label'].split('_')[1])
    chinese_label = label_mapping[label_id]
    score = result['score']
    
    print(f"{i}. 文本: {sentence}")
    print(f"   预测: {chinese_label} (置信度: {score:.4f})")
    print()
```

---

## 3. 非功能性需求

### 3.1 性能要求
- **训练时间**：取决于硬件配置，CPU环境下约需数小时，GPU环境下约需数十分钟
- **推理速度**：单句推理时间 < 1秒（CPU）
- **内存占用**：
  - 训练阶段：建议至少8GB RAM（GPU显存建议4GB以上）
  - 推理阶段：约2-4GB RAM

### 3.2 准确性要求
- 测试集准确率目标：≥ 85%
- 典型输出示例：`{'test_loss': 0.2, 'test_accuracy': 0.85}`

### 3.3 兼容性要求
- Python版本：3.7+
- 支持平台：Windows、Linux、macOS
- 支持设备：CPU、GPU（CUDA）

### 3.4 可维护性要求
- 代码需包含详细的中文注释
- 关键步骤需有清晰的打印输出（如"---------------开始训练---------------"）
- 使用相对路径而非硬编码绝对路径

---

## 4. 数据结构定义

### 4.1 数据集字段
ChnSentiCorp数据集包含以下字段：
- **text**（字符串）：中文文本内容
- **label**（整数）：情感标签（0=负面，1=正面）

### 4.2 模型输入格式
经过tokenize_function处理后的数据结构：
```python
{
    'input_ids': [[101, 2769, 3221, ..., 102], ...],  # token ID序列
    'token_type_ids': [[0, 0, 0, ..., 0], ...],       # 句子类型ID
    'attention_mask': [[1, 1, 1, ..., 1], ...],       # 注意力掩码
    'labels': [1, 0, 1, ...]                          # 真实标签
}
```

### 4.3 模型输出格式
Pipeline推理返回结果：
```python
[
    {
        'label': 'LABEL_1',  # 或 'LABEL_0'
        'score': 0.9958      # 置信度分数（0-1之间）
    }
]
```

---

## 5. 文件组织结构

```
code14/
├── ChnSentiCorp/                  # 数据集目录
│   └── data/
│       ├── train-*.parquet
│       ├── validation-*.parquet
│       └── test-*.parquet
├── bert-trainer.py                # 训练脚本
├── bert-run.py                    # 推理脚本
├── results/                       # 训练输出目录（自动生成）
│   └── checkpoint-*/
├── logs/                          # 训练日志目录（自动生成）
│   └── runs/
└── sentiment_model/               # 导出的模型目录（训练后生成）
    ├── config.json
    ├── model.safetensors
    ├── special_tokens_map.json
    ├── tokenizer_config.json
    └── vocab.txt
```

---

## 6. 完整代码实现

### 6.1 训练脚本（bert-trainer.py）

```python
"""
 * @author: zkyuan
 * @date: 2026/2/26 14:37
 * @description: bert模型情感分析专项微调
"""
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

# 加载 ChnSentiCorp 数据集
# 数据集地址：https://huggingface.co/datasets/lansinuote/ChnSentiCorp
# dataset = load_dataset('lansinuote/ChnSentiCorp')
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建本地数据集路径
local_dataset_path = os.path.join(current_dir, 'ChnSentiCorp')

# 从本地路径加载 ChnSentiCorp 数据集
dataset = load_dataset('parquet',
                       data_files={
                           'train': os.path.join(local_dataset_path, 'data',
                                                 'train-00000-of-00001-02f200ca5f2a7868.parquet'),
                           'validation': os.path.join(local_dataset_path, 'data',
                                                      'validation-00000-of-00001-405befbaa3bcf1a2.parquet'),
                           'test': os.path.join(local_dataset_path, 'data',
                                                'test-00000-of-00001-5372924f059fe767.parquet')
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
```

### 6.2 推理脚本（bert-run.py）

```python
"""
 * @author: zkyuan
 * @date: 2026/2/26 14:40
 * @description: 测试微调效果
"""
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

# 执行分类任务
# LABEL_0：在二分类情感分析任务中，0 通常表示"负面"情感。
# LABEL_1：相应地，1 通常表示"正面"情感。
# output = classifier("我今天心情很好")
# print(output)
# [{'label': 'LABEL_1', 'score': 0.9958015084266663}]

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
```

---

## 7. 使用流程

### 7.1 训练流程
1. 确保已安装依赖包：`pip install torch transformers datasets scikit-learn`
2. 准备ChnSentiCorp数据集，放置在 `code14/ChnSentiCorp/data/` 目录下
3. 运行训练脚本：`python bert-trainer.py`
4. 等待训练完成（观察控制台输出的训练进度和评估指标）
5. 训练完成后，模型自动保存到 `./sentiment_model` 目录

### 7.2 推理流程
1. 确保已完成训练，存在 `./sentiment_model` 目录
2. 运行推理脚本：`python bert-run.py`
3. 查看控制台输出的情感分析结果

---

## 8. 常见问题与解决方案

### 8.1 内存不足
**问题**：训练时出现OOM（Out Of Memory）错误  
**解决方案**：
- 减小 `per_device_train_batch_size`（如改为1）
- 减小 `max_length`（如改为64）
- 使用GPU训练

### 8.2 模型下载失败
**问题**：无法从HuggingFace下载bert-base-chinese  
**解决方案**：
- 配置国内镜像源
- 手动下载模型到本地，修改 `from_pretrained()` 参数为本地路径
- 设置环境变量：`setx HF_HOME "D:\huggingface"`

### 8.3 数据集加载失败
**问题**：找不到Parquet文件  
**解决方案**：
- 确认数据集路径正确
- 检查文件名是否与代码中一致
- 使用绝对路径代替相对路径

### 8.4 准确率低
**问题**：测试准确率低于80%  
**解决方案**：
- 增加训练轮数（num_train_epochs）
- 调整学习率（learning_rate）
- 检查数据清洗是否过度（去除标点可能影响语义）

---

## 9. 扩展功能建议

### 9.1 支持GPU加速
```python
# 在TrainingArguments中添加
training_args = TrainingArguments(
    ...
    fp16=True,  # 启用混合精度训练
)

# 在推理时修改device参数
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device=0)  # 0表示第一个GPU
```

### 9.2 添加早停机制
```python
training_args = TrainingArguments(
    ...
    load_best_model_at_end=True,
    metric_for_best_model="eval_accuracy",
    early_stopping_patience=3,  # 连续3个epoch无提升则停止
)
```

### 9.3 支持批量推理
```python
# 一次性对多个句子进行分类
results = classifier(test_sentences)
for i, (sentence, result) in enumerate(zip(test_sentences, results), 1):
    label_id = int(result['label'].split('_')[1])
    chinese_label = label_mapping[label_id]
    print(f"{i}. 文本: {sentence}")
    print(f"   预测: {chinese_label} (置信度: {result['score']:.4f})")
```

### 9.4 添加Web界面
可使用Streamlit或Gradio创建交互式情感分析Demo：
```python
import streamlit as st
from transformers import pipeline

st.title("中文情感分析系统")
text = st.text_input("请输入要分析的文本：")
if text:
    result = classifier(text)[0]
    st.write(f"情感：{result['label']}")
    st.write(f"置信度：{result['score']:.4f}")
```

---

## 10. 参考资料

1. HuggingFace Transformers官方文档：https://huggingface.co/docs/transformers
2. BERT论文：https://arxiv.org/abs/1810.04805
3. ChnSentiCorp数据集：https://huggingface.co/datasets/lansinuote/ChnSentiCorp
4. bert-base-chinese模型：https://huggingface.co/bert-base-chinese

---

## 附录：关键术语解释

- **BERT**：Bidirectional Encoder Representations from Transformers，双向编码器表示模型
- **Fine-tuning（微调）**：在预训练模型基础上，使用特定任务数据进行进一步训练
- **Tokenization（分词）**：将文本切分为模型可处理的token序列
- **Padding（填充）**：将短序列补充到统一长度
- **Truncation（截断）**：将长序列裁剪到最大长度
- **Epoch（轮次）**：完整遍历一次训练数据集
- **Batch Size（批次大小）**：每次梯度更新所使用的样本数量
- **Learning Rate（学习率）**：控制模型参数更新步长的超参数
- **Pipeline**：HuggingFace提供的高级API，简化模型推理流程
