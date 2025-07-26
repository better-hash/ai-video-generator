#!/usr/bin/env python3
"""
检查AI模型下载状态
"""

import os
import sys
from pathlib import Path
import json

def check_model_downloads():
    """检查模型下载状态"""
    print("🔍 检查AI模型下载状态")
    print("=" * 50)
    
    # 获取缓存目录
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    
    if not cache_dir.exists():
        print("❌ 缓存目录不存在")
        return
    
    print(f"📁 缓存目录: {cache_dir}")
    
    # 检查各个模型
    models_to_check = [
        {
            "name": "Stable Video Diffusion",
            "path": "models--stabilityai--stable-video-diffusion-img2vid-xt",
            "expected_files": 9,
            "status": "❓"
        },
        {
            "name": "Stable Diffusion XL", 
            "path": "models--stabilityai--stable-diffusion-xl-base-1.0",
            "expected_files": 19,
            "status": "❓"
        },
        {
            "name": "SpeechT5",
            "path": "models--microsoft--speecht5_tts",
            "expected_files": 5,
            "status": "❓"
        }
    ]
    
    total_size = 0
    all_complete = True
    
    for model in models_to_check:
        model_path = cache_dir / model["path"]
        
        if model_path.exists():
            # 计算文件大小
            size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
            total_size += size
            
            # 检查文件数量
            files = list(model_path.rglob('*'))
            file_count = len([f for f in files if f.is_file()])
            
            if file_count >= model["expected_files"]:
                model["status"] = "✅"
                print(f"{model['status']} {model['name']}")
                print(f"   文件数: {file_count}/{model['expected_files']}")
                print(f"   大小: {size / (1024**3):.2f} GB")
            else:
                model["status"] = "⚠️"
                all_complete = False
                print(f"{model['status']} {model['name']} (部分下载)")
                print(f"   文件数: {file_count}/{model['expected_files']}")
                print(f"   大小: {size / (1024**3):.2f} GB")
        else:
            model["status"] = "❌"
            all_complete = False
            print(f"{model['status']} {model['name']} (未下载)")
    
    print(f"\n📊 总结:")
    print(f"   总大小: {total_size / (1024**3):.2f} GB")
    print(f"   状态: {'✅ 全部完成' if all_complete else '⚠️ 部分完成'}")
    
    return all_complete

def check_dependencies():
    """检查依赖库"""
    print("\n🔧 检查依赖库")
    print("=" * 30)
    
    dependencies = [
        ("torch", "PyTorch"),
        ("diffusers", "Diffusers"),
        ("transformers", "Transformers"),
        ("sentencepiece", "SentencePiece"),
        ("cv2", "OpenCV"),
        ("PIL", "Pillow")
    ]
    
    missing_deps = []
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (缺失)")
            missing_deps.append(module)
    
    if missing_deps:
        print(f"\n⚠️ 缺失依赖: {', '.join(missing_deps)}")
        print("安装命令:")
        for dep in missing_deps:
            print(f"   pip install {dep}")
    
    return len(missing_deps) == 0

def test_model_loading():
    """测试模型加载"""
    print("\n🧪 测试模型加载")
    print("=" * 30)
    
    try:
        import torch
        
        # 测试图像生成模型
        print("测试 Stable Diffusion XL...")
        from diffusers import StableDiffusionPipeline
        pipeline = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            safety_checker=None
        )
        print("✅ Stable Diffusion XL 加载成功")
        
        # 测试视频生成模型
        print("测试 Stable Video Diffusion...")
        from diffusers import StableVideoDiffusionPipeline
        svd_pipeline = StableVideoDiffusionPipeline.from_pretrained(
            "stabilityai/stable-video-diffusion-img2vid-xt",
            torch_dtype=torch.float16,
            variant="fp16"
        )
        print("✅ Stable Video Diffusion 加载成功")
        
        # 测试语音合成模型
        print("测试 SpeechT5...")
        from transformers import pipeline
        tts_pipeline = pipeline("text-to-speech", model="microsoft/speecht5_tts")
        print("✅ SpeechT5 加载成功")
        
        print("\n🎉 所有模型加载成功！")
        return True
        
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return False

def main():
    """主函数"""
    print("🔍 AI模型下载状态检查")
    print("=" * 60)
    
    # 检查下载状态
    downloads_ok = check_model_downloads()
    
    # 检查依赖
    deps_ok = check_dependencies()
    
    # 测试模型加载
    if downloads_ok and deps_ok:
        print("\n🚀 尝试加载模型...")
        models_ok = test_model_loading()
    else:
        models_ok = False
    
    # 总结
    print(f"\n📋 检查结果:")
    print(f"   下载状态: {'✅ 完成' if downloads_ok else '❌ 不完整'}")
    print(f"   依赖状态: {'✅ 完整' if deps_ok else '❌ 缺失'}")
    print(f"   模型加载: {'✅ 成功' if models_ok else '❌ 失败'}")
    
    if downloads_ok and deps_ok and models_ok:
        print("\n🎉 所有检查通过！可以正常使用AI功能。")
    else:
        print("\n⚠️ 需要修复一些问题才能正常使用AI功能。")
        print("建议使用简化模式进行测试。")

if __name__ == "__main__":
    main() 