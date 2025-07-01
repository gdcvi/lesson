"""
 * @author: zkyuan
 * @date: 2025/7/1 10:18
 * @description: 图片数字识别神经网络
"""
import torch
from torch import nn


# 定义神经网络
class Network(nn.Module):
    def __init__(self):
        super().__init__()
        # 线性层1：输入层和隐藏层之间的线性层
        self.layer1 = nn.Linear(784, 256)
        # 线性层2：隐藏层和输出层之间的线性层
        self.layer2 = nn.Linear(256, 10)

    # 在前向传播 forward函数中，输入图像x
    def forward(self, x):
        # 使用view()函数，将x展平
        x = x.view(-1, 28 * 28)
        # 将x输入至layer1
        x = self.layer1(x)
        # 使用relu激活
        x = torch.relu(x)
        # 输入至layer2计算
        result = self.layer2(x)
        return result
        # 在使用CrossEntropyLoss损失函数时，会实现softmax的计算

