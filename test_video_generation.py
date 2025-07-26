#!/usr/bin/env python3
"""
视频生成测试脚本
"""

import sys
import os
from pathlib import Path
import requests
import json
import time

def test_video_generation():
    """测试视频生成功能"""
    print("🎬 测试视频生成功能")
    print("=" * 50)
    
    # 确保后端服务正在运行
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code != 200:
            print("❌ 后端服务未运行，请先启动: python start_project.py --backend")
            return False
        print("✅ 后端服务正在运行")
    except:
        print("❌ 无法连接到后端服务，请先启动: python start_project.py --backend")
        return False
    
    # 1. 解析剧本
    print("\n📝 步骤1: 解析剧本")
    script_data = {
        "title": "浪漫晚餐",
        "content": """
场景：高级餐厅
角色：小明（男，30岁，西装革履，成熟稳重）
角色：小丽（女，28岁，优雅连衣裙，温柔美丽）

小明：今晚的月亮真美。
小丽：是啊，和你一起看更美。
小明：你总是这么会说话。
小丽：我只是说出心里话而已。
        """,
        "characters": [
            {"name": "小明", "description": "30岁男性，西装革履，成熟稳重"},
            {"name": "小丽", "description": "28岁女性，优雅连衣裙，温柔美丽"}
        ],
        "settings": {"quality": "high", "duration": 15}
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/scripts/parse",
            json=script_data
        )
        
        if response.status_code == 200:
            result = response.json()
            script_id = result["script_id"]
            print(f"✅ 剧本解析成功，ID: {script_id}")
            print(f"   解析结果: {len(result['parsed_data']['characters'])} 个角色, {len(result['parsed_data']['scenes'])} 个场景")
        else:
            print(f"❌ 剧本解析失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 剧本解析请求失败: {e}")
        return False
    
    # 2. 生成角色
    print("\n👥 步骤2: 生成角色")
    characters = []
    
    for char_data in script_data["characters"]:
        try:
            response = requests.post(
                "http://localhost:8000/api/characters/generate",
                json={
                    "name": char_data["name"],
                    "description": char_data["description"],
                    "voice_model": "default"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                characters.append(result["character"])
                print(f"✅ 角色生成成功: {char_data['name']}")
            else:
                print(f"❌ 角色生成失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 角色生成请求失败: {e}")
    
    # 3. 生成场景
    print("\n🎬 步骤3: 生成场景")
    scenes = []
    
    try:
        response = requests.post(
            "http://localhost:8000/api/scenes/generate",
            params={"scene_description": "高级餐厅，浪漫氛围"}
        )
        
        if response.status_code == 200:
            result = response.json()
            scenes.append(result["scene"])
            print(f"✅ 场景生成成功: {result['scene']['description']}")
        else:
            print(f"❌ 场景生成失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 场景生成请求失败: {e}")
    
    # 4. 生成视频
    print("\n🎥 步骤4: 生成视频")
    try:
        response = requests.post(
            "http://localhost:8000/api/videos/generate",
            json={
                "script_id": script_id,
                "quality": "high",
                "duration": 15
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            task_id = result["task_id"]
            print(f"✅ 视频生成任务已启动，任务ID: {task_id}")
            
            # 5. 监控生成进度
            print("\n⏳ 步骤5: 监控生成进度")
            max_attempts = 30  # 最多等待30次
            attempt = 0
            
            while attempt < max_attempts:
                try:
                    response = requests.get(f"http://localhost:8000/api/videos/{task_id}/status")
                    
                    if response.status_code == 200:
                        status_data = response.json()
                        progress = status_data.get("progress", 0)
                        status = status_data.get("status", "unknown")
                        
                        print(f"   进度: {progress}% - 状态: {status}")
                        
                        if status == "completed":
                            print("✅ 视频生成完成！")
                            break
                        elif status == "failed":
                            print("❌ 视频生成失败")
                            return False
                    
                    time.sleep(2)  # 等待2秒
                    attempt += 1
                    
                except Exception as e:
                    print(f"⚠️ 查询状态失败: {e}")
                    time.sleep(2)
                    attempt += 1
            
            if attempt >= max_attempts:
                print("⚠️ 等待超时，视频可能仍在生成中")
            
            # 6. 获取视频下载链接
            print("\n📥 步骤6: 获取视频下载链接")
            try:
                response = requests.get(f"http://localhost:8000/api/videos/{task_id}/download")
                
                if response.status_code == 200:
                    result = response.json()
                    video_url = result.get("video_url", "")
                    print(f"✅ 视频下载链接: {video_url}")
                    print(f"   完整路径: http://localhost:8000{video_url}")
                else:
                    print(f"❌ 获取下载链接失败: {response.text}")
                    
            except Exception as e:
                print(f"❌ 获取下载链接请求失败: {e}")
            
        else:
            print(f"❌ 视频生成请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 视频生成请求失败: {e}")
        return False
    
    print("\n🎉 视频生成测试完成！")
    print("\n📋 生成的文件位置:")
    print("   - 视频文件: data/videos/")
    print("   - 角色图像: data/characters/")
    print("   - 场景图像: data/scenes/")
    print("   - 临时文件: data/temp/")
    
    return True

def test_direct_video_generation():
    """直接测试视频生成器"""
    print("\n🔧 直接测试视频生成器")
    print("=" * 30)
    
    try:
        # 添加backend目录到Python路径
        sys.path.append(str(Path(__file__).parent / "backend"))
        
        from models.video_generator import VideoGenerator
        from models.script_parser import ScriptParser
        
        # 创建测试剧本
        test_script_content = """
        测试视频
        
        场景：公园
        角色：测试角色（男，25岁，休闲装）
        
        测试角色：这是一个测试视频。
        """
        
        # 解析剧本
        parser = ScriptParser()
        script = parser.parse_script(test_script_content)
        
        # 创建角色
        from models.character_generator import CharacterGenerator
        char_generator = CharacterGenerator()
        character = char_generator.generate_character("测试角色（男，25岁，休闲装）")
        
        # 生成视频
        video_generator = VideoGenerator()
        video = video_generator.generate_video(script, [character], [])
        
        print(f"✅ 直接生成成功:")
        print(f"   视频ID: {video.id}")
        print(f"   文件路径: {video.file_path}")
        print(f"   时长: {video.duration}秒")
        print(f"   元数据: {video.metadata}")
        
        return True
        
    except Exception as e:
        print(f"❌ 直接生成失败: {e}")
        return False

def main():
    """主函数"""
    print("🎬 AI视频生成工具 - 视频生成测试")
    print("=" * 60)
    
    # 测试API接口
    success1 = test_video_generation()
    
    # 测试直接生成
    # success2 = test_direct_video_generation()
    
    if success1 :
        print("\n🎉 测试完成！")
        print("\n💡 提示:")
        print("1. 查看 data/videos/ 目录下的生成文件")
        print("2. 如果生成了 .txt 文件，说明是模拟模式")
        print("3. 要生成真实视频，需要安装 OpenCV: pip install opencv-python")
        print("4. 要使用AI模型，需要安装: pip install torch diffusers transformers")
    else:
        print("\n❌ 测试失败")
    
    return success1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 