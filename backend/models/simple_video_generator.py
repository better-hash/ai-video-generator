
import os
import uuid
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Video:
    id: str
    file_path: str
    duration: float
    metadata: Dict[str, Any]

class SimpleVideoGenerator:
    """简化版视频生成器 - 不依赖AI模型"""
    
    def __init__(self):
        self.output_dir = "data/videos"
        self.temp_dir = "data/temp"
        self.fps = 24
        self.resolution = (1920, 1080)
        
        for dir_path in [self.output_dir, self.temp_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        print("🎬 简化版视频生成器初始化完成")
    
    def generate_video(self, script, characters: List, actions: List) -> Video:
        """生成视频（简化版）"""
        try:
            video_id = str(uuid.uuid4())
            print(f"🎬 开始生成视频: {video_id}")
            
            # 创建简单的视频文件
            video_path = os.path.join(self.output_dir, f"{video_id}.txt")
            
            with open(video_path, 'w', encoding='utf-8') as f:
                f.write(f"简化版视频文件 - {video_id}\n")
                f.write(f"剧本: {getattr(script, 'title', 'unknown')}\n")
                f.write(f"角色数: {len(characters)}\n")
                f.write(f"帧率: {self.fps}\n")
                f.write(f"分辨率: {self.resolution}\n")
                f.write("状态: 简化模式生成完成\n")
            
            print(f"✅ 视频生成完成: {video_path}")
            
            return Video(
                id=video_id,
                file_path=video_path,
                duration=10.0,
                metadata={
                    "status": "simple_mode",
                    "script": getattr(script, 'title', 'unknown'),
                    "characters": len(characters),
                    "mode": "simplified"
                }
            )
            
        except Exception as e:
            print(f"❌ 视频生成失败: {e}")
            return self._create_fallback_video(script, characters)
    
    def _create_fallback_video(self, script, characters: List) -> Video:
        """创建备用视频"""
        video_id = str(uuid.uuid4())
        fallback_path = os.path.join(self.output_dir, f"{video_id}_fallback.txt")
        
        with open(fallback_path, 'w', encoding='utf-8') as f:
            f.write("视频生成失败，这是备用文件\n")
            f.write(f"剧本: {getattr(script, 'title', 'unknown')}\n")
            f.write(f"角色数: {len(characters)}\n")
        
        return Video(
            id=video_id,
            file_path=fallback_path,
            duration=10.0,
            metadata={"status": "fallback", "error": "生成失败"}
        )
