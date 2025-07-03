"""
 * @author: zkyuan
 * @date: 2025/7/3 14:17
 * @description: 使用python代码拉取开源模型
"""
from modelscope import snapshot_download

model_dir = snapshot_download('Qwen/Qwen3-0.6B', cache_dir='D:/AI_Model')