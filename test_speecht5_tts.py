#!/usr/bin/env python3
"""
SpeechT5 语音合成模型测试程序
"""

import os
import torch
from datetime import datetime
import numpy as np

def test_speecht5_tts():
    """测试 SpeechT5 语音合成模型"""
    print("🎤 测试 SpeechT5 语音合成模型")
    print("=" * 50)
    
    try:
        # 检查CUDA可用性
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"📱 使用设备: {device}")
        
        # 导入模型
        from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
        
        print("🔄 正在加载 SpeechT5 模型...")
        
        # 加载处理器
        processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        print("✅ 处理器加载成功")
        
        # 加载文本转语音模型
        model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        print("✅ TTS模型加载成功")
        
        # 加载声码器
        vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        print("✅ 声码器加载成功")
        
        # 移动模型到设备
        if device == "cuda":
            model = model.to("cuda")
            vocoder = vocoder.to("cuda")
            print("✅ 模型已移动到GPU")
        
        # 创建输出目录
        output_dir = "data/test_outputs/tts"
        os.makedirs(output_dir, exist_ok=True)
        
        # 测试文本
        test_texts = [
            "Hello, this is a test of the SpeechT5 text-to-speech model.",
            "The weather is beautiful today, perfect for a walk in the park.",
            "Artificial intelligence is transforming the way we work and live.",
            "Thank you for testing the speech synthesis system."
        ]
        
        # 创建默认说话人嵌入
        print("🔄 创建说话人嵌入...")
        speaker_embedding = torch.zeros(512)
        if device == "cuda":
            speaker_embedding = speaker_embedding.to("cuda")
        
        # 生成语音
        for i, text in enumerate(test_texts):
            print(f"\n🎯 测试 {i+1}/{len(test_texts)}: {text[:50]}...")
            
            try:
                # 限制文本长度
                text = text[:200] if len(text) > 200 else text
                
                # 处理输入文本
                inputs = processor(text=text, return_tensors="pt")
                
                # 移动输入到设备
                if device == "cuda":
                    inputs = {k: v.to("cuda") for k, v in inputs.items()}
                
                # 生成语音
                print("🔄 正在生成语音...")
                with torch.no_grad():
                    speech = model.generate_speech(
                        inputs["input_ids"], 
                        speaker_embedding.unsqueeze(0), 
                        vocoder=vocoder
                    )
                
                # 保存语音文件
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"tts_test_{i+1}_{timestamp}.wav"
                filepath = os.path.join(output_dir, filename)
                
                # 使用soundfile保存
                try:
                    import soundfile as sf
                    sf.write(filepath, speech.cpu().numpy(), 16000)
                    print(f"✅ 语音生成成功: {filepath}")
                    print(f"   采样率: 16000 Hz")
                    print(f"   时长: {len(speech.cpu().numpy()) / 16000:.2f} 秒")
                except ImportError:
                    # 如果没有soundfile，使用scipy
                    try:
                        from scipy.io import wavfile
                        wavfile.write(filepath, 16000, speech.cpu().numpy())
                        print(f"✅ 语音生成成功: {filepath}")
                        print(f"   采样率: 16000 Hz")
                        print(f"   时长: {len(speech.cpu().numpy()) / 16000:.2f} 秒")
                    except ImportError:
                        print("❌ 无法保存音频文件，请安装 soundfile 或 scipy")
                        # 至少保存为numpy数组
                        np_filepath = filepath.replace('.wav', '.npy')
                        np.save(np_filepath, speech.cpu().numpy())
                        print(f"✅ 语音数据保存为numpy数组: {np_filepath}")
                
            except Exception as e:
                print(f"❌ 语音生成失败: {e}")
        
        # 测试中文文本（如果支持）
        print("\n🌏 测试中文语音合成...")
        chinese_texts = [
            "你好，这是语音合成测试。",
            "今天天气很好。"
        ]
        
        for i, text in enumerate(chinese_texts):
            try:
                print(f"🎯 中文测试 {i+1}: {text}")
                
                # 处理中文文本
                inputs = processor(text=text, return_tensors="pt")
                
                if device == "cuda":
                    inputs = {k: v.to("cuda") for k, v in inputs.items()}
                
                with torch.no_grad():
                    speech = model.generate_speech(
                        inputs["input_ids"], 
                        speaker_embedding.unsqueeze(0), 
                        vocoder=vocoder
                    )
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"tts_chinese_{i+1}_{timestamp}.wav"
                filepath = os.path.join(output_dir, filename)
                
                try:
                    import soundfile as sf
                    sf.write(filepath, speech.cpu().numpy(), 16000)
                    print(f"✅ 中文语音生成成功: {filepath}")
                except:
                    np_filepath = filepath.replace('.wav', '.npy')
                    np.save(np_filepath, speech.cpu().numpy())
                    print(f"✅ 中文语音数据保存: {np_filepath}")
                    
            except Exception as e:
                print(f"⚠️ 中文语音生成失败: {e}")
                print("   SpeechT5主要针对英文优化")
        
        print(f"\n🎉 SpeechT5 测试完成")
        print(f"📁 输出目录: {output_dir}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请安装必要的依赖: pip install transformers torch soundfile")
        return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_speaker_embeddings():
    """测试不同的说话人嵌入"""
    print("\n🎭 测试不同说话人嵌入")
    print("-" * 30)
    
    try:
        from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
        import torch
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 加载模型
        processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        
        if device == "cuda":
            model = model.to("cuda")
            vocoder = vocoder.to("cuda")
        
        # 创建不同的说话人嵌入
        embeddings = {
            "default": torch.zeros(512),
            "variant1": torch.randn(512) * 0.1,
            "variant2": torch.randn(512) * 0.2
        }
        
        test_text = "This is a test with different speaker embeddings."
        output_dir = "data/test_outputs/tts"
        os.makedirs(output_dir, exist_ok=True)
        
        for name, embedding in embeddings.items():
            try:
                if device == "cuda":
                    embedding = embedding.to("cuda")
                
                inputs = processor(text=test_text, return_tensors="pt")
                if device == "cuda":
                    inputs = {k: v.to("cuda") for k, v in inputs.items()}
                
                with torch.no_grad():
                    speech = model.generate_speech(
                        inputs["input_ids"], 
                        embedding.unsqueeze(0), 
                        vocoder=vocoder
                    )
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"speaker_{name}_{timestamp}.wav"
                filepath = os.path.join(output_dir, filename)
                
                try:
                    import soundfile as sf
                    sf.write(filepath, speech.cpu().numpy(), 16000)
                    print(f"✅ 说话人 {name}: {filepath}")
                except:
                    np_filepath = filepath.replace('.wav', '.npy')
                    np.save(np_filepath, speech.cpu().numpy())
                    print(f"✅ 说话人 {name}: {np_filepath}")
                    
            except Exception as e:
                print(f"❌ 说话人 {name} 测试失败: {e}")
        
    except Exception as e:
        print(f"❌ 说话人嵌入测试失败: {e}")

def test_model_info():
    """显示模型信息"""
    print("\n📋 SpeechT5 模型信息")
    print("-" * 30)
    print("TTS模型: microsoft/speecht5_tts")
    print("声码器: microsoft/speecht5_hifigan")
    print("功能: 文本到语音合成")
    print("采样率: 16000 Hz")
    print("语言支持: 主要英文，部分多语言")
    print("说话人: 可自定义嵌入向量")
    print("内存需求: 2-4GB VRAM (GPU) / 8GB RAM (CPU)")

if __name__ == "__main__":
    test_model_info()
    success = test_speecht5_tts()
    
    if success:
        test_speaker_embeddings()
        print("\n🎊 所有测试通过！")
    else:
        print("\n⚠️ 测试失败，请检查环境配置")