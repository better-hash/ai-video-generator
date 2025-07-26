#!/usr/bin/env python3
"""
AI视频生成工具 - 项目启动脚本
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 9):
        print("❌ 错误: 需要Python 3.9或更高版本")
        print(f"当前版本: {sys.version}")
        sys.exit(1)
    print(f"✅ Python版本检查通过: {sys.version}")

def check_dependencies():
    """检查依赖项"""
    required_packages = [
        "fastapi",
        "uvicorn", 
        "torch",
        "transformers",
        "diffusers",
        "Pillow",
        "numpy"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r backend/requirements.txt")
        return False
    
    print("✅ 所有依赖包检查通过")
    return True

def create_directories():
    """创建必要的目录"""
    directories = [
        "data",
        "data/characters", 
        "data/scenes",
        "data/videos",
        "data/temp",
        "logs",
        "frontend",
        "backend/models",
        "backend/database",
        "docs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def install_dependencies():
    """安装依赖"""
    print("📦 安装Python依赖...")
    try:
        # 首先尝试安装简化版本
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements_simple.txt"
        ], check=True)
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        print("💡 尝试分步安装...")
        try:
            # 分步安装核心依赖
            core_packages = [
                "fastapi", "uvicorn", "pydantic", "requests", "Pillow", "numpy"
            ]
            for package in core_packages:
                print(f"安装 {package}...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True)
            print("✅ 核心依赖安装完成")
        except subprocess.CalledProcessError as e2:
            print(f"❌ 分步安装也失败: {e2}")
            return False
    return True

def setup_frontend():
    """设置前端"""
    if not Path("frontend/package.json").exists():
        print("📦 初始化前端项目...")
        try:
            # 创建React项目
            subprocess.run([
                "npx", "create-react-app", "frontend", "--template", "typescript"
            ], check=True)
            print("✅ 前端项目创建完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 前端项目创建失败: {e}")
            return False
    else:
        print("✅ 前端项目已存在")
    
    return True

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "backend.main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 后端服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 后端服务启动失败: {e}")

def start_frontend():
    """启动前端服务"""
    print("🚀 启动前端服务...")
    try:
        os.chdir("frontend")
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 前端服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 前端服务启动失败: {e}")

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    try:
        # 运行剧本解析测试
        subprocess.run([
            sys.executable, "backend/models/script_parser.py"
        ], check=True)
        
        # 运行角色生成测试
        subprocess.run([
            sys.executable, "backend/models/character_generator.py"
        ], check=True)
        
        print("✅ 测试完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 测试失败: {e}")

def show_project_info():
    """显示项目信息"""
    print("""
🎬 AI视频生成工具 - 项目信息

📋 项目概述:
    这是一个基于AI技术的视频生成工具，能够根据剧本、人物形象描述
    和场地信息，自动生成具有真实演戏效果的视频内容。

🏗️ 技术架构:
    - 前端: React + TypeScript + Three.js
    - 后端: FastAPI + Redis + PostgreSQL  
    - AI模型: Stable Diffusion + ControlNet + SVD
    - 视频处理: FFmpeg + OpenCV + MoviePy

📁 项目结构:
    ├── frontend/          # React前端应用
    ├── backend/           # FastAPI后端服务
    ├── ai_models/         # AI模型集成
    ├── video_processing/  # 视频处理模块
    ├── data/              # 数据存储
    ├── docs/              # 文档
    └── scripts/           # 工具脚本

🚀 快速开始:
    1. 安装依赖: python start_project.py --install
    2. 启动后端: python start_project.py --backend
    3. 启动前端: python start_project.py --frontend
    4. 运行测试: python start_project.py --test

📖 更多信息:
    查看 docs/ 目录下的详细文档
    """)

def main():
    parser = argparse.ArgumentParser(description="AI视频生成工具启动脚本")
    parser.add_argument("--check", action="store_true", help="检查环境和依赖")
    parser.add_argument("--install", action="store_true", help="安装依赖")
    parser.add_argument("--setup", action="store_true", help="初始化项目")
    parser.add_argument("--backend", action="store_true", help="启动后端服务")
    parser.add_argument("--frontend", action="store_true", help="启动前端服务")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--info", action="store_true", help="显示项目信息")
    
    args = parser.parse_args()
    
    if args.info:
        show_project_info()
        return
    
    print("🎬 AI视频生成工具 - 项目启动脚本")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    if args.check:
        print("\n🔍 检查依赖...")
        check_dependencies()
        return
    
    if args.install:
        print("\n📦 安装依赖...")
        if not install_dependencies():
            sys.exit(1)
        return
    
    if args.setup:
        print("\n🏗️ 初始化项目...")
        create_directories()
        if not setup_frontend():
            sys.exit(1)
        print("✅ 项目初始化完成")
        return
    
    if args.test:
        print("\n🧪 运行测试...")
        run_tests()
        return
    
    if args.backend:
        start_backend()
        return
    
    if args.frontend:
        start_frontend()
        return
    
    # 默认行为：显示帮助信息
    if len(sys.argv) == 1:
        show_project_info()
        print("\n💡 使用 --help 查看所有可用选项")

if __name__ == "__main__":
    main() 