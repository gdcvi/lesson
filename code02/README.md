# lesson1

## 安装依赖

```shell
pip install openai

pip install packaging
pip install modelscope

pip install transformers
pip install accelerate
```
## 下载模型
- 使用命令
```shell
# 下载模型
modelscope download --model Qwen/Qwen3-0.6B
# 下载单个文件
modelscope download --model Qwen/Qwen3-0.6B README.md --local_dir ./dir
# 下载模型到指定位置
modelscope download --model Qwen/Qwen3-0.6B --local_dir D:/AI_Model/Qwen/Qwen3-0.6B
```
- 使用代码
```python
#模型下载
from modelscope import snapshot_download

model_dir = snapshot_download('Qwen/Qwen3-0.6B', cache_dir='D:/AI_Model')

```
