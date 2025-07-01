"""
 * @author: zkyuan
 * @date: 2025/3/9 16:14
 * @description: 数据加载
"""
from torch.utils.data import DataLoader
from torchvision import transforms, datasets

if __name__ == '__main__':
    # 实现图像的预处理pipeline
    transform = transforms.Compose(
        [
            # 转换为单通道灰度图
            transforms.Grayscale(num_output_channels=1),
            # 转为张量
            transforms.ToTensor()
        ]
    )

    # 使用ImageFolder函数，读取数据文件夹，构建数据集dataset
    # 这个函数会将保存数据的文件的名字，作为数据的标签，组织数据。例如，名字为‘3’的文件里面的图片是3
    # 文件夹和图片配对，文件夹名作为label
    # 使用绝对路径
    train_data = datasets.ImageFolder(root=r'E:\code\GitWork\gdcvi\lesson\lesson01\mnist_train', transform=transform)
    test_data = datasets.ImageFolder(root=r'E:\code\GitWork\gdcvi\lesson\lesson01\mnist_test', transform=transform)
    # 打印他们
    print("train:", len(train_data), "\ntest", len(test_data))

    # 使用train_loader实现小批量的数据读取
    # batch_size = 64 每个批次包括64个数据
    train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
    # 打印train_loader
    print("train_loader:", len(train_loader))

    # 查看数据，循环遍历train_loader，每次能取出64个图像数据
    for batch_idx, (data, label) in enumerate(train_loader):
        if batch_idx == 3:
            break
        print("batch_idx:", batch_idx, "\ndata.shape:", data.shape, "\nlabel.shape:", label.shape, "\n", label)
