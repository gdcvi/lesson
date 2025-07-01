"""
 * @author: zkyuan
 * @date: 2025/7/1 10:19
 * @description: 测试训练结果
"""
from nNet import Network
from torchvision import transforms
from torchvision import datasets
import torch

if __name__ == '__main__':
    # 读取测试数据集
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor()
    ])
    test_data = datasets.ImageFolder(root=r'E:\code\GitWork\gdcvi\lesson\lesson01\mnist_test', transform=transform)
    print("test_dataset length: ", len(test_data))

    # 定义模型
    model = Network()
    # 加载模型训练后的权重
    model.load_state_dict(torch.load('mnist.pt'))
    # 正确识别的数量
    right = 0

    for i, (x, y) in enumerate(test_data):
        # 将其中的数据x输入到模型
        output = model(x.unsqueeze(0))
        # 选择概率最大的标签作为预测结果
        predict = output.argmax(1).item()
        # 比较预测结果和真实标签y
        if predict == y:
            right += 1
        else:
            # 将识别错误的样例打印出来
            img_path = test_data.samples[i][0]
            print(f"wrong case: predict = {predict} actual = {y} img_path = {img_path}")

    # 计算测试结果
    sample_num = len(test_data)
    acc = right * 1.0 / sample_num
    print("正确数：", right, "错误数：", 10000-right)
    print("准确率 = %d / %d = %.31f" % (right, sample_num, acc))
