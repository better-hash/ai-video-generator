#!/usr/bin/env python3
"""
Stable Diffusion XL 图像生成模型测试程序
"""

import os
import torch
from PIL import Image
from datetime import datetime

def test_stable_diffusion_xl():
    """测试 Stable Diffusion XL 模型"""
    print("🎨 测试 Stable Diffusion XL 图像生成模型")
    print("=" * 50)
    
    try:
        # 检查CUDA可用性
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"📱 使用设备: {device}")
        
        # 导入模型
        from diffusers import StableDiffusionXLPipeline
        
        print("🔄 正在加载 Stable Diffusion XL 模型...")
        pipeline = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            variant="fp16" if device == "cuda" else None,
            use_safetensors=True
        )
        
        if device == "cuda":
            pipeline = pipeline.to("cuda")
        
        print("✅ 模型加载成功")
        
        # 测试提示词
        test_prompts = [
            "a professional portrait of a young businessman in a suit, high quality, detailed",
            "a beautiful woman with long hair, elegant dress, studio lighting",
            "an elderly man with glasses, wise expression, warm lighting",
            "a modern office scene with computers and plants, bright lighting"
        ]
        
        # 创建输出目录
        output_dir = "data/test_outputs/sdxl"
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成图像
        for i, prompt in enumerate(test_prompts):
            print(f"\n🎯 测试 {i+1}/{len(test_prompts)}: {prompt[:50]}...")
            
            try:
                # 生成图像
                with torch.no_grad():
                    image = pipeline(
                        prompt=prompt,
                        num_inference_steps=20,
                        guidance_scale=7.5,
                        width=1024,
                        height=1024
                    ).images[0]
                
                # 保存图像
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sdxl_test_{i+1}_{timestamp}.png"
                filepath = os.path.join(output_dir, filename)
                image.save(filepath)
                
                print(f"✅ 图像生成成功: {filepath}")
                print(f"   分辨率: {image.size}")
                
            except Exception as e:
                print(f"❌ 图像生成失败: {e}")
        
        print(f"\n🎉 Stable Diffusion XL 测试完成")
        print(f"📁 输出目录: {output_dir}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请安装必要的依赖: pip install diffusers torch")
        return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_model_info():
    """显示模型信息"""
    print("\n📋 Stable Diffusion XL 模型信息")
    print("-" * 30)
    print("模型名称: stabilityai/stable-diffusion-xl-base-1.0")
    print("功能: 文本到图像生成")
    print("分辨率: 1024x1024")
    print("推荐步数: 20-50")
    print("引导比例: 7.5")
    print("内存需求: 6-8GB VRAM (GPU) / 16GB RAM (CPU)")

if __name__ == "__main__":
    test_model_info()
    success = test_stable_diffusion_xl()
    
    if success:
        print("\n🎊 所有测试通过！")
    else:
        print("\n⚠️ 测试失败，请检查环境配置")