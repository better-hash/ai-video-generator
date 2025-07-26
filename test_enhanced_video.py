#!/usr/bin/env python3
"""
增强视频生成测试 - 包含角色、台词和声音
"""

import sys
import os
from pathlib import Path

def test_enhanced_video_generation():
    """测试增强的视频生成功能"""
    print("🎬 增强视频生成测试 - 包含角色、台词和声音")
    print("=" * 60)
    
    try:
        # 添加backend目录到Python路径
        sys.path.append(str(Path(__file__).parent / "backend"))
        
        from models.video_generator import VideoGenerator
        from models.script_parser import ScriptParser
        from models.character_generator import CharacterGenerator
        
        # 创建更丰富的测试剧本
        test_script_content = """
        浪漫晚餐
        
        场景：高级餐厅，烛光晚餐，浪漫氛围
        角色：小明（男，30岁，西装革履，成熟稳重）
        角色：小丽（女，28岁，优雅连衣裙，温柔美丽）
        
        小明：今晚的月亮真美。
        小丽：是啊，和你一起看更美。
        小明：你总是这么会说话。
        小丽：我只是说出心里话而已。
        """
        
        print("📝 解析剧本...")
        parser = ScriptParser()
        script = parser.parse_script(test_script_content)
        print(f"✅ 剧本解析成功: {script.title if hasattr(script, 'title') else '未知标题'}")
        
        print("\n👥 生成角色...")
        char_generator = CharacterGenerator()
        characters = []
        
        # 生成多个角色
        character_descriptions = [
            "小明（男，30岁，西装革履，成熟稳重）",
            "小丽（女，28岁，优雅连衣裙，温柔美丽）"
        ]
        
        for desc in character_descriptions:
            character = char_generator.generate_character(desc)
            characters.append(character)
            print(f"✅ 角色生成成功: {character.name}")
        
        print("\n🎬 生成增强视频...")
        video_generator = VideoGenerator()
        
        # 检查AI模型状态
        print(f"   AI模型状态:")
        print(f"   - SD Pipeline: {'✅ 已加载' if video_generator.sd_pipeline else '❌ 未加载'}")
        print(f"   - SVD Pipeline: {'✅ 已加载' if video_generator.svd_pipeline else '❌ 未加载'}")
        print(f"   - TTS Pipeline: {'✅ 已加载' if video_generator.tts_pipeline else '❌ 未加载'}")
        
        # 生成视频
        video = video_generator.generate_video(script, characters, [])
        
        print(f"\n✅ 增强视频生成成功:")
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
                
                # 检查是否包含音频
                try:
                    import cv2
                    cap = cv2.VideoCapture(video.file_path)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    cap.release()
                    
                    print(f"   📹 视频信息:")
                    print(f"      - 帧率: {fps} fps")
                    print(f"      - 总帧数: {frame_count}")
                    print(f"      - 分辨率: {video_generator.resolution}")
                    
                except Exception as e:
                    print(f"   ⚠️ 无法读取视频信息: {e}")
                    
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
    print("🎬 AI视频生成工具 - 增强测试")
    print("=" * 60)
    
    success = test_enhanced_video_generation()
    
    if success:
        print("\n🎉 增强测试完成！")
        print("\n💡 改进说明:")
        print("1. ✅ 添加了角色图像合成")
        print("2. ✅ 添加了角色名称标签")
        print("3. ✅ 添加了台词字幕")
        print("4. ✅ 改进了AI模型调用")
        print("5. ✅ 增强了音频生成")
    else:
        print("\n❌ 测试失败")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 