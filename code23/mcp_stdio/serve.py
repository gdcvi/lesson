import asyncio
import csv
import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("WeatherServer")

# OpenWeather API 配置
OPENWEATHER_API_BASE = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "YOUR_API_KEY"  # 请替换为你自己的 OpenWeather API Key
USER_AGENT = "weather-app/1.0"


def find_code(csv_file_path, district_name) -> str:
    """
    根据区域或者城市的名字，返回该区域的编码
    :param csv_file_path:
    :param district_name:
    :return: 城市编码
    """
    district_map = {}
    with open(csv_file_path, mode='r', encoding='utf-8') as f:
        # 读取csv文件内容
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            # districtcode、district表格列字段名
            district_code = row['districtcode'].strip()
            district = row['district'].strip()
            # 城市名做键、城市编码做值
            if district not in district_map:
                district_map[district] = district_code
    # 根据城市名拿到编码并返回
    return district_map.get(district_name, None)


def get_url(city: str) -> str:
    """获取天气调用的url"""
    district_code = find_code(r'E:\code\GitWork\python_study\py7\mcp_demo\mcp-serve\weather_district_id.csv', city)
    print(f"城市{city}的编码是: {district_code}")
    url = f'https://api.map.baidu.com/weather/v1/?district_id={district_code}&data_type=now&ak=gY1JIffsDTozewoC8Xeds77nPKcSlvPX'
    return url


async def fetch_weather(city: str) -> dict[str, Any] | None:
    """
    从 OpenWeather API 获取天气信息。
    :param city: 城市名称（需使用英文，如 Beijing）
    :return: 天气数据字典；若出错返回包含 error 信息的字典
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_cn"
    }
    headers = {"User-Agent": USER_AGENT}

    async with httpx.AsyncClient() as client:
        try:
            # response = await client.get(OPENWEATHER_API_BASE, params=params, headers=headers, timeout=30.0)
            url = get_url(city)  # 获取天气url
            response = await client.get(url)
            print(response.json())
            response.raise_for_status()
            return response.json()  # 返回字典类型
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP 错误: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"请求失败: {str(e)}"}


def format_weather(data: dict[str, Any] | str) -> str:
    """
    将天气数据格式化为易读文本。
    :param data: 天气数据（可以是字典或 JSON 字符串）
    :return: 格式化后的天气信息字符串
    """
    # 如果传入的是字符串，则先转换为字典
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            return f"无法解析天气数据: {e}"

    # 如果数据中包含错误信息，直接返回错误提示
    if "error" in data:
        return f"⚠️ {data['error']}"

    # 提取数据时做容错处理
    city = data.get("name", "未知")
    country = data.get("sys", {}).get("country", "未知")
    # temp = data.get("main", {}).get("temp", "N/A")
    humidity = data.get("main", {}).get("humidity", "N/A")
    wind_speed = data.get("wind", {}).get("speed", "N/A")
    # weather 可能为空列表，因此用 [0] 前先提供默认字典
    weather_list = data.get("weather", [{}])
    description = weather_list[0].get("description", "未知")

    # 解析数据
    text = data["result"]["now"]['text']  # 当前天气
    temp = data["result"]["now"]['temp']  # 当前温度
    feels_like = data["result"]["now"]['feels_like']  # 体感温度
    rh = data["result"]["now"]['rh']  # 相对湿度
    wind_dir = data["result"]["now"]['wind_dir']  # 风速
    wind_class = data["result"]["now"]['wind_class']  # 风向
    # prec_1h = data["result"]["now"]['prec_1h']  # 1小时累计降水量(mm)
    # clouds = data["result"]["now"]['clouds']  # 云量(%)
    # vis = data["result"]["now"]['vis']  # 能见度(m)
    # aqi = data["result"]["now"]['aqi']  # 空气质量指数数值
    # pm25 = data["result"]["now"]['pm25']  # pm2.5浓度(μg/m3)
    # pm10 = data["result"]["now"]['pm10']  # pm10浓度(μg/m3)
    # o3 = data["result"]["now"]['o3']  # 臭氧浓度(μg/m3)

    return (
        f"🌍 {city}, {country}\n"
        f"🌡 温度: {temp}°C\n"
        f"💧 湿度: {rh}%\n"
        f"🌬 风速: {wind_dir} m/s\n"
        f"🌤 天气: {description}\n"
        f"💨 风向: {wind_class} m/s\n"
        f"🌡 体感温度: {feels_like}°C\n"
        # f"💧 1小时累计降水量(mm): {prec_1h}%\n"
        # f"💧 云量(%): {clouds}%\n"
        # f"💧 能见度(m): {vis}%\n"
        # f"💧 空气质量指数数值: {aqi}%\n"
        # f"💧 pm2.5浓度(μg/m3): {pm25}%\n"
        # f"💧 pm10浓度(μg/m3): {pm10}%\n"
        # f"💧 臭氧浓度(μg/m3): {o3}%\n"
        f"📝 描述: {text}"
    )

@mcp.tool(name="query_weather")
async def query_weather(city: str) -> str:
    print(f"调用了query_weather工具，参数为：{city}")
    data = await fetch_weather(city)
    print(data)
    return format_weather(data)

async def query_weather_1(city: str) -> str:
    data = await fetch_weather(city)
    print(data)
    return format_weather(data)


async def main():
    """本地测试"""
    weather = await query_weather_1("北京")
    print(weather)


if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    # asyncio.run(main())
    mcp.run(transport='stdio')
