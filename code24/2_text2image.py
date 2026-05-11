"""
 * @author: zkyuan
 * @date: 2026/5/11
 * @description: 文生图模型 —— 通过文本描述生成图片
 * 使用 DashScope ImageSynthesis API，支持同步/异步两种调用方式
"""
import os
import time
import socket
import requests
import dashscope
from dashscope import ImageSynthesis
from dotenv import load_dotenv

load_dotenv()

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def check_network():
    """预检查网络连通性"""
    host = "dashscope.aliyuncs.com"
    print(f"正在检查网络连通性 ({host}:443)...")
    try:
        socket.getaddrinfo(host, 443)
        print("网络连通性检查通过")
        return True
    except socket.gaierror as e:
        print(f"DNS解析失败: {e}")
        print("请检查网络连接或 DNS 设置")
        return False


def download_image(url: str, save_path: str) -> bool:
    """从URL下载图片并保存到本地"""
    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(resp.content)
        file_size = os.path.getsize(save_path) / 1024
        print(f"图片已保存: {save_path} ({file_size:.1f}KB)")
        return True
    except Exception as e:
        print(f"下载图片失败: {e}")
        return False


def text_to_image(prompt: str, negative_prompt: str = None, size: str = "1024*1024"):
    """调用文生图模型生成图片（同步方式）"""
    print(f"\n提示词: {prompt}")
    if negative_prompt:
        print(f"负面提示词: {negative_prompt}")
    print(f"图片尺寸: {size}")
    print("正在生成图片，请稍候...")

    result = ImageSynthesis.call(
        model="wan2.2-t2i-flash",
        prompt=prompt,
        negative_prompt=negative_prompt,
        n=1,
        size=size,
    )

    if result.status_code == 200:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        for i, img in enumerate(result.output.results):
            print(f"\n生成成功!")
            print(f"图片URL: {img.url}")
            save_path = os.path.join(OUTPUT_DIR, f"text2img_{timestamp}_{i}.png")
            download_image(img.url, save_path)
    else:
        print(f"生成失败: status_code={result.status_code}")
        print(f"错误信息: {result.message}")


def text_to_image_async(prompt: str, size: str = "1024*1024"):
    """调用文生图模型生成图片（异步方式，适合长时间任务）"""
    print(f"\n提示词: {prompt}")
    print(f"图片尺寸: {size}")
    print("正在提交异步任务...")

    # 异步提交任务
    task_result = ImageSynthesis.async_call(
        model="wanx-v1",
        prompt=prompt,
        n=1,
        size=size,
    )

    if task_result.status_code != 200:
        print(f"任务提交失败: {task_result.message}")
        return

    task_id = task_result.output.task_id
    print(f"任务已提交, task_id: {task_id}")
    print("等待任务完成", end="", flush=True)

    # 轮询等待任务完成
    result = ImageSynthesis.wait(task_id)

    if result.status_code == 200:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        for i, img in enumerate(result.output.results):
            print(f"\n\n生成成功!")
            print(f"图片URL: {img.url}")
            save_path = os.path.join(OUTPUT_DIR, f"text2img_async_{timestamp}_{i}.png")
            download_image(img.url, save_path)
    else:
        print(f"\n生成失败: {result.message}")


def demo_single_image():
    """示例1：基础文生图 —— 简单的文字描述生成图片"""
    print("\n" + "=" * 50)
    print("【示例1】基础文生图")
    print("=" * 50)

    text_to_image(
        prompt="一只可爱的橘猫坐在窗台上，阳光透过窗户洒在它身上，窗外是蓝天白云",
        size="1024*1024",
    )


def demo_with_negative_prompt():
    """示例2：带负面提示词的文生图"""
    print("\n" + "=" * 50)
    print("【示例2】带负面提示词的文生图")
    print("=" * 50)

    text_to_image(
        prompt="一幅美丽的山水画，清澈的湖水，远处有青山，近处有桃花盛开",
        negative_prompt="blurry, distorted, low quality, watermark, text",
        size="1024*1024",
    )


def demo_portrait_style():
    """示例3：竖屏风格"""
    print("\n" + "=" * 50)
    print("【示例3】不同尺寸比例 —— 竖屏")
    print("=" * 50)

    text_to_image(
        prompt="一位古代侠客站在悬崖边，夕阳西下，风吹动他的披风，武侠电影海报风格",
        size="720*1280",
    )


def demo_landscape_style():
    """示例4：横屏宽图"""
    print("\n" + "=" * 50)
    print("【示例4】不同尺寸比例 —— 横屏")
    print("=" * 50)

    text_to_image(
        prompt="赛博朋克风格的城市夜景，霓虹灯闪烁，未来科技感，电影级画质",
        size="1280*720",
    )


if __name__ == "__main__":
    # 预检查网络
    if not check_network():
        print("\n网络不通，无法继续。请检查：")
        print("  1. 网络连接是否正常")
        print("  2. 是否需要配置代理 (HTTP_PROXY / HTTPS_PROXY)")
        print("  3. DNS 是否正常解析 dashscope.aliyuncs.com")
        exit(1)

    demo_single_image()
    demo_with_negative_prompt()
    demo_portrait_style()
    demo_landscape_style()

    print("\n" + "=" * 50)
    print("所有文生图示例演示完毕，图片保存在 output/ 目录")
    print("=" * 50)

# 测试运行结果
"""
D:\Anaconda\envs\lesson\python.exe E:\code\GitWork\gdcvi\lesson\code24\2_text2image.py 
正在检查网络连通性 (dashscope.aliyuncs.com:443)...
网络连通性检查通过

==================================================
【示例1】基础文生图
==================================================

提示词: 一只可爱的橘猫坐在窗台上，阳光透过窗户洒在它身上，窗外是蓝天白云
图片尺寸: 1024*1024
正在生成图片，请稍候...

生成成功!
图片URL: https://dashscope-5859.oss-cn-wulanchabu-acdr-1.aliyuncs.com/1d/9e/20260511/6514ac22/56e999e7-3f40-4b21-abc4-2357f78fbd3b201887464.png?Expires=1778556921&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=Pu04XClxwBVufFt2k53mfGeSMuY%3D
图片已保存: E:\code\GitWork\gdcvi\lesson\code24\output\text2img_20260511_113522_0.png (1044.3KB)

==================================================
【示例2】带负面提示词的文生图
==================================================

提示词: 一幅美丽的山水画，清澈的湖水，远处有青山，近处有桃花盛开
负面提示词: blurry, distorted, low quality, watermark, text
图片尺寸: 1024*1024
正在生成图片，请稍候...

生成成功!
图片URL: https://dashscope-5859.oss-cn-wulanchabu-acdr-1.aliyuncs.com/1d/55/20260511/6514ac22/ed3a0b83-a66e-4a8e-a0bd-0e182f42d8571473251330.png?Expires=1778556930&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=wlITjHUag%2BbBpQ24Nfn%2BrjRN%2F%2Fg%3D
图片已保存: E:\code\GitWork\gdcvi\lesson\code24\output\text2img_20260511_113532_0.png (1738.7KB)

==================================================
【示例3】不同尺寸比例 —— 竖屏
==================================================

提示词: 一位古代侠客站在悬崖边，夕阳西下，风吹动他的披风，武侠电影海报风格
图片尺寸: 720*1280
正在生成图片，请稍候...

生成成功!
图片URL: https://dashscope-5859.oss-cn-wulanchabu-acdr-1.aliyuncs.com/1d/cc/20260511/6514ac22/71ff54f7-f940-42f5-a1f2-126ed6b3dabc3201486910.png?Expires=1778556941&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=XxNq1nyMuAIYy5jnpENpbumC85g%3D
图片已保存: E:\code\GitWork\gdcvi\lesson\code24\output\text2img_20260511_113543_0.png (1026.0KB)

==================================================
【示例4】不同尺寸比例 —— 横屏
==================================================

提示词: 赛博朋克风格的城市夜景，霓虹灯闪烁，未来科技感，电影级画质
图片尺寸: 1280*720
正在生成图片，请稍候...

生成成功!
图片URL: https://dashscope-5859.oss-cn-wulanchabu-acdr-1.aliyuncs.com/1d/28/20260511/6514ac22/6148cdfc-2869-4299-9d60-a44b4d70c455364433082.png?Expires=1778556951&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=krlAT5k2aXO7hJDJRmkKEekMCeY%3D
图片已保存: E:\code\GitWork\gdcvi\lesson\code24\output\text2img_20260511_113555_0.png (1318.0KB)

==================================================
所有文生图示例演示完毕，图片保存在 output/ 目录
==================================================

Process finished with exit code 0

"""