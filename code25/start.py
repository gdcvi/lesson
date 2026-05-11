"""
多模态AI智能助手 - 启动脚本

使用方法:
    python start.py              # 默认启动（端口 8501）
    python start.py --port 8080  # 指定端口
    python start.py --check      # 仅检查依赖，不启动
"""
import os
import sys
import subprocess
import argparse


def check_env():
    """检查环境配置"""
    print("=" * 50)
    print("🤖 多模态AI智能助手 - 环境检查")
    print("=" * 50)

    # 检查 Python 版本
    py_version = sys.version_info
    print(f"\n✅ Python 版本: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version < (3, 10):
        print("⚠️  建议使用 Python 3.10+")

    # 检查 .env 文件
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        print(f"✅ .env 文件存在: {env_path}")
    else:
        print(f"❌ .env 文件不存在: {env_path}")
        print("   请复制 .env.example 为 .env 并填入 API Key")
        return False

    # 检查 API Key
    from dotenv import load_dotenv
    load_dotenv(env_path)
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    if api_key:
        masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"✅ API Key 已配置: {masked}")
    else:
        print("❌ API Key 未配置")
        print("   请在 .env 文件中设置 DASHSCOPE_API_KEY")
        return False

    # 检查依赖包
    print("\n📦 检查依赖包...")
    required_packages = [
        ("streamlit", "streamlit"),
        ("langchain", "langchain"),
        ("langchain_openai", "langchain-openai"),
        ("langchain_chroma", "langchain-chroma"),
        ("chromadb", "chromadb"),
        ("dashscope", "dashscope"),
        ("dotenv", "python-dotenv"),
        ("pandas", "pandas"),
        ("requests", "requests"),
    ]

    missing = []
    for module_name, pip_name in required_packages:
        try:
            __import__(module_name)
            print(f"  ✅ {pip_name}")
        except ImportError:
            print(f"  ❌ {pip_name} (未安装)")
            missing.append(pip_name)

    if missing:
        print(f"\n⚠️  缺少 {len(missing)} 个依赖包，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        print("✅ 依赖安装完成")

    # 检查数据目录
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    sub_dirs = ["knowledge_bases", "temp_docs", "outputs/images", "outputs/videos", "outputs/audio", "cache"]
    for sub in sub_dirs:
        dir_path = os.path.join(data_dir, sub)
        os.makedirs(dir_path, exist_ok=True)
    print("✅ 数据目录结构正常")

    print("\n" + "=" * 50)
    print("✅ 环境检查通过！")
    print("=" * 50)
    return True


def start_app(port=8501):
    """启动 Streamlit 应用"""
    app_path = os.path.join(os.path.dirname(__file__), "app.py")

    print(f"\n🚀 正在启动多模态AI智能助手...")
    print(f"   端口: {port}")
    print(f"   地址: http://localhost:{port}")
    print(f"   按 Ctrl+C 停止服务\n")

    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.port", str(port),
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
        ], cwd=os.path.dirname(__file__))
    except KeyboardInterrupt:
        print("\n\n🛑 应用已停止")


def main():
    parser = argparse.ArgumentParser(description="多模态AI智能助手 - 启动脚本")
    parser.add_argument("--port", type=int, default=8501, help="端口号（默认 8501）")
    parser.add_argument("--check", action="store_true", help="仅检查环境，不启动应用")
    args = parser.parse_args()

    if args.check:
        check_env()
    else:
        if check_env():
            start_app(port=args.port)
        else:
            print("\n❌ 环境检查未通过，请修复后重试")
            sys.exit(1)


if __name__ == "__main__":
    main()
