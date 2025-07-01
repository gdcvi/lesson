"""
 * @author: zkyuan
 * @date: 2025/7/1 10:19
 * @description: 训练
"""
import torch
from torch import optim, nn

from nNet import Network
from torch.utils.data import DataLoader
from torchvision import transforms, datasets

# 数据加载
transform = transforms.Compose([transforms.Grayscale(num_output_channels=1), transforms.ToTensor()])

train_data = datasets.ImageFolder(root=r'E:\code\GitWork\gdcvi\lesson\lesson01\mnist_train',transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

# 在使用pytorch训练模型时，需要创建三个对象
# 自己设计的神经网络模型
model = Network()
# 优化器  Adam
optimezer = optim.Adam(model.parameters())
# 损失函数 分类模型
criterion = nn.CrossEntropyLoss()

# 开始训练，循环迭代
# 外层循环，代表了整个训练数据集的迭代次数
for epoch in range(10):
    # 内层循环，使用train_loader，进行小批量的数据读取
    for batch_idx, (data, label) in enumerate(train_loader):
        # 每循环一次，就会进行一次梯度下降算法。内层循环的五个步骤
        # pytorch框架训练的五个步骤
        # 1、计算神经网络的前向传播结果
        output = model(data)
        # 2、计算output和标签label之间的损失值
        loss = criterion(output, label)
        # 3、使用backward计算梯度
        loss.backward()
        # 4、更新参数
        optimezer.step()
        # 5、将梯度清零
        optimezer.zero_grad()

        # 每迭代100个，打印一次模型的损失loss，观察训练过程
        if batch_idx % 100 == 0:
            print("epoch:", epoch+1, "  batch:", batch_idx/len(train_loader), "  loss:", loss.item())

# 保存模型权重
torch.save(model.state_dict(), 'mnist.pt')