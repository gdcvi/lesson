"""
 * @author: zkyuan
 * @date: 2026/5/11
 * @description: 图生视频模型 —— 通过一张静态图片 + 文字描述生成动态视频
 * 使用 DashScope VideoSynthesis API，调用 wanx2.1-i2v-turbo / wanx2.1-i2v-plus 模型
"""
import os
import time
import requests
import dashscope
from dashscope import VideoSynthesis
from dotenv import load_dotenv

load_dotenv()

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_video(url: str, save_path: str) -> bool:
    """从URL下载视频并保存到本地"""
    try:
        print(f"正在下载视频...")
        resp = requests.get(url, timeout=300)
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(resp.content)
        file_size = os.path.getsize(save_path) / (1024 * 1024)
        print(f"视频已保存: {save_path} ({file_size:.1f}MB)")
        return True
    except Exception as e:
        print(f"下载视频失败: {e}")
        return False


def image_to_video(img_url: str, prompt: str, model: str = "wanx2.1-i2v-turbo", duration: int = None):
    """调用图生视频模型"""
    print(f"\n模型: {model}")
    print(f"图片URL: {img_url[:80]}...")
    print(f"动作描述: {prompt}")
    if duration:
        print(f"视频时长: {duration}秒")
    print("正在生成视频（可能需要几分钟），请耐心等待...")

    kwargs = {
        "model": model,
        "prompt": prompt,
        "img_url": img_url,
    }
    if duration:
        kwargs["duration"] = duration

    result = VideoSynthesis.call(**kwargs)

    if result.status_code == 200:
        task_status = getattr(result.output, 'task_status', None)
        task_id = getattr(result.output, 'task_id', None)

        # 如果任务是 PENDING 状态，需要轮询等待
        if task_status == "PENDING" and task_id:
            print(f"任务处理中 (task_id: {task_id})")
            print("等待任务完成", end="", flush=True)
            result = VideoSynthesis.wait(task_id)

        if result.status_code == 200:
            video_url = getattr(result.output, 'video_url', None)
            if video_url:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                print(f"\n生成成功!")
                print(f"视频URL: {video_url}")
                save_path = os.path.join(OUTPUT_DIR, f"img2video_{timestamp}.mp4")
                download_video(video_url, save_path)
            else:
                # 检查 task_status
                final_status = getattr(result.output, 'task_status', 'UNKNOWN')
                print(f"\n任务状态: {final_status}")
                if final_status != "SUCCEEDED":
                    print(f"视频生成未成功，状态: {final_status}")
        else:
            print(f"最终结果获取失败: {result.message}")
    else:
        print(f"生成失败: status_code={result.status_code}")
        print(f"错误信息: {result.message}")


def demo_basic_img2video():
    """示例1：基础图生视频"""
    print("\n" + "=" * 50)
    print("【示例1】基础图生视频")
    print("=" * 50)

    image_to_video(
        img_url="https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
        prompt="狗开心地摇着尾巴，女孩伸手去摸狗。",
        model="wanx2.1-i2v-turbo",
    )


def demo_static_to_dynamic():
    """示例2：静态风景图转动态视频"""
    print("\n" + "=" * 50)
    print("【示例2】风景静态转动态")
    print("=" * 50)

    image_to_video(
        img_url="https://dashscope.oss-cn-beijing.aliyuncs.com/images/watercolor.jpeg",
        prompt="微风轻拂树梢，湖面水面泛起涟漪，云朵缓缓飘过天空。",
        model="wanx2.1-i2v-turbo",
    )


def demo_high_quality():
    """示例3：使用高质量模型 wanx2.1-i2v-plus"""
    print("\n" + "=" * 50)
    print("【示例3】高质量图生视频 (wanx2.1-i2v-plus)")
    print("=" * 50)

    image_to_video(
        img_url="https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
        prompt="狗好奇地歪着头，耳朵竖起，女孩微笑着轻轻挠着狗的耳后。",
        model="wanx2.1-i2v-plus",
    )


if __name__ == "__main__":
    # 注意：图生视频耗时较长，按需运行
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "all":
        demo_basic_img2video()
        demo_static_to_dynamic()
        demo_high_quality()
    else:
        print("图生视频耗时较长，默认只运行基础示例")
        print("如需运行全部示例，使用: python 4_image2video.py all")
        print()
        demo_basic_img2video()

    print("\n" + "=" * 50)
    print("图生视频示例演示完毕，视频保存在 output/ 目录")
    print("=" * 50)

# 测试运行结果

"""
D:\Anaconda\envs\lesson\python.exe E:\code\GitWork\gdcvi\lesson\code24\4_image2video.py 
图生视频耗时较长，默认只运行基础示例
如需运行全部示例，使用: python 4_image2video.py all


==================================================
【示例1】基础图生视频
==================================================

模型: wanx2.1-i2v-turbo
图片URL: https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg...
动作描述: 狗开心地摇着尾巴，女孩伸手去摸狗。
正在生成视频（可能需要几分钟），请耐心等待...

生成成功!
视频URL: https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/1d/56/20260511/a0f45588/b7328636-761f-48e7-ba61-b5e8922b397b.mp4?Expires=1778570211&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=X5nX9dQx3PlBhW0LakiG0DCL%2BVM%3D
正在下载视频...
视频已保存: E:\code\GitWork\gdcvi\lesson\code24\output\img2video_20260511_151654.mp4 (2.4MB)

==================================================
图生视频示例演示完毕，视频保存在 output/ 目录
==================================================

Process finished with exit code 0

"""