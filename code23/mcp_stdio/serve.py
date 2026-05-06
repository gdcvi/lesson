# 导入所需的模块和库
import asyncio  # 异步编程支持
import csv  # CSV文件处理
import json  # JSON数据处理
import httpx  # 异步HTTP客户端库
from typing import Any  # 类型提示支持
from mcp.server.fastmcp import FastMCP  # MCP服务器框架

# 初始化 MCP 服务器实例，命名为"WeatherServer"
mcp = FastMCP("WeatherServer")

# OpenWeather API 配置信息（当前未使用，实际使用的是百度天气API）
OPENWEATHER_API_BASE = "https://api.openweathermap.org/data/2.5/weather"  # OpenWeather API基础URL
API_KEY = "YOUR_API_KEY"  # 请替换为你自己的 OpenWeather API Key（当前未使用）
USER_AGENT = "weather-app/1.0"  # HTTP请求的用户代理标识


def find_code(csv_file_path, district_name) -> str:
    """
    根据区域或者城市的名字，从CSV文件中查找并返回该区域的编码
    :param csv_file_path: CSV文件路径，包含城市名称和编码的映射关系
    :param district_name: 要查询的城市或区域名称
    :return: 城市编码，如果找不到则返回None
    """
    # 创建字典用于存储城市名到编码的映射关系
    district_map = {}
    
    # 以只读模式打开CSV文件，指定UTF-8编码以支持中文字符
    with open(csv_file_path, mode='r', encoding='utf-8') as f:
        # 使用DictReader读取CSV文件，将每行数据转换为字典格式
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            # 提取并清理每行中的城市编码和城市名称字段（去除首尾空格）
            # districtcode、district是CSV表格中的列字段名
            district_code = row['districtcode'].strip()
            district = row['district'].strip()
            
            # 建立城市名作为键、城市编码作为值的映射关系（避免重复覆盖）
            if district not in district_map:
                district_map[district] = district_code
    
    # 根据传入的城市名从映射字典中获取对应的编码并返回，找不到则返回None
    return district_map.get(district_name, None)


def get_url(city: str) -> str:
    """
    根据城市名称构建百度天气API的调用URL
    :param city: 城市名称（中文，如"北京"）
    :return: 完整的百度天气API调用URL地址
    """
    # 通过城市名称查找对应的行政区划编码（district_id）
    district_code = find_code(r'E:\code\GitWork\gdcvi\lesson\code23\mcp_stdio\weather_district_id.csv', city)
    print(f"城市{city}的编码是: {district_code}")
    
    # 构建百度天气API的完整URL，包含行政区划ID、数据类型（实时天气）和访问密钥（AK）
    url = f'https://api.map.baidu.com/weather/v1/?district_id={district_code}&data_type=now&ak=gY1JIffsD......PKcSlvPX'
    return url


async def fetch_weather(city: str) -> dict[str, Any] | None:
    """
    异步函数：从百度天气API获取指定城市的实时天气信息。
    :param city: 城市名称（支持中文，如"北京"）
    :return: 天气数据字典；若出错返回包含error信息的字典
    """
    # 构造OpenWeather API的请求参数（当前未使用，实际使用的是百度API）
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # 使用摄氏度单位
        "lang": "zh_cn"     # 返回中文结果
    }
    headers = {"User-Agent": USER_AGENT}  # 设置HTTP请求头

    # 创建异步HTTP客户端会话
    async with httpx.AsyncClient() as client:
        try:
            # 原OpenWeather API调用方式（已注释）
            # response = await client.get(OPENWEATHER_API_BASE, params=params, headers=headers, timeout=30.0)
            
            # 获取百度天气API的URL并发起GET请求
            url = get_url(city)  # 根据城市名获取天气API URL
            response = await client.get(url)
            print(response.json())  # 打印原始响应数据（调试用）
            response.raise_for_status()  # 检查HTTP状态码，如有错误则抛出异常
            return response.json()  # 解析JSON响应并返回字典类型数据
        except httpx.HTTPStatusError as e:
            # 捕获HTTP状态码错误（如404、500等）
            return {"error": f"HTTP 错误: {e.response.status_code}"}
        except Exception as e:
            # 捕获其他所有异常（网络错误、超时等）
            return {"error": f"请求失败: {str(e)}"}


def format_weather(data: dict[str, Any] | str) -> str:
    """
    将天气API返回的数据格式化为易于阅读的文本格式。
    :param data: 天气数据（可以是字典对象或JSON字符串）
    :return: 格式化后的天气信息字符串，包含温度、湿度、风速等信息
    """
    # 如果传入的是字符串类型，尝试将其解析为JSON字典
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            return f"无法解析天气数据: {e}"

    # 检查数据中是否包含错误信息，如果有则直接返回错误提示
    if "error" in data:
        return f"⚠️ {data['error']}"

    # 从百度天气API响应中提取各项天气数据，并进行容错处理（提供默认值）
    # 注意：这里保留了一些OpenWeather API的字段提取代码（已注释），实际使用的是百度API字段
    city = data.get("name", "未知")  # 城市名称（OpenWeather字段，实际未使用）
    country = data.get("sys", {}).get("country", "未知")  # 国家代码（OpenWeather字段，实际未使用）
    # temp = data.get("main", {}).get("temp", "N/A")  # 温度（OpenWeather字段，已废弃）
    humidity = data.get("main", {}).get("humidity", "N/A")  # 湿度（OpenWeather字段，实际未使用）
    wind_speed = data.get("wind", {}).get("speed", "N/A")  # 风速（OpenWeather字段，实际未使用）
    # weather 可能为空列表，因此用 [0] 前先提供默认字典（OpenWeather字段，实际未使用）
    weather_list = data.get("weather", [{}])
    description = weather_list[0].get("description", "未知")  # 天气描述（OpenWeather字段，实际未使用）

    # 从百度天气API的result.now字段中提取实时天气数据
    text = data["result"]["now"]['text']  # 当前天气现象描述（如：晴、多云等）
    temp = data["result"]["now"]['temp']  # 当前实际温度（摄氏度）
    feels_like = data["result"]["now"]['feels_like']  # 体感温度（摄氏度）
    rh = data["result"]["now"]['rh']  # 相对湿度（百分比）
    wind_dir = data["result"]["now"]['wind_dir']  # 风向（如：东北风）
    wind_class = data["result"]["now"]['wind_class']  # 风力等级（如：3级）
    # 以下字段已注释，可根据需要启用：
    # prec_1h = data["result"]["now"]['prec_1h']  # 1小时累计降水量(mm)
    # clouds = data["result"]["now"]['clouds']  # 云量(%)
    # vis = data["result"]["now"]['vis']  # 能见度(m)
    # aqi = data["result"]["now"]['aqi']  # 空气质量指数数值
    # pm25 = data["result"]["now"]['pm25']  # pm2.5浓度(μg/m3)
    # pm10 = data["result"]["now"]['pm10']  # pm10浓度(μg/m3)
    # o3 = data["result"]["now"]['o3']  # 臭氧浓度(μg/m3)

    # 构建格式化的天气信息字符串，使用emoji图标增强可读性
    return (
        f"🌍 {city}, {country}\n"  # 地理位置信息（当前显示"未知, 未知"，因为使用的是百度API）
        f"🌡 温度: {temp}°C\n"  # 实际温度
        f"💧 湿度: {rh}%\n"  # 相对湿度（注意：这里使用了百度API的rh字段）
        f"🌬 风速: {wind_dir} m/s\n"  # 风向（标签写的是风速，实际是风向）
        f"🌤 天气: {description}\n"  # 天气现象描述（来自OpenWeather字段，可能不准确）
        f"💨 风向: {wind_class} m/s\n"  # 风力等级（标签写的是风向，实际是风力）
        f"🌡 体感温度: {feels_like}°C\n"  # 体感温度
        # 以下扩展信息已注释，可根据需要启用：
        # f"💧 1小时累计降水量(mm): {prec_1h}%\n"
        # f"💧 云量(%): {clouds}%\n"
        # f"💧 能见度(m): {vis}%\n"
        # f"💧 空气质量指数数值: {aqi}%\n"
        # f"💧 pm2.5浓度(μg/m3): {pm25}%\n"
        # f"💧 pm10浓度(μg/m3): {pm10}%\n"
        # f"💧 臭氧浓度(μg/m3): {o3}%\n"
        f"📝 描述: {text}"  # 天气现象详细描述（来自百度API）
    )

@mcp.tool(name="query_weather")  # 将此函数注册为MCP工具，工具名为"query_weather"
async def query_weather(city: str) -> str:
    """
    MCP工具函数：查询指定城市的实时天气信息。
    此函数可被大模型通过Function Calling机制调用。
    :param city: 城市名称（支持中文，如"北京"）
    :return: 格式化后的天气信息字符串
    """
    print(f"调用了query_weather工具，参数为：{city}")  # 记录工具调用日志
    data = await fetch_weather(city)  # 异步调用天气数据获取函数
    print(data)  # 打印原始天气数据（调试用）
    return format_weather(data)  # 将天气数据格式化后返回

async def query_weather_1(city: str) -> str:
    """
    本地测试用的天气查询函数（非MCP工具）。
    与query_weather功能相同，但未注册为MCP工具，仅用于独立测试。
    :param city: 城市名称
    :return: 格式化后的天气信息字符串
    """
    data = await fetch_weather(city)  # 获取天气数据
    print(data)  # 打印原始数据（调试用）
    return format_weather(data)  # 返回格式化结果


async def main():
    """
    本地测试主函数：直接调用天气查询功能进行测试，不通过MCP协议。
    用于验证天气API调用和数据格式化是否正常工作。
    """
    # 查询北京的天气信息并打印结果
    weather = await query_weather_1("北京")
    print(weather)


if __name__ == "__main__":
    # 程序入口：以标准I/O（stdio）方式运行MCP服务器
    # 当被MCP客户端调用时，服务器将通过标准输入输出进行通信
    
    # 本地测试模式（已注释）：直接运行main函数测试天气查询功能
    # asyncio.run(main())
    
    # 正式运行模式：启动MCP服务器，等待客户端连接
    mcp.run(transport='stdio')  # 以stdio传输方式运行MCP服务器
