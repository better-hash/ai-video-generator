#!/usr/bin/env python3
"""
基础功能测试脚本
"""

import sys
import os
from pathlib import Path

def test_script_parser():
    """测试剧本解析功能"""
    print("🧪 测试剧本解析功能...")
    
    try:
        # 添加backend目录到Python路径
        sys.path.append(str(Path(__file__).parent / "backend"))
        
        from models.script_parser import ScriptParser
        
        # 测试剧本
        test_script = """
        浪漫晚餐
        
        场景：高级餐厅
        角色：小明（男，30岁，西装革履，成熟稳重）
        角色：小丽（女，28岁，优雅连衣裙，温柔美丽）
        
        小明：今晚的月亮真美。
        小丽：是啊，和你一起看更美。
        小明：你总是这么会说话。
        小丽：我只是说出心里话而已。
        """
        
        parser = ScriptParser()
        result = parser.parse_script(test_script)
        
        print(f"✅ 剧本标题: {result.title}")
        print(f"✅ 角色数量: {len(result.characters)}")
        print(f"✅ 场景数量: {len(result.scenes)}")
        print(f"✅ 对话数量: {len(result.dialogues)}")
        
        # 显示解析结果
        print("\n📝 解析结果:")
        for char in result.characters:
            print(f"  - 角色: {char.name} ({char.gender}, {char.age})")
        
        for scene in result.scenes:
            print(f"  - 场景: {scene.description}")
        
        for dialogue in result.dialogues:
            print(f"  - {dialogue.character}: {dialogue.content} ({dialogue.emotion})")
        
        return True
        
    except Exception as e:
        print(f"❌ 剧本解析测试失败: {e}")
        return False

def test_character_generator():
    """测试角色生成功能"""
    print("\n🧪 测试角色生成功能...")
    
    try:
        from models.character_generator import CharacterGenerator
        
        generator = CharacterGenerator()
        
        # 测试角色生成
        test_descriptions = [
            "小明（男，30岁，西装革履，成熟稳重）",
            "小丽（女，28岁，优雅连衣裙，温柔美丽）"
        ]
        
        for desc in test_descriptions:
            character = generator.generate_character(desc)
            print(f"✅ 生成角色: {character.name}")
            print(f"  描述: {character.description}")
            print(f"  图像路径: {character.image_path}")
            print(f"  语音模型: {character.voice_model}")
            print(f"  元数据: {character.metadata}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ 角色生成测试失败: {e}")
        return False

def test_basic_imports():
    """测试基本导入"""
    print("🧪 测试基本导入...")
    
    try:
        import fastapi
        print("✅ FastAPI 导入成功")
        
        import uvicorn
        print("✅ Uvicorn 导入成功")
        
        import pydantic
        print("✅ Pydantic 导入成功")
        
        import requests
        print("✅ Requests 导入成功")
        
        from PIL import Image
        print("✅ Pillow 导入成功")
        
        import numpy as np
        print("✅ NumPy 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def create_sample_data():
    """创建示例数据"""
    print("\n📁 创建示例数据...")
    
    try:
        # 创建数据目录
        data_dirs = ["data", "data/characters", "data/scenes", "data/videos"]
        for dir_path in data_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建目录: {dir_path}")
        
        # 创建示例剧本文件
        sample_script = """
# 示例剧本

标题：浪漫晚餐

场景：高级餐厅
时间：夜晚
氛围：浪漫温馨

角色：小明（男，30岁，西装革履，成熟稳重）
角色：小丽（女，28岁，优雅连衣裙，温柔美丽）

## 第一场

小明：（看着窗外的月亮）今晚的月亮真美。

小丽：（微笑）是啊，和你一起看更美。

小明：（深情地看着小丽）你总是这么会说话。

小丽：（害羞地低头）我只是说出心里话而已。

## 第二场

小明：（举起酒杯）为我们美好的时光干杯。

小丽：（举起酒杯）为我们美好的未来干杯。

小明：小丽，我想告诉你一件事。

小丽：什么事？

小明：我爱你。

小丽：（感动）我也爱你。
        """
        
        with open("data/sample_script.txt", "w", encoding="utf-8") as f:
            f.write(sample_script)
        print("✅ 创建示例剧本文件")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建示例数据失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🎬 AI视频生成工具 - 基础功能测试")
    print("=" * 50)
    
    # 测试基本导入
    if not test_basic_imports():
        print("\n❌ 基本导入测试失败，请检查依赖安装")
        return False
    
    # 创建示例数据
    if not create_sample_data():
        print("\n❌ 示例数据创建失败")
        return False
    
    # 测试剧本解析
    if not test_script_parser():
        print("\n❌ 剧本解析测试失败")
        return False
    
    # 测试角色生成
    if not test_character_generator():
        print("\n❌ 角色生成测试失败")
        return False
    
    print("\n🎉 所有基础功能测试通过！")
    print("\n📋 下一步:")
    print("1. 运行 'python start_project.py --backend' 启动后端服务")
    print("2. 访问 http://localhost:8000/docs 查看API文档")
    print("3. 运行 'python start_project.py --frontend' 启动前端服务")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 