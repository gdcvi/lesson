"""
MCP 天气查询系统 - 快速测试脚本
用于验证服务器和客户端配置是否正确
"""
import asyncio
import sys
from serve import query_weather_1


async def test_weather_api():
    """测试天气 API 是否正常工作"""
    print("=" * 50)
    print("MCP 天气查询系统 - 功能测试")
    print("=" * 50)
    print()
    
    # 测试城市列表
    test_cities = ["北京", "上海", "广州", "深圳"]
    
    for city in test_cities:
        print(f"\n正在测试 {city} 的天气查询...")
        try:
            result = await query_weather_1(city)
            print(f"✅ {city} 查询成功！")
            print(f"返回结果预览: {result[:100]}...")
        except Exception as e:
            print(f"❌ {city} 查询失败: {str(e)}")
            return False
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！系统可以正常使用。")
    print("=" * 50)
    return True


def test_env_config():
    """测试环境变量配置"""
    print("\n检查环境变量配置...")
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("BASE_URL_DEEPSEEK")
        model = os.getenv("MODEL_DEEPSEEK")
        
        if api_key and base_url and model:
            print(f"✅ DEEPSEEK_API_KEY: 已配置 ({api_key[:10]}...)")
            print(f"✅ BASE_URL_DEEPSEEK: {base_url}")
            print(f"✅ MODEL_DEEPSEEK: {model}")
            return True
        else:
            print("❌ 环境变量配置不完整，请检查 .env 文件")
            return False
    except Exception as e:
        print(f"❌ 环境变量加载失败: {str(e)}")
        return False


def test_dependencies():
    """测试依赖库是否安装"""
    print("检查依赖库...")
    dependencies = [
        ("mcp", "MCP 协议库"),
        ("openai", "OpenAI SDK"),
        ("httpx", "HTTP 客户端"),
        ("dotenv", "环境变量管理"),
    ]
    
    all_installed = True
    for package, name in dependencies:
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"✅ {name} ({package}): 已安装")
        except ImportError:
            print(f"❌ {name} ({package}): 未安装")
            all_installed = False
    
    return all_installed


def main():
    """主测试函数"""
    print("\n开始系统测试...\n")
    
    # 测试 1: 依赖库
    print("[测试 1/3] 依赖库检查")
    if not test_dependencies():
        print("\n请先安装缺失的依赖库：")
        print("pip install mcp openai python-dotenv httpx")
        return
    
    # 测试 2: 环境变量
    print("\n[测试 2/3] 环境变量检查")
    if not test_env_config():
        print("\n请检查 .env 文件配置")
        return
    
    # 测试 3: 天气 API
    print("\n[测试 3/3] 天气 API 测试")
    asyncio.run(test_weather_api())
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)
    print("\n下一步：")
    print("1. 启动服务器: python serve.py")
    print("2. 启动客户端: python client.py serve.py")
    print("3. 或直接运行: start.bat")
    print()


if __name__ == "__main__":
    main()
