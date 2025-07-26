#!/usr/bin/env python3
"""
直接测试视频生成功能
"""

import sys
import os
from pathlib import Path

def test_video_generation():
    """测试视频生成功能"""
    print("🎬 直接测试视频生成功能")
    print("=" * 50)
    
    try:
        # 添加backend目录到Python路径
        sys.path.append(str(Path(__file__).parent / "backend"))
        
        from models.video_generator import VideoGenerator
        from models.script_parser import ScriptParser
        from models.character_generator import CharacterGenerator
        
        # 创建测试剧本
        test_script_content = """
        测试视频
        
        场景：公园
        角色：测试角色（男，25岁，休闲装）
        
        测试角色：这是一个测试视频。
        """
        
        print("📝 解析剧本...")
        parser = ScriptParser()
        script = parser.parse_script(test_script_content)
        print(f"✅ 剧本解析成功: {script.title if hasattr(script, 'title') else '未知标题'}")
        
        print("👥 生成角色...")
        char_generator = CharacterGenerator()
        character = char_generator.generate_character("测试角色（男，25岁，休闲装）")
        print(f"✅ 角色生成成功: {character.name}")
        
        print("🎬 生成视频...")
        video_generator = VideoGenerator()
        
        # 检查AI模型状态
        print(f"   AI模型状态:")
        print(f"   - SD Pipeline: {'✅ 已加载' if video_generator.sd_pipeline else '❌ 未加载'}")
        print(f"   - SVD Pipeline: {'✅ 已加载' if video_generator.svd_pipeline else '❌ 未加载'}")
        print(f"   - TTS Pipeline: {'✅ 已加载' if video_generator.tts_pipeline else '❌ 未加载'}")
        
        video = video_generator.generate_video(script, [character], [])
        
        print(f"✅ 视频生成成功:")
        print(f"   视频ID: {video.id}")
        print(f"   文件路径: {video.file_path}")
        print(f"   时长: {video.duration}秒")
        print(f"   状态: {video.metadata.get('status', 'unknown')}")
        
        # 检查文件是否存在
        if os.path.exists(video.file_path):
            file_size = os.path.getsize(video.file_path)
            print(f"   文件大小: {file_size} 字节")
            
            # 检查文件类型
            if video.file_path.endswith('.mp4'):
                print("   ✅ 生成了真实的MP4视频文件")
            elif video.file_path.endswith('.txt'):
                print("   ⚠️ 生成了占位符文本文件")
        else:
            print("   ❌ 文件不存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🎬 AI视频生成工具 - 直接测试")
    print("=" * 60)
    
    success = test_video_generation()
    
    if success:
        print("\n🎉 测试完成！")
        print("\n💡 说明:")
        print("1. 如果生成了MP4文件，说明视频生成功能正常")
        print("2. 如果AI模型未加载，会使用占位符内容")
        print("3. 要使用真实AI生成，需要安装: pip install torch diffusers transformers")
    else:
        print("\n❌ 测试失败")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 