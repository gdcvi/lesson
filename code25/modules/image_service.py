"""文生图服务模块 —— 封装 DashScope ImageSynthesis API"""
import os
import time
import dashscope
from dashscope import ImageSynthesis
from config.settings import DASHSCOPE_API_KEY
from utils.file_utils import download_image, ensure_output_dir, get_timestamp_filename


class ImageService:
    """文生图服务类"""

    def __init__(self):
        dashscope.api_key = DASHSCOPE_API_KEY

    def generate(self, prompt: str, negative_prompt: str = None,
                 size: str = "1024*1024", n: int = 1,
                 model: str = "wan2.2-t2i-flash") -> list[dict]:
        """同步文生图，返回 [{"url": str, "local_path": str, "file_size": int}, ...]"""
        result = ImageSynthesis.call(
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            n=n,
            size=size,
        )

        if result.status_code != 200:
            raise Exception(f"文生图失败: status_code={result.status_code}, message={result.message}")

        output_dir = ensure_output_dir("images")
        images = []
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        for i, img in enumerate(result.output.results):
            local_path = os.path.join(output_dir, f"t2i_{timestamp}_{i}.png")
            success = download_image(img.url, local_path)
            images.append({
                "url": img.url,
                "local_path": local_path if success else None,
                "file_size": os.path.getsize(local_path) if success else 0,
            })
        return images

    def generate_async(self, prompt: str, size: str = "1024*1024",
                       model: str = "wanx-v1", n: int = 1) -> list[dict]:
        """异步文生图（含轮询等待）"""
        task_result = ImageSynthesis.async_call(
            model=model,
            prompt=prompt,
            n=n,
            size=size,
        )

        if task_result.status_code != 200:
            raise Exception(f"任务提交失败: {task_result.message}")

        task_id = task_result.output.task_id
        result = ImageSynthesis.wait(task_id)

        if result.status_code != 200:
            raise Exception(f"异步生成失败: {result.message}")

        output_dir = ensure_output_dir("images")
        images = []
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        for i, img in enumerate(result.output.results):
            local_path = os.path.join(output_dir, f"t2i_async_{timestamp}_{i}.png")
            success = download_image(img.url, local_path)
            images.append({
                "url": img.url,
                "local_path": local_path if success else None,
                "file_size": os.path.getsize(local_path) if success else 0,
            })
        return images
