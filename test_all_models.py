#!/usr/bin/env python3
"""
所有AI模型综合测试程序
"""

import os
import sys
import torch
from datetime import datetime
import subprocess

def check_system_requirements():
    """检查系统要求"""
    print("🔍 检查系统要求")
    print("=" * 40)
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"🐍 Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python版本过低，需要3.8+")
        return False
    else:
        print("✅ Python版本符合要求")
    
    # 检查CUDA
    if torch.cuda.is_available():
        print(f"🚀 CUDA可用: {torch.cuda.get_device_name(0)}")
        print(f"   CUDA版本: {torch.version.cuda}")
        print(f"   显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        print("⚠️ CUDA不可用，将使用CPU模式")
    
    # 检查内存
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"💾 系统内存: {memory.total / 1024**3:.1f} GB")
        print(f"   可用内存: {memory.available / 1024**3:.1f} GB")
        
        if memory.total < 16 * 1024**3:  # 16GB
            print("⚠️ 内存可能不足，建议16GB+")
    except ImportError:
        print("⚠️ 无法检查内存信息")
    
    return True

def check_dependencies():
    """检查依赖库"""
    print("\n🔧 检查依赖库")
    print("=" * 40)
    
    required_packages = [
        ("torch", "PyTorch"),
        ("diffusers", "Diffusers"),
        ("transformers", "Transformers"),
        ("PIL", "Pillow"),
        ("cv2", "OpenCV"),
        ("soundfile", "SoundFile"),
        ("scipy", "SciPy"),
        ("numpy", "NumPy")
    ]
    
    missing_packages = []
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (缺失)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 缺失依赖: {', '.join(missing_packages)}")
        print("安装命令: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ 所有依赖库已安装")
    return True

def test_model_downloads():
    """检查模型下载状态"""
    print("\n📦 检查模型下载状态")
    print("=" * 40)
    
    try:
        # 运行模型下载检查脚本
        result = subprocess.run([sys.executable, "check_downloads.py"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ 模型下载检查完成")
            print(result.stdout)
            return True
        else:
            print("⚠️ 模型下载检查失败")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ 模型检查超时")
        return False
    except FileNotFoundError:
        print("⚠️ 找不到check_downloads.py文件")
        return False
    except Exception as e:
        print(f"⚠️ 模型检查失败: {e}")
        return False

def run_individual_tests():
    """运行各个模型的单独测试"""
    print("\n🧪 运行模型测试")
    print("=" * 40)
    
    test_scripts = [
        ("test_stable_diffusion_xl.py", "Stable Diffusion XL"),
        ("test_stable_video_diffusion.py", "Stable Video Diffusion"),
        ("test_speecht5_tts.py", "SpeechT5 TTS")
    ]
    
    results = {}
    
    for script, model_name in test_scripts:
        print(f"\n🔄 测试 {model_name}...")
        
        if not os.path.exists(script):
            print(f"❌ 测试脚本不存在: {script}")
            results[model_name] = False
            continue
        
        try:
            result = subprocess.run([sys.executable, script], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ {model_name} 测试通过")
                results[model_name] = True
            else:
                print(f"❌ {model_name} 测试失败")
                print(f"错误信息: {result.stderr[:200]}...")
                results[model_name] = False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {model_name} 测试超时")
            results[model_name] = False
        except Exception as e:
            print(f"❌ {model_name} 测试异常: {e}")
            results[model_name] = False
    
    return results

def test_integration():
    """测试模型集成功能"""
    print("\n🔗 测试模型集成")
    print("=" * 40)
    
    try:
        # 导入项目模块
        sys.path.append('backend')
        from models.video_generator import VideoGenerator
        from models.character_generator import CharacterGenerator
        from models.voice_generator import VoiceGenerator
        
        print("✅ 模块导入成功")
        
        # 测试视频生成器初始化
        print("🔄 初始化视频生成器...")
        video_gen = VideoGenerator()
        print("✅ 视频生成器初始化成功")
        
        # 测试角色生成器初始化
        print("🔄 初始化角色生成器...")
        char_gen = CharacterGenerator()
        print("✅ 角色生成器初始化成功")
        
        # 测试语音生成器初始化
        print("🔄 初始化语音生成器...")
        voice_gen = VoiceGenerator()
        print("✅ 语音生成器初始化成功")
        
        print("✅ 所有模块集成测试通过")
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False

def generate_test_report(system_ok, deps_ok, downloads_ok, test_results, integration_ok):
    """生成测试报告"""
    print("\n📊 测试报告")
    print("=" * 50)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"测试时间: {timestamp}")
    print()
    
    # 系统检查
    print(f"🖥️  系统要求: {'✅ 通过' if system_ok else '❌ 失败'}")
    print(f"📦 依赖库: {'✅ 完整' if deps_ok else '❌ 缺失'}")
    print(f"🤖 模型下载: {'✅ 完成' if downloads_ok else '❌ 不完整'}")
    print(f"🔗 模块集成: {'✅ 成功' if integration_ok else '❌ 失败'}")
    print()
    
    # 模型测试结果
    print("🧪 模型测试结果:")
    for model_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {model_name}: {status}")
    
    # 总体评估
    all_passed = all([system_ok, deps_ok, downloads_ok, integration_ok] + list(test_results.values()))
    
    print()
    if all_passed:
        print("🎉 所有测试通过！系统可以正常使用。")
        print("💡 建议: 可以开始使用AI视频生成功能")
    else:
        print("⚠️ 部分测试失败，需要修复问题")
        print("💡 建议:")
        if not deps_ok:
            print("   - 安装缺失的依赖库")
        if not downloads_ok:
            print("   - 检查网络连接，重新下载模型")
        if not integration_ok:
            print("   - 检查代码完整性")
        if not all(test_results.values()):
            print("   - 检查GPU内存和系统资源")
    
    # 保存报告到文件
    try:
        report_dir = "data/test_outputs"
        os.makedirs(report_dir, exist_ok=True)
        
        report_file = os.path.join(report_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"AI视频生成工具 - 测试报告\n")
            f.write(f"测试时间: {timestamp}\n\n")
            f.write(f"系统要求: {'通过' if system_ok else '失败'}\n")
            f.write(f"依赖库: {'完整' if deps_ok else '缺失'}\n")
            f.write(f"模型下载: {'完成' if downloads_ok else '不完整'}\n")
            f.write(f"模块集成: {'成功' if integration_ok else '失败'}\n\n")
            f.write("模型测试结果:\n")
            for model_name, result in test_results.items():
                f.write(f"  {model_name}: {'通过' if result else '失败'}\n")
            f.write(f"\n总体结果: {'所有测试通过' if all_passed else '部分测试失败'}\n")
        
        print(f"\n📄 测试报告已保存: {report_file}")
        
    except Exception as e:
        print(f"⚠️ 无法保存测试报告: {e}")

def main():
    """主函数"""
    print("🤖 AI视频生成工具 - 综合测试")
    print("=" * 60)
    
    # 创建输出目录
    os.makedirs("data/test_outputs", exist_ok=True)
    
    # 执行各项检查
    system_ok = check_system_requirements()
    deps_ok = check_dependencies()
    downloads_ok = test_model_downloads() if deps_ok else False
    
    # 运行模型测试
    test_results = {}
    if system_ok and deps_ok:
        test_results = run_individual_tests()
    
    # 测试集成
    integration_ok = test_integration() if deps_ok else False
    
    # 生成报告
    generate_test_report(system_ok, deps_ok, downloads_ok, test_results, integration_ok)

if __name__ == "__main__":
    main()