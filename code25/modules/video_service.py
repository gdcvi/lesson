"""图生视频服务模块 —— 封装 DashScope VideoSynthesis API"""
import os
import time
import dashscope
from dashscope import VideoSynthesis
from config.settings import DASHSCOPE_API_KEY
from utils.file_utils import download_video, ensure_output_dir, get_timestamp_filename


class VideoService:
    """图生视频服务类"""

    def __init__(self):
        dashscope.api_key = DASHSCOPE_API_KEY

    def generate(self, img_url: str, prompt: str,
                 model: str = "wanx2.1-i2v-turbo",
                 duration: int = None) -> dict:
        """图生视频（异步，含轮询），返回 {"video_url": str, "local_path": str, "task_id": str}"""
        kwargs = {"model": model, "prompt": prompt, "img_url": img_url}
        if duration:
            kwargs["duration"] = duration

        result = VideoSynthesis.call(**kwargs)

        if result.status_code != 200:
            raise Exception(f"图生视频请求失败: status_code={result.status_code}, message={result.message}")

        task_status = getattr(result.output, 'task_status', None)
        task_id = getattr(result.output, 'task_id', None)

        if task_status == "PENDING" and task_id:
            result = VideoSynthesis.wait(task_id)

        if result.status_code != 200:
            raise Exception(f"图生视频最终失败: {result.message}")

        video_url = getattr(result.output, 'video_url', None)
        if not video_url:
            final_status = getattr(result.output, 'task_status', 'UNKNOWN')
            raise Exception(f"视频生成未成功，状态: {final_status}")

        output_dir = ensure_output_dir("videos")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        local_path = os.path.join(output_dir, f"i2v_{timestamp}.mp4")
        download_video(video_url, local_path)

        return {
            "video_url": video_url,
            "local_path": local_path,
            "task_id": task_id,
            "file_size": os.path.getsize(local_path),
        }

    def submit_task(self, img_url: str, prompt: str,
                    model: str = "wanx2.1-i2v-turbo",
                    duration: int = None) -> str:
        """提交异步任务，返回 task_id"""
        kwargs = {"model": model, "prompt": prompt, "img_url": img_url}
        if duration:
            kwargs["duration"] = duration

        result = VideoSynthesis.call(**kwargs)
        if result.status_code != 200:
            raise Exception(f"任务提交失败: {result.message}")

        return getattr(result.output, 'task_id', None)

    def wait_for_task(self, task_id: str) -> dict:
        """轮询等待任务完成并下载视频"""
        result = VideoSynthesis.wait(task_id)
        if result.status_code != 200:
            raise Exception(f"任务失败: {result.message}")

        video_url = getattr(result.output, 'video_url', None)
        if not video_url:
            raise Exception("未获取到视频URL")

        output_dir = ensure_output_dir("videos")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        local_path = os.path.join(output_dir, f"i2v_{timestamp}.mp4")
        download_video(video_url, local_path)

        return {
            "video_url": video_url,
            "local_path": local_path,
            "task_id": task_id,
            "file_size": os.path.getsize(local_path),
        }
