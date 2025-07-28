#!/usr/bin/env python3
"""
快速模型测试程序 - 仅验证模型加载，不进行实际生成
"""

import os
import torch
from datetime import datetime

def quick_test_stable_diffusion_xl():
    """快速测试 Stable Diffusion XL 模型加载"""
    print("🎨 快速测试 Stable Diffusion XL")
    print("-" * 40)
    
    try:
        from diffusers import StableDiffusionXLPipeline
        
        print("🔄 加载模型...")
        pipeline = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            variant="fp16" if torch.cuda.is_available() else None,
            use_safetensors=True
        )
        
        if torch.cuda.is_available():
            pipeline = pipeline.to("cuda")
            print("✅ 模型已加载到GPU")
        else:
            print("✅ 模型已加载到CPU")
        
        # 检查模型组件
        print(f"   UNet: {type(pipeline.unet).__name__}")
        print(f"   VAE: {type(pipeline.vae).__name__}")
        print(f"   文本编码器: {type(pipeline.text_encoder).__name__}")
        
        # 清理内存
        del pipeline
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        return True
        
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return False

def quick_test_stable_video_diffusion():
    """快速测试 Stable Video Diffusion 模型加载"""
    print("\n🎬 快速测试 Stable Video Diffusion")
    print("-" * 40)
    
    try:
        from diffusers import StableVideoDiffusionPipeline
        
        print("🔄 加载模型...")
        pipeline = StableVideoDiffusionPipeline.from_pretrained(
            "stabilityai/stable-video-diffusion-img2vid-xt",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            variant="fp16" if torch.cuda.is_available() else None
        )
        
        if torch.cuda.is_available():
            pipeline = pipeline.to("cuda")
            print("✅ 模型已加载到GPU")
        else:
            print("✅ 模型已加载到CPU")
        
        # 检查模型组件
        print(f"   UNet: {type(pipeline.unet).__name__}")
        print(f"   VAE: {type(pipeline.vae).__name__}")
        print(f"   图像编码器: {type(pipeline.image_encoder).__name__}")
        
        # 清理内存
        del pipeline
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        return True
        
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return False

def quick_test_speecht5():
    """快速测试 SpeechT5 模型加载"""
    print("\n🎤 快速测试 SpeechT5")
    print("-" * 40)
    
    try:
        from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
        
        print("🔄 加载处理器...")
        processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        print("✅ 处理器加载成功")
        
        print("🔄 加载TTS模型...")
        model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        print("✅ TTS模型加载成功")
        
        print("🔄 加载声码器...")
        vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        print("✅ 声码器加载成功")
        
        if torch.cuda.is_available():
            model = model.to("cuda")
            vocoder = vocoder.to("cuda")
            print("✅ 模型已移动到GPU")
        else:
            print("✅ 模型在CPU上运行")
        
        # 检查模型配置
        print(f"   词汇表大小: {model.config.vocab_size}")
        print(f"   隐藏层大小: {model.config.hidden_size}")
        
        # 清理内存
        del processor, model, vocoder
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        return True
        
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return False

def check_gpu_memory():
    """检查GPU内存使用情况"""
    if torch.cuda.is_available():
        print("\n🚀 GPU内存信息")
        print("-" * 40)
        
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            allocated = torch.cuda.memory_allocated(i) / 1024**3
            cached = torch.cuda.memory_reserved(i) / 1024**3
            total = props.total_memory / 1024**3
            
            print(f"GPU {i}: {props.name}")
            print(f"   总内存: {total:.1f} GB")
            print(f"   已分配: {allocated:.1f} GB")
            print(f"   已缓存: {cached:.1f} GB")
            print(f"   可用: {total - cached:.1f} GB")
    else:
        print("\n⚠️ 未检测到CUDA GPU")

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能")
    print("-" * 40)
    
    try:
        # 测试torch基本操作
        print("🔄 测试PyTorch基本操作...")
        x = torch.randn(2, 3)
        y = torch.randn(3, 4)
        z = torch.mm(x, y)
        print(f"✅ 矩阵运算: {z.shape}")
        
        # 测试CUDA操作（如果可用）
        if torch.cuda.is_available():
            print("🔄 测试CUDA操作...")
            x_cuda = x.cuda()
            y_cuda = y.cuda()
            z_cuda = torch.mm(x_cuda, y_cuda)
            print(f"✅ CUDA矩阵运算: {z_cuda.shape}")
        
        # 测试图像处理
        print("🔄 测试图像处理...")
        from PIL import Image
        import numpy as np
        
        # 创建测试图像
        img_array = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        print(f"✅ 图像创建: {img.size}")
        
        # 测试音频处理
        print("🔄 测试音频处理...")
        audio_data = np.random.randn(16000)  # 1秒的音频
        print(f"✅ 音频数据: {audio_data.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ 基本功能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("⚡ AI模型快速测试")
    print("=" * 60)
    
    start_time = datetime.now()
    
    # 检查系统信息
    print(f"🐍 Python版本: {torch.__version__}")
    print(f"🔥 PyTorch版本: {torch.__version__}")
    print(f"🚀 CUDA可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   CUDA版本: {torch.version.cuda}")
        print(f"   GPU数量: {torch.cuda.device_count()}")
    
    # 检查GPU内存
    check_gpu_memory()
    
    # 测试基本功能
    basic_ok = test_basic_functionality()
    
    if not basic_ok:
        print("\n❌ 基本功能测试失败，停止模型测试")
        return
    
    # 测试各个模型
    results = {}
    
    print("\n🤖 开始模型加载测试")
    print("=" * 60)
    
    results['SDXL'] = quick_test_stable_diffusion_xl()
    results['SVD'] = quick_test_stable_video_diffusion()
    results['SpeechT5'] = quick_test_speecht5()
    
    # 最终检查GPU内存
    check_gpu_memory()
    
    # 总结
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n📊 测试结果")
    print("=" * 60)
    print(f"⏱️  测试耗时: {duration:.1f} 秒")
    print()
    
    for model, result in results.items():
        status = "✅ 成功" if result else "❌ 失败"
        print(f"   {model}: {status}")
    
    all_passed = all(results.values())
    
    print()
    if all_passed:
        print("🎉 所有模型加载测试通过！")
        print("💡 可以运行完整的功能测试")
    else:
        failed_models = [model for model, result in results.items() if not result]
        print(f"⚠️ 以下模型加载失败: {', '.join(failed_models)}")
        print("💡 请检查网络连接和模型下载状态")
    
    # 保存快速测试结果
    try:
        os.makedirs("data/test_outputs", exist_ok=True)
        report_file = f"data/test_outputs/quick_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"AI模型快速测试报告\n")
            f.write(f"测试时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"测试耗时: {duration:.1f} 秒\n\n")
            f.write("测试结果:\n")
            for model, result in results.items():
                f.write(f"  {model}: {'成功' if result else '失败'}\n")
            f.write(f"\n总体结果: {'所有测试通过' if all_passed else '部分测试失败'}\n")
        
        print(f"\n📄 测试报告已保存: {report_file}")
        
    except Exception as e:
        print(f"⚠️ 无法保存测试报告: {e}")

if __name__ == "__main__":
    main()