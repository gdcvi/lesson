"""
 * @author: zkyuan
 * @date: 2026/5/11
 * @description: 多模态混合使用 —— 综合运用多个模型完成复杂任务
 * 使用 LangChain ChatOpenAI 进行文本和视觉调用，DashScope SDK 进行图片/视频生成
 * 功能演示：
 *   1. 视频生文：使用 qwen-vl 视觉模型理解视频内容
 *   2. 图文链式调用：文本 -> 图片生成 -> 图片理解
 *   3. 多图对比分析：同时分析多张图片
 *   4. 图文混合：图片 + 文本多模态综合问答
"""
import os
import requests
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import dashscope
from dashscope import ImageSynthesis
from dotenv import load_dotenv

load_dotenv()

# LangChain ChatOpenAI 客户端（用于LLM文本和视觉模型）
SHARED_KWARGS = {
    "api_key": os.getenv("DASHSCOPE_API_KEY"),
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
}

# DashScope SDK（用于文生图等非对话API）
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==================== 1、视频生文 ====================

def video_to_text(video_url: str, question: str, model: str = "qwen-vl-max"):
    """视频理解：传入视频URL，让模型理解和描述视频内容"""
    print(f"\n模型: {model}")
    print(f"视频URL: {video_url[:80]}...")
    print(f"问题: {question}")
    print("正在分析视频（可能需要较长时间）...")

    llm = ChatOpenAI(model=model, max_tokens=1500, **SHARED_KWARGS)
    message = HumanMessage(
        content=[
            {"type": "video_url", "video_url": {"url": video_url}},
            {"type": "text", "text": question},
        ]
    )

    response = llm.invoke([message])

    print(f"\n分析结果:\n{response.content}")
    if "token_usage" in response.response_metadata:
        print(f"Token用量: {response.response_metadata['token_usage']}")
    return response.content


def video_to_text_by_frames(video_url: str, question: str, model: str = "qwen-vl-max"):
    """视频理解备用方案：当直接传视频URL不可用时"""
    print(f"\n(备用方案) 模型: {model}")
    print(f"视频URL: {video_url[:80]}...")
    print(f"问题: {question}")

    llm = ChatOpenAI(model=model, max_tokens=800, **SHARED_KWARGS)
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"请分析以下视频的URL: {video_url}\n问题: {question}\n\n"
                        f"如果你无法直接访问视频，请基于URL信息和你的知识给出分析建议。",
            }
        ]
    )

    response = llm.invoke([message])
    print(f"\n分析结果:\n{response.content}")


# ==================== 2、图文链式调用 ====================

def chain_text_to_image_to_text(topic: str):
    """链式调用：文本 -> 生成图片 -> 理解图片内容"""
    print("\n" + "-" * 40)
    print(f"链式任务: {topic}")
    print("-" * 40)

    # 步骤1：用 LLM 生成详细的图片描述 prompt
    print("\n[步骤1] 用LangChain ChatOpenAI生成图片描述prompt...")
    llm_text = ChatOpenAI(model="qwen-plus", max_tokens=200, **SHARED_KWARGS)
    messages = [
        SystemMessage(content="你是一个专业的图片描述生成器。根据用户主题，生成一段详细、适合AI文生图的英文prompt。只输出prompt本身，不要其他说明。"),
        HumanMessage(content=f"主题: {topic}"),
    ]
    response = llm_text.invoke(messages)
    image_prompt = response.content.strip()
    print(f"生成的Prompt: {image_prompt}")

    # 步骤2：调用文生图模型生成图片（DashScope SDK，非对话API）
    print("\n[步骤2] 调用文生图模型生成图片...")
    img_result = ImageSynthesis.call(
        model="wan2.2-t2i-flash",
        prompt=image_prompt,
        n=1,
        size="1024*1024",
    )

    if img_result.status_code != 200:
        print(f"图片生成失败: {img_result.message}")
        return

    image_url = img_result.output.results[0].url
    print(f"图片生成成功: {image_url[:60]}...")

    # 下载图片到本地
    try:
        img_data = requests.get(image_url, timeout=60).content
        img_path = os.path.join(OUTPUT_DIR, "chain_output.png")
        with open(img_path, "wb") as f:
            f.write(img_data)
        print(f"图片已保存: {img_path}")
    except Exception as e:
        print(f"图片下载失败: {e}")

    # 步骤3：调用视觉模型分析生成的图片
    print("\n[步骤3] 用LangChain ChatOpenAI视觉模型分析生成的图片...")
    llm_vision = ChatOpenAI(model="qwen-vl-plus", max_tokens=500, **SHARED_KWARGS)
    vision_message = HumanMessage(
        content=[
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": "请描述这张图片的内容，评估是否满足原始需求，并给出评分(1-10分)"},
        ]
    )

    eval_response = llm_vision.invoke([vision_message])
    print(f"\n图片评估结果:\n{eval_response.content}")


# ==================== 3、多图对比分析 ====================

def multi_image_compare(question: str, *image_urls):
    """多图对比：同时分析多张图片并对比"""
    print(f"\n问题: {question}")
    print(f"图片数量: {len(image_urls)}")

    # 构建多图片的 content 列表
    content_list = []
    for url in image_urls:
        content_list.append({"type": "image_url", "image_url": {"url": url}})
    content_list.append({"type": "text", "text": question})

    llm = ChatOpenAI(model="qwen-vl-max", max_tokens=1000, **SHARED_KWARGS)

    try:
        response = llm.invoke([HumanMessage(content=content_list)])
        print(f"\n分析结果:\n{response.content}")
    except Exception as e:
        print(f"多图同时分析失败: {e}")
        print("\n使用逐图分析 + LLM 汇总的备用方案...")

        # 备用方案：逐张分析后再由 LLM 汇总对比
        analyses = []
        for i, url in enumerate(image_urls):
            try:
                print(f"\n分析图片 {i + 1}...")
                single_llm = ChatOpenAI(model="qwen-vl-plus", max_tokens=400, **SHARED_KWARGS)
                single_msg = HumanMessage(content=[
                    {"type": "image_url", "image_url": {"url": url}},
                    {"type": "text", "text": f"请简要描述图片{i + 1}的内容、风格和色调"},
                ])
                resp = single_llm.invoke([single_msg])
                analyses.append(f"图片{i + 1}: {resp.content}")
            except Exception as e2:
                analyses.append(f"图片{i + 1}: 分析失败 ({e2})")

        # LLM 汇总
        summary_llm = ChatOpenAI(model="qwen-plus", max_tokens=600, **SHARED_KWARGS)
        summary_prompt = f"问题: {question}\n\n以下是各图片的分析:\n" + "\n\n".join(analyses)
        summary = summary_llm.invoke(summary_prompt)
        print(f"\n对比汇总:\n{summary.content}")


# ==================== 4、图文综合问答 ====================

def multimodal_qa(image_url: str, context: str, question: str):
    """多模态综合问答：结合图片和文本上下文进行推理回答"""
    print(f"\n上下文: {context}")
    print(f"问题: {question}")

    llm = ChatOpenAI(model="qwen-vl-max", max_tokens=800, **SHARED_KWARGS)
    message = HumanMessage(
        content=[
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": f"背景信息: {context}\n\n问题: {question}\n\n请结合图片和背景信息，给出综合回答。"},
        ]
    )

    response = llm.invoke([message])
    print(f"\n综合回答:\n{response.content}")


# ==================== 主函数 ====================

if __name__ == "__main__":
    # print("=" * 60)
    # print("多模态混合使用演示")
    # print("=" * 60)
    #
    # # --- 演示1：视频生文 ---
    # print("\n" + "=" * 50)
    # print("【演示1】视频生文 —— 视频内容理解")
    # print("=" * 50)
    #
    # sample_video_url = "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/video/robot.mp4"
    # try:
    #     video_to_text(
    #         video_url=sample_video_url,
    #         question="请详细描述这个视频的内容，包括场景、人物、动作和可能的情节",
    #         model="qwen-vl-max",
    #     )
    # except Exception as e:
    #     print(f"视频生文失败（可能视频URL不支持直接传入）: {e}")
    #     print("尝试备用方案...")
    #     video_to_text_by_frames(
    #         video_url=sample_video_url,
    #         question="请详细描述这个视频的内容",
    #     )
    #
    # # --- 演示2：图文链式调用 ---
    # print("\n" + "=" * 50)
    # print("【演示2】图文链式调用 —— 从文本到图片再到理解")
    # print("=" * 50)
    #
    # chain_text_to_image_to_text("一只戴着墨镜的柴犬在冲浪板上冲浪，卡通风格")

    # --- 演示3：多图对比分析 ---
    print("\n" + "=" * 50)
    print("【演示3】多图对比分析")
    print("=" * 50)

    multi_image_compare(
        "请对比分析这两张图片的摄影技巧,包括用光、构图、色彩搭配和情感表达的异同",
        "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
        "https://dashscope.oss-cn-beijing.aliyuncs.com/images/panda.jpeg",
    )

    # --- 演示4：图文综合问答 ---
    print("\n" + "=" * 50)
    print("【演示4】图文综合问答")
    print("=" * 50)

    multimodal_qa(
        image_url="https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
        context="这张照片是在一个公园里拍摄的，时间是秋天的下午，阳光温和。照片中的女孩叫小美，这是她第一次见到这只金毛犬。",
        question="根据图片和背景信息，分析小美和狗狗之间可能正在发生什么互动？描述他们的情感状态。",
    )

    print("\n" + "=" * 60)
    print("所有多模态混合使用示例演示完毕")
    print("=" * 60)

# 测试运行结果

"""
D:\Anaconda\envs\lesson\python.exe E:\code\GitWork\gdcvi\lesson\code24\7_multimodal_mix.py 
============================================================
多模态混合使用演示
============================================================

==================================================
【演示1】视频生文 —— 视频内容理解
==================================================

模型: qwen-vl-max
视频URL: https://dashscope.oss-cn-beijing.aliyuncs.com/samples/video/robot.mp4...
问题: 请详细描述这个视频的内容，包括场景、人物、动作和可能的情节
正在分析视频（可能需要较长时间）...
视频生文失败（可能视频URL不支持直接传入）: Error code: 400 - {'error': {'message': '<400> InternalError.Algo.InvalidParameter: Failed to download multimodal content', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_parameter_error'}, 'id': 'chatcmpl-be3f050a-aa2b-9b64-9c6a-c3a9b5fcf4b9', 'request_id': 'be3f050a-aa2b-9b64-9c6a-c3a9b5fcf4b9'}
尝试备用方案...

(备用方案) 模型: qwen-vl-max
视频URL: https://dashscope.oss-cn-beijing.aliyuncs.com/samples/video/robot.mp4...
问题: 请详细描述这个视频的内容

分析结果:
我目前无法直接访问或播放外部视频链接，包括您提供的 URL：`https://dashscope.oss-cn-beijing.aliyuncs.com/samples/video/robot.mp4`。因此，无法直接观看并描述该视频的具体内容。

不过，我可以基于以下几点为您提供分析建议和推测：

---

### 一、URL 分析

1. **域名与服务提供方**：
   - `dashscope.oss-cn-beijing.aliyuncs.com` 是阿里云（Alibaba Cloud）的 OSS（对象存储服务）域名。
   - “DashScope” 是阿里云推出的大模型服务平台，用于提供 AI 模型 API 接口，如通义千问、通义万相、通义听悟等。
   - 这意味着该视频很可能是由阿里云 DashScope 平台提供或用于演示其 AI 能力的示例素材。

2. **文件名**：
   - 文件名为 `robot.mp4`，表明这是一个 MP4 格式的视频，主题可能与“机器人”相关。

3. **路径结构**：
   - `/samples/video/robot.mp4` 表明这是平台的一个“样本”（sample）视频，通常用于展示功能或作为测试用例。

---

### 二、合理推测内容

结合上述信息，可以合理推测该视频的内容如下：

- **主题**：机器人技术或人工智能驱动的机器人行为展示。
- **可能场景**：
  - 一个机器人在执行任务（如搬运、行走、识别物体）。
  - 机器人与人类互动（如对话、协作）。
  - 展示 AI 控制下的机器人动作流畅性或智能决策能力。
  - 可能是某种服务机器人（如客服机器人、家庭助手、工业机器人）的演示。
- **用途**：
  - 用于展示 AI 视频理解、语音识别、动作生成等能力。
  - 或作为 AI 视频生成模型（如视频生成大模型）的输出样例。
  - 可能用于训练或验证 AI 模型对动态场景的理解。

---

### 三、如何进一步获取详细内容？

如果您希望获得更准确的视频内容描述，建议采取以下方式：

1. **本地下载并观看**：
   - 使用浏览器或下载工具（如 wget、curl）下载该视频：
     ```bash
     wget https://dashscope.oss-cn-beijing.aliyuncs.com/samples/video/robot.mp4
     ```
   - 然后使用播放器（如 VLC、PotPlayer）观看。

2. **使用视频分析工具**：
   - 使用视频分析软件提取关键帧、字幕、音频等信息。
   - 利用 AI 工具（如 OpenCV、MediaPipe、DeepLearning 模型）进行内容识别。

3. **调用 AI 视频理解 API**：
   - 如果您有 DashScope 或其他 AI 平台的权限，可上传视频至支持视频理解的 API（如通义千问视觉模型），获取自动描述。

4. **查看官方文档或示例说明**：
   - 查阅阿里云 DashScope 官方文档，看是否有关于该 sample video 的说明。

---

### 四、总结

虽然我无法直接观看该视频，但从 URL 和命名来看，`robot.mp4` 很可能是阿里云 DashScope 提供的一个用于展示 AI 与机器人交互或自动化控制的示例视频。内容可能涉及机器人运动、AI 控制、人机协作等场景。

如需精确描述，请自行下载并观看，或使用 AI 视频分析工具进行解析。

如果您有该视频的截图、文字描述或片段信息，我也可帮助进一步分析。

==================================================
【演示2】图文链式调用 —— 从文本到图片再到理解
==================================================

----------------------------------------
链式任务: 一只戴着墨镜的柴犬在冲浪板上冲浪，卡通风格
----------------------------------------

[步骤1] 用LangChain ChatOpenAI生成图片描述prompt...
生成的Prompt: A cartoon-style Shiba Inu dog wearing cool black sunglasses, standing confidently on a colorful surfboard riding a vibrant blue wave with white foam splashing, sunny beach background with palm trees and clear sky, bold outlines, playful and energetic atmosphere, high-detail whimsical illustration

[步骤2] 调用文生图模型生成图片...
图片生成成功: https://dashscope-5859.oss-cn-wulanchabu-acdr-1.aliyuncs.com...
图片已保存: E:\code\GitWork\gdcvi\lesson\code24\output\chain_output.png

[步骤3] 用LangChain ChatOpenAI视觉模型分析生成的图片...

图片评估结果:
### 图片描述

这是一幅卡通风格的插画，描绘了一只可爱的柴犬在冲浪的场景。画面整体色彩鲜艳，充满活力。

- **主体**：一只柴犬站在一块彩虹色的冲浪板上，冲浪板上有红、橙、黄、绿、蓝、紫等颜色的条纹。柴犬的表情自信且放松，戴着一副黑色的太阳镜，脖子上系着一条红色的印花围巾，围巾上有白色的星星图案。
  
- **背景**：背景是一片热带海滩，天空是明亮的蓝色，点缀着几朵白云。海浪汹涌，呈现出深浅不一的蓝色和白色泡沫，营造出动感的效果。右侧有几棵高大的椰子树，树叶茂盛，树干粗壮，树上还挂着几个椰子。沙滩是浅黄色的，与海水相接。

- **细节**：柴犬的毛发细节丰富，尾巴卷曲，四肢健壮，爪子清晰可见。冲浪板下方的水花飞溅，增加了画面的动感。整体构图平衡，色彩搭配和谐，给人一种轻松愉快的感觉。

### 评估

1. **创意性**：图片的创意非常独特，将柴犬与冲浪结合在一起，既有趣又富有想象力。评分：9/10
2. **色彩运用**：色彩鲜艳且搭配得当，尤其是冲浪板的彩虹色和背景的蓝色调，使画面非常吸引眼球。评分：9/10
3. **细节处理**：柴犬的毛发、太阳镜、围巾等细节都处理得非常细致，增加了画面的真实感和趣味性。评分：8/10
4. **构图**：构图合理，主体突出，背景与主体之间的关系协调，没有显得杂乱。评分：8/10
5. **情感表达**：画面传达出一种轻松、快乐的情感，让人感受到夏日海滩的惬意。评分：9/10

### 总体评分

综合以上各方面的评估，这张图片的整体质量非常高，能够很好地满足原始需求（即创作一幅有趣的卡通插画）。因此，我给这张图片的评分为：

**9/10**

### 原始需求满足情况

根据描述，这张图片完全满足了原始需求。它不仅展示了柴犬冲浪的场景，还通过丰富的色彩、细腻的细节和生动的构图，成功地传达了夏日海滩的欢乐氛围。无论是作为装饰画、海报设计，还是社交媒体分享，这张图片都能引起观众的兴趣和共鸣。

==================================================
【演示3】多图对比分析
==================================================

问题: 请对比分析这两张图片的摄影技巧,包括用光、构图、色彩搭配和情感表达的异同
图片数量: 2

分析结果:
这两张图片虽然主题不同——一张是人与狗在海滩上的互动，另一张是熊猫与乌鸦的趣味互动——但它们都展现了高水准的摄影技巧。以下从**用光、构图、色彩搭配和情感表达**四个方面进行对比分析：

---

### 一、用光

#### 图1（海滩人与狗）：
- **自然光运用**：采用的是日出或日落时的“黄金时刻”光线，阳光柔和，呈暖色调，从画面右侧斜射而来，形成逆光效果。
- **光影层次**：人物与狗的轮廓被勾勒出温暖的边缘光，沙滩上有细腻的明暗过渡，增强了空间感。
- **氛围营造**：光线营造出温馨、宁静、浪漫的氛围，突出了人与宠物之间亲密的情感。

#### 图2（熊猫与乌鸦）：
- **自然散射光**：拍摄于白天，光线较为均匀，属于阴天或树荫下的漫反射光，避免了强烈阴影。
- **细节清晰**：由于光线柔和，熊猫毛发的黑白纹理、乌鸦羽毛的光泽都清晰可见。
- **无明显方向性**：没有强烈的逆光或侧光，整体亮度均衡，适合展现动物的自然状态。

✅ **异同点**：
- **相同**：两幅图均使用自然光，且注重光线对主体的塑造。
- **不同**：图1强调**情绪化光线**（黄金时刻），图2更注重**真实记录**，追求自然状态下的清晰呈现。

---

### 二、构图

#### 图1：
- **对角线构图**：人与狗呈对角线分布，形成视觉引导，增强画面动感。
- **中心聚焦**：两人握手的动作成为视觉中心，突出互动主题。
- **留白处理**：上方天空大面积留白，使画面不拥挤，营造开阔感。
- **前景与背景**：沙滩为前景，海浪为中景，天空为远景，层次分明。

#### 图2（上下拼接图）：
- **分镜式构图**：采用上下两个画面拼接，形成“前因后果”的叙事结构。
- **水平构图**：每幅图均为横向构图，主体居中或偏右，平衡稳定。
- **互动焦点**：熊猫与乌鸦之间的距离和姿态形成视觉焦点，尤其第二幅图中两者几乎“面对面”，极具戏剧性。

✅ **异同点**：
- **相同**：都通过主体间的互动吸引视线，强调“关系”。
- **不同**：图1是**单幅完整构图**，图2是**双联叙事构图**，更具故事性。

---

### 三、色彩搭配

#### 图1：
- **主色调**：以暖黄色、米白色为主，沙滩与阳光融合成统一的暖调。
- **点缀色**：狗的彩色项圈和女子的格子衫为画面增添活力，但不喧宾夺主。
- **冷暖对比**：海水呈蓝灰色，与暖色沙滩形成冷暖对比，增强视觉层次。

#### 图2：
- **主色调**：黑白灰为主，熊猫的黑白毛色与乌鸦的黑色羽毛形成强烈对比。
- **背景色彩**：绿色植被和金属栏杆提供环境信息，但不抢眼，保持画面简洁。
- **色彩克制**：整体色彩低调，突出动物本身，强调自然与和谐。

✅ **异同点**：
- **相同**：都使用了**低饱和度+自然色系**，营造真实感。
- **不同**：图1色彩**温暖丰富**，图2色彩**冷静克制**，风格迥异。

---

### 四、情感表达

#### 图1：
- **情感基调**：温馨、愉悦、亲密。女子微笑，狗抬起前爪，像在“握手”，传递出人与宠物之间的信任与爱意。
- **人类视角**：强调人与动物的情感连接，带有“治愈系”摄影风格。
- **象征意义**：手与爪的接触象征平等与理解，具有一定的诗意。

#### 图2：
- **情感基调**：幽默、好奇、和谐。熊猫与乌鸦的互动看似“对话”，充满童趣与想象力。
- **动物视角**：捕捉到野生动物间罕见的“社交”瞬间，引发观者会心一笑。
- **象征意义**：不同物种间的和平共处，体现自然界的奇妙联系。

✅ **异同点**：
- **相同**：都表达了**跨物种的友好互动**，传递积极情感。
- **不同**：图1侧重**情感深度**（人与宠物的羁绊），图2侧重**趣味性与偶然性**（动物间的“社交”）。

---

### 总结对比表

| 维度       | 图1（海滩人与狗）                          | 图2（熊猫与乌鸦）                           |
|------------|------------------------------------------|--------------------------------------------|
| **用光**   | 黄金时刻逆光，暖调，情绪化                | 均匀漫射光，自然真实，细节清晰             |
| **构图**   | 对角线+中心聚焦，单幅完整构图            | 分镜式拼接，叙事性强，强调互动过程         |
| **色彩**   | 暖黄+蓝灰，冷暖对比，温馨明亮            | 黑白灰+绿植，低调克制，突出主体           |
| **情感**   | 温馨、亲密、治愈                          | 幽默、好奇、自然和谐                       |

---

### 结语

这两张照片虽风格迥异，却都体现了摄影者对**瞬间捕捉**和**情感传达**的敏锐感知。  
- 图1通过**光影与构图**营造出温暖的人宠关系；  
- 图2则凭借**真实互动与叙事结构**展现了自然界的奇妙瞬间。  

二者共同证明：优秀的摄影作品不仅在于技术，更在于能否触动人心。

==================================================
【演示4】图文综合问答
==================================================

上下文: 这张照片是在一个公园里拍摄的，时间是秋天的下午，阳光温和。照片中的女孩叫小美，这是她第一次见到这只金毛犬。
问题: 根据图片和背景信息，分析小美和狗狗之间可能正在发生什么互动？描述他们的情感状态。

综合回答:
根据图片内容与背景信息，尽管背景描述中提到“照片是在一个公园里拍摄的”，但图像实际显示的是海滩场景而非公园；此外，时间也更接近日落时分，而非一般意义上的“下午”。因此，我们应以图像内容为准，并结合背景信息进行合理推断。

从图像来看，小美正坐在沙滩上，面带微笑地与一只金毛犬互动。狗狗站立着前腿抬起，与小美的手相触，仿佛在“握手”或进行某种游戏动作。这种姿态通常表示友好、信任和积极的互动，是狗与人类建立联系的常见方式。

结合背景信息——这是小美第一次见到这只金毛犬——我们可以推测：他们之间正在发生一种初次见面的温馨互动。小美可能正在通过轻柔的动作（如握手）来与狗狗建立信任关系。她的笑容表明她感到愉悦和放松，而狗狗则表现出温顺和期待，说明它对这个新朋友充满善意。

情感状态方面：
- 小美显得开心、温暖且富有亲和力，她的眼神专注而温柔，显示出对狗狗的好奇与喜爱。
- 金毛犬则展现出友好、活泼的一面，它的身体语言开放，没有防御性姿态，反映出它愿意亲近人类。

虽然地点和时间略有出入，但这并不影响整体情感氛围的解读。画面捕捉了一个充满爱与和谐的瞬间，展现了人与动物之间纯粹的情感连接。这或许是一次难忘的初遇，也为未来的关系埋下了美好的伏笔。

============================================================
所有多模态混合使用示例演示完毕
============================================================

Process finished with exit code 0

"""