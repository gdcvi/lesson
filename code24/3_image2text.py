"""
 * @author: zkyuan
 * @date: 2026/5/11
 * @description: 图生文模型 —— 使用 LangChain ChatOpenAI 调用Qwen视觉模型理解和描述图片
 * 使用 ChatOpenAI 调用 qwen-vl-plus / qwen-vl-max 视觉模型
 * 支持本地图片（base64编码）和网络图片URL两种输入方式
"""
import os
import base64
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


def create_vl_llm(model: str = "qwen-vl-plus"):
    """创建视觉模型 ChatOpenAI 实例"""
    return ChatOpenAI(
        model=model,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        max_tokens=1000,
    )


def encode_image_to_base64(image_path: str) -> str:
    """将本地图片文件编码为 base64 字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def image_to_text_by_url(image_url: str, question: str, model: str = "qwen-vl-plus"):
    """通过图片URL进行图生文 —— 传入公网可访问的图片地址"""
    print(f"\n模型: {model}")
    print(f"图片URL: {image_url[:80]}...")
    print(f"问题: {question}")
    print("正在分析图片...")

    llm = create_vl_llm(model)
    message = HumanMessage(
        content=[
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": question},
        ]
    )

    response = llm.invoke([message])

    print(f"回答: {response.content}")
    if "token_usage" in response.response_metadata:
        print(f"Token用量: {response.response_metadata['token_usage']}")
    return response.content


def image_to_text_by_local(local_path: str, question: str, model: str = "qwen-vl-plus"):
    """通过本地图片进行图生文 —— base64编码后传入"""
    print(f"\n模型: {model}")
    print(f"本地图片: {local_path}")
    print(f"问题: {question}")
    print("正在分析图片...")

    # 根据文件扩展名确定MIME类型
    ext = os.path.splitext(local_path)[1].lower()
    mime_map = {".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp", ".gif": "gif"}
    mime_type = mime_map.get(ext, "jpeg")

    img_b64 = encode_image_to_base64(local_path)

    llm = create_vl_llm(model)
    message = HumanMessage(
        content=[
            {"type": "image_url", "image_url": {"url": f"data:image/{mime_type};base64,{img_b64}"}},
            {"type": "text", "text": question},
        ]
    )

    response = llm.invoke([message])

    print(f"回答: {response.content}")
    if "token_usage" in response.response_metadata:
        print(f"Token用量: {response.response_metadata['token_usage']}")
    return response.content


def demo_url_image():
    """示例1：通过URL进行图片理解"""
    print("\n" + "=" * 50)
    print("【示例1】通过图片URL进行理解")
    print("=" * 50)

    image_to_text_by_url(
        image_url="https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
        question="请详细描述图片中的内容，包括人物、动物、场景和氛围",
        model="qwen-vl-plus",
    )


def demo_local_image():
    """示例2：通过本地图片文件进行理解"""
    print("\n" + "=" * 50)
    print("【示例2】通过本地图片进行理解")
    print("=" * 50)

    # 检查是否有之前生成的图片
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    local_images = []
    if os.path.exists(output_dir):
        local_images = [
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        ]

    if local_images:
        # 使用最新生成的图片
        local_images.sort(key=os.path.getmtime, reverse=True)
        image_to_text_by_local(
            local_path=local_images[0],
            question="请用三句话简短描述这张图片",
            model="qwen-vl-plus",
        )
    else:
        print("未找到本地图片文件，跳过此示例")
        print("提示: 先运行 2_text2image.py 生成图片，再运行本示例")


def demo_detailed_analysis():
    """示例3：使用 qwen-vl-max 进行更详细的分析"""
    print("\n" + "=" * 50)
    print("【示例3】详细视觉分析 (qwen-vl-max)")
    print("=" * 50)

    image_to_text_by_url(
        image_url="https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
        question="请分析这张图片：1.光线和色彩运用 2.构图特点 3.画面传达的情感",
        model="qwen-vl-max",
    )


def demo_ocr():
    """示例4：图片文字识别(OCR)"""
    print("\n" + "=" * 50)
    print("【示例4】图片文字识别 (OCR)")
    print("=" * 50)

    image_to_text_by_url(
        image_url="https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
        question="这张图片中有文字吗？如果有，请把所有文字提取出来。如果没有，请告诉我。",
        model="qwen-vl-plus",
    )


if __name__ == "__main__":
    demo_url_image()
    demo_local_image()
    demo_detailed_analysis()
    demo_ocr()

    print("\n" + "=" * 50)
    print("所有图生文示例演示完毕")
    print("=" * 50)

# 测试运行结果

"""
D:\Anaconda\envs\lesson\python.exe E:\code\GitWork\gdcvi\lesson\code24\3_image2text.py 

==================================================
【示例1】通过图片URL进行理解
==================================================

模型: qwen-vl-plus
图片URL: https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg...
问题: 请详细描述图片中的内容，包括人物、动物、场景和氛围
正在分析图片...
回答: 这张照片捕捉了一个温馨而宁静的瞬间，背景是海滩的日落场景。画面中，一位年轻女性和一只狗在沙滩上互动，营造出一种和谐与亲密的氛围。

### 人物描述：
- **女性**：她坐在沙滩上，面向大海，面带微笑，显得非常开心和放松。她的长发自然垂落，穿着一件蓝白相间的格子衬衫，袖子卷起，露出手腕上的白色手环。下身穿着深色裤子，赤脚坐在沙地上。
- **动作**：她伸出右手，与狗的前爪轻轻相触，仿佛在进行一场友好的“握手”。她的表情温柔，眼神中透露出对宠物的喜爱和满足。

### 动物描述：
- **狗**：这是一只金黄色的拉布拉多犬，体型中等，毛发光滑且富有光泽。它戴着一个彩色的胸背带，上面有图案装饰，看起来既时尚又舒适。狗的前爪抬起，稳稳地搭在女性的手上，表现出温顺和亲昵的态度。
- **姿态**：狗端坐在沙滩上，身体挺直，尾巴自然垂下，显得非常乖巧。它的目光似乎也注视着女性，显示出对她的信任和依赖。

### 场景描述：
- **沙滩**：沙滩细腻柔软，呈现出浅灰色的色调，上面有一些脚印和波浪留下的痕迹。阳光洒在沙地上，反射出柔和的光芒，增添了画面的温暖感。
- **大海**：背景是广阔的大海，海浪轻轻拍打着岸边，形成一层薄薄的水雾。远处的海平线与天空相接，显得辽阔而宁静。
- **天空**：天空明亮，呈现出淡淡的橙黄色和白色渐变，表明这是日落时分。阳光从画面右侧照射过来，给整个场景增添了一层金色的光辉。

### 氛围描述：
- **情感**：照片整体散发出一种温馨、幸福的情感。女性和狗之间的互动充满了爱意和默契，让人感受到人与动物之间深厚的情感纽带。
- **氛围**：画面的光线柔和，色彩温暖，给人一种平静、放松的感觉。日落时分的海滩景色更是为这个场景增添了一份浪漫和诗意。

### 总结：
这张照片通过细腻的构图和柔和的光线，成功地捕捉到了一个充满爱与和谐的瞬间。女性和狗在海滩上的互动，不仅展现了他们之间的亲密关系，也让观者感受到大自然的美好和生活的简单幸福。
Token用量: {'completion_tokens': 535, 'prompt_tokens': 1272, 'total_tokens': 1807, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None, 'text_tokens': 535}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 896}}

==================================================
【示例2】通过本地图片进行理解
==================================================

模型: qwen-vl-plus
本地图片: E:\code\GitWork\gdcvi\lesson\code24\output\text2img_20260511_113555_0.png
问题: 请用三句话简短描述这张图片
正在分析图片...
回答: 夜晚的都市雨景中，高楼大厦灯火辉煌，霓虹灯招牌闪烁着各种文字。街道上车辆疾驰，车灯留下长长的光轨，显得格外繁忙。一个人撑着黑色雨伞，背对着镜头，走在湿漉漉的人行道上，增添了一丝孤独与宁静的氛围。
Token用量: {'completion_tokens': 68, 'prompt_tokens': 899, 'total_tokens': 967, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None, 'text_tokens': 68}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}

==================================================
【示例3】详细视觉分析 (qwen-vl-max)
==================================================

模型: qwen-vl-max
图片URL: https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg...
问题: 请分析这张图片：1.光线和色彩运用 2.构图特点 3.画面传达的情感
正在分析图片...
回答: 这张图片展现了一位年轻女子与一只金毛犬在沙滩上互动的温馨场景，画面温暖而富有情感。以下从三个方面进行详细分析：

---

### 1. 光线和色彩运用

**光线：**
- 图片拍摄于日出或日落时分（黄金时刻），阳光从右侧斜射入画面，形成柔和的逆光效果。
- 光线温暖明亮，为人物和狗的轮廓勾勒出柔和的光晕，尤其是女子头发边缘和狗的毛发被照亮，增强了立体感和温暖氛围。
- 沙滩上的光影层次丰富，沙粒的纹理在低角度光照下清晰可见，增加了画面质感。

**色彩：**
- 整体色调偏暖，以橙黄色、米白和浅蓝为主，营造出宁静、安详的氛围。
- 天空呈现淡金色渐变至浅蓝，海水颜色柔和，与沙滩的白色相呼应。
- 女子穿着格子衬衫，其深色图案在暖光中显得沉稳而不突兀，狗的浅棕色毛发与背景和谐融合。
- 狗佩戴的彩色项圈成为画面中的小亮点，增添一丝活泼感。

---

### 2. 构图特点

- **主体位置：** 女子与狗位于画面中央偏右的位置，形成视觉焦点。两者面对面，动作对称且互动性强，构成稳定的三角形构图。
- **动态平衡：** 狗抬起前爪与女子击掌，动作自然流畅，形成一种“对话”般的互动，增强画面的生动性。
- **前景与背景：** 前景是细腻的沙滩纹理，中景是人与狗的互动，背景是平静的海面和朦胧的天空，层次分明。
- **留白处理：** 上方天空留白较多，避免画面压抑，同时突出人物与自然的和谐关系。
- **引导线：** 海浪的波纹和沙滩的痕迹形成自然的线条，将视线引向主体。

---

### 3. 画面传达的情感

- **亲密与陪伴：** 女子与狗之间的击掌动作充满默契与信任，展现出深厚的情感纽带，传递出人与宠物之间纯粹的爱与理解。
- **宁静与自由：** 海边的环境象征着放松与开阔，阳光洒下的温暖光芒让人感受到内心的平和与自由。
- **幸福与满足：** 女子的笑容真诚自然，眼神专注而温柔，反映出她此刻的快乐与满足。狗也表现出放松和愉悦的状态。
- **人与自然的和谐：** 整个画面没有人为的喧嚣，只有人、动物与自然的共处，体现了一种返璞归真、简单美好的生活哲学。

---

### 总结

这是一幅充满温情与诗意的画面，通过温暖的光线、和谐的构图和真挚的情感表达，成功地捕捉了人与宠物之间最动人的瞬间。它不仅展现了视觉美感，更唤起了观者对陪伴、自由与自然之美的共鸣。
Token用量: {'completion_tokens': 660, 'prompt_tokens': 1280, 'total_tokens': 1940, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None, 'text_tokens': 660}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0, 'image_tokens': 1249, 'text_tokens': 31}}

==================================================
【示例4】图片文字识别 (OCR)
==================================================

模型: qwen-vl-plus
图片URL: https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg...
问题: 这张图片中有文字吗？如果有，请把所有文字提取出来。如果没有，请告诉我。
正在分析图片...
回答: 这张图片中没有文字。图片展示了一位女士和一只狗在海滩上互动的场景，背景是海浪和夕阳。女士穿着格子衬衫，狗戴着彩色的牵引绳，两人正在握手。整个画面充满了温馨和愉快的氛围。
Token用量: {'completion_tokens': 55, 'prompt_tokens': 1275, 'total_tokens': 1330, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None, 'text_tokens': 55}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 896}}

==================================================
所有图生文示例演示完毕
==================================================

Process finished with exit code 0

"""