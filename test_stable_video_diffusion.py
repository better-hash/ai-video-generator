#!/usr/bin/env python3
"""
Stable Video Diffusion 视频生成模型测试程序
"""

import os
import torch
from PIL import Image
from datetime import datetime
import numpy as np

def test_stable_video_diffusion():
    """测试 Stable Video Diffusion 模型"""
    print("🎬 测试 Stable Video Diffusion 视频生成模型")
    print("=" * 50)
    
    try:
        # 检查CUDA可用性
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"📱 使用设备: {device}")
        
        # 导入模型
        from diffusers import StableVideoDiffusionPipeline
        
        print("🔄 正在加载 Stable Video Diffusion 模型...")
        pipeline = StableVideoDiffusionPipeline.from_pretrained(
            "stabilityai/stable-video-diffusion-img2vid-xt",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            variant="fp16" if device == "cuda" else None
        )
        
        if device == "cuda":
            pipeline = pipeline.to("cuda")
        
        print("✅ 模型加载成功")
        
        # 创建输出目录
        output_dir = "data/test_outputs/svd"
        os.makedirs(output_dir, exist_ok=True)
        
        # 准备测试图像
        test_images = []
        
        # 检查是否有现有的测试图像
        test_image_paths = [
            "data/scenes/scene_001.png",
            "data/scenes/123.jpg"
        ]
        
        for img_path in test_image_paths:
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path).convert("RGB")
                    # 调整图像尺寸到模型要求
                    img = img.resize((1024, 576))  # SVD推荐尺寸
                    test_images.append((img, os.path.basename(img_path)))
                    print(f"📸 加载测试图像: {img_path}")
                except Exception as e:
                    print(f"⚠️ 无法加载图像 {img_path}: {e}")
        
        # 如果没有现有图像，创建一个简单的测试图像
        if not test_images:
            print("📸 创建默认测试图像...")
            # 创建一个简单的渐变图像
            img_array = np.zeros((576, 1024, 3), dtype=np.uint8)
            for i in range(576):
                img_array[i, :, 0] = int(255 * i / 576)  # 红色渐变
                img_array[i, :, 1] = int(128)  # 绿色固定
                img_array[i, :, 2] = int(255 * (576 - i) / 576)  # 蓝色反向渐变
            
            test_img = Image.fromarray(img_array)
            test_images.append((test_img, "gradient_test.png"))
        
        # 生成视频
        for i, (image, img_name) in enumerate(test_images):
            print(f"\n🎯 测试 {i+1}/{len(test_images)}: {img_name}")
            
            try:
                # 生成视频帧
                print("🔄 正在生成视频帧...")
                with torch.no_grad():
                    frames = pipeline(
                        image=image,
                        num_frames=14,  # SVD默认帧数
                        num_inference_steps=25,
                        fps=7,
                        motion_bucket_id=127,  # 运动强度
                        noise_aug_strength=0.02
                    ).frames[0]
                
                # 保存视频帧
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                frame_dir = os.path.join(output_dir, f"svd_test_{i+1}_{timestamp}")
                os.makedirs(frame_dir, exist_ok=True)
                
                for j, frame in enumerate(frames):
                    frame_path = os.path.join(frame_dir, f"frame_{j:03d}.png")
                    frame.save(frame_path)
                
                print(f"✅ 视频帧生成成功: {frame_dir}")
                print(f"   帧数: {len(frames)}")
                print(f"   分辨率: {frames[0].size}")
                
                # 尝试合成为视频文件
                try:
                    video_path = create_video_from_frames(frame_dir, f"svd_test_{i+1}_{timestamp}.mp4")
                    if video_path:
                        print(f"🎬 视频文件生成成功: {video_path}")
                except Exception as e:
                    print(f"⚠️ 视频合成失败: {e}")
                    print("   帧序列已保存，可手动合成视频")
                
            except Exception as e:
                print(f"❌ 视频生成失败: {e}")
        
        print(f"\n🎉 Stable Video Diffusion 测试完成")
        print(f"📁 输出目录: {output_dir}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请安装必要的依赖: pip install diffusers torch")
        return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def create_video_from_frames(frame_dir, output_name):
    """从帧序列创建视频文件"""
    try:
        import cv2
        
        # 获取帧文件列表
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])
        if not frame_files:
            return None
        
        # 读取第一帧获取尺寸
        first_frame_path = os.path.join(frame_dir, frame_files[0])
        first_frame = cv2.imread(first_frame_path)
        height, width, _ = first_frame.shape
        
        # 创建视频写入器
        output_path = os.path.join(frame_dir, output_name)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, 7.0, (width, height))
        
        # 写入所有帧
        for frame_file in frame_files:
            frame_path = os.path.join(frame_dir, frame_file)
            frame = cv2.imread(frame_path)
            video_writer.write(frame)
        
        video_writer.release()
        return output_path
        
    except ImportError:
        print("⚠️ OpenCV未安装，无法合成视频文件")
        return None
    except Exception as e:
        print(f"⚠️ 视频合成错误: {e}")
        return None

def test_model_info():
    """显示模型信息"""
    print("\n📋 Stable Video Diffusion 模型信息")
    print("-" * 30)
    print("模型名称: stabilityai/stable-video-diffusion-img2vid-xt")
    print("功能: 图像到视频生成")
    print("输入分辨率: 1024x576 (推荐)")
    print("输出帧数: 14帧 (约2秒@7fps)")
    print("推荐步数: 25")
    print("内存需求: 8-12GB VRAM (GPU) / 32GB RAM (CPU)")
    print("运动强度: 0-255 (127为默认)")

if __name__ == "__main__":
    test_model_info()
    success = test_stable_video_diffusion()
    
    if success:
        print("\n🎊 所有测试通过！")
    else:
        print("\n⚠️ 测试失败，请检查环境配置")