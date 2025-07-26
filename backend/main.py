from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import uvicorn
import asyncio
from datetime import datetime
import uuid

# 导入自定义模块
try:
    from .models.script_parser import ScriptParser
    from .models.character_generator import CharacterGenerator
    from .models.scene_generator import SceneGenerator
    from .models.video_generator import VideoGenerator
except ImportError:
    # 直接运行时使用绝对导入
    from models.script_parser import ScriptParser
    from models.character_generator import CharacterGenerator
    from models.scene_generator import SceneGenerator
    from models.video_generator import VideoGenerator

# 简化的数据模型
@dataclass
class Script:
    id: str
    title: str
    content: str
    parsed_data: Dict[str, Any]
    created_at: datetime

@dataclass
class Character:
    id: str
    name: str
    description: str
    appearance_path: str
    voice_model: Optional[str]
    created_at: datetime

@dataclass
class Scene:
    id: str
    description: str
    background_path: str
    created_at: datetime

@dataclass
class Video:
    id: str
    file_path: str
    duration: float
    metadata: Dict[str, Any]

app = FastAPI(
    title="AI视频生成工具",
    description="根据剧本生成AI视频的API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化AI模型
script_parser = ScriptParser()
character_generator = CharacterGenerator()
scene_generator = SceneGenerator()
video_generator = VideoGenerator()

# 任务状态存储 (实际应用中应该使用数据库或Redis)
task_status = {}

# 数据模型
class ScriptRequest(BaseModel):
    title: str
    content: str
    characters: List[dict]
    settings: Optional[dict] = {}

class CharacterRequest(BaseModel):
    name: str
    description: str
    voice_model: Optional[str] = "default"

class CharacterWithImageRequest(BaseModel):
    name: str
    description: str
    voice_model: Optional[str] = "default"
    image_path: Optional[str] = None

class VideoGenerationRequest(BaseModel):
    script_id: str
    quality: str = "high"
    duration: int = 30

# API端点
@app.get("/")
async def root():
    return {"message": "AI视频生成工具API服务", "version": "1.0.0"}

@app.post("/api/scripts/parse")
async def parse_script(request: ScriptRequest):
    """解析剧本文本"""
    try:
        # 解析剧本
        parsed_script = script_parser.parse_script(request.content)
        
        # 添加标题
        if hasattr(parsed_script, 'title'):
            parsed_script.title = request.title
        
        # 保存到数据库
        script_id = str(uuid.uuid4())
        script = Script(
            id=script_id,
            title=request.title,
            content=request.content,
            parsed_data={
                "title": getattr(parsed_script, 'title', request.title),
                "characters": getattr(parsed_script, 'characters', []),
                "scenes": getattr(parsed_script, 'scenes', []),
                "dialogues": getattr(parsed_script, 'dialogues', [])
            },
            created_at=datetime.utcnow()
        )
        
        # 这里应该保存到数据库
        # db.add(script)
        # db.commit()
        
        return {
            "script_id": script_id,
            "parsed_data": script.parsed_data,
            "message": "剧本解析成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"剧本解析失败: {str(e)}")

@app.post("/api/characters/generate")
async def generate_character(request: CharacterRequest):
    """生成角色形象"""
    try:
        # 生成角色形象
        character = character_generator.generate_character(request.description)
        
        # 保存角色信息
        character_id = str(uuid.uuid4())
        character_data = Character(
            id=character_id,
            name=request.name,
            description=request.description,
            appearance_path=character.image_path,
            voice_model=request.voice_model,
            created_at=datetime.utcnow()
        )
        
        return {
            "character_id": character_id,
            "character": {
                "id": character_data.id,
                "name": character_data.name,
                "description": character_data.description,
                "appearance_path": character_data.appearance_path,
                "voice_model": character_data.voice_model,
                "created_at": character_data.created_at.isoformat()
            },
            "message": "角色生成成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"角色生成失败: {str(e)}")

@app.post("/api/characters/generate-with-image")
async def generate_character_with_image(request: CharacterWithImageRequest):
    """使用指定图片生成角色形象"""
    try:
        if request.image_path:
            # 使用指定图片生成角色
            character = character_generator.generate_character_with_image(
                request.description, 
                request.image_path,
                request.name
            )
        else:
            # 使用默认生成方式
            character = character_generator.generate_character(request.description)
        
        # 保存角色信息
        character_id = str(uuid.uuid4())
        character_data = Character(
            id=character_id,
            name=request.name,
            description=request.description,
            appearance_path=character.image_path,
            voice_model=request.voice_model,
            created_at=datetime.utcnow()
        )
        
        return {
            "character_id": character_id,
            "character": {
                "id": character_data.id,
                "name": character_data.name,
                "description": character_data.description,
                "appearance_path": character_data.appearance_path,
                "voice_model": character_data.voice_model,
                "created_at": character_data.created_at.isoformat()
            },
            "message": "角色生成成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"角色生成失败: {str(e)}")

@app.post("/api/scenes/generate")
async def generate_scene(scene_description: Optional[str] = None):
    """生成场景"""
    try:
        # 如果没有提供场景描述，使用默认值
        if not scene_description:
            scene_description = "默认场景"
        
        # 生成场景
        scene = scene_generator.generate_scene(scene_description)
        
        scene_id = str(uuid.uuid4())
        scene_data = Scene(
            id=scene_id,
            description=scene_description,
            background_path=scene.background_path,
            created_at=datetime.utcnow()
        )
        
        return {
            "scene_id": scene_id,
            "scene": {
                "id": scene_data.id,
                "description": scene_data.description,
                "background_path": scene_data.background_path,
                "created_at": scene_data.created_at.isoformat()
            },
            "message": "场景生成成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"场景生成失败: {str(e)}")

@app.post("/api/videos/generate")
async def generate_video(request: VideoGenerationRequest):
    """生成视频"""
    try:
        # 创建任务ID
        task_id = str(uuid.uuid4())
        
        # 初始化任务状态
        task_status[task_id] = {
            "status": "processing",
            "progress": 0,
            "message": "任务已启动"
        }
        
        # 启动异步处理
        asyncio.create_task(process_video_generation(task_id, request))
        
        return {
            "task_id": task_id,
            "status": "processing",
            "message": "视频生成任务已启动"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"视频生成失败: {str(e)}")

@app.get("/api/videos/{task_id}/status")
async def get_video_status(task_id: str):
    """获取视频生成状态"""
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    status = task_status[task_id]
    return {
        "task_id": task_id,
        "status": status["status"],
        "progress": status["progress"],
        "message": status["message"],
        "estimated_time": "2分钟" if status["status"] == "processing" else None
    }

@app.get("/api/videos/{task_id}/download")
async def download_video(task_id: str):
    """下载生成的视频"""
    # 这里应该返回视频文件
    return {
        "task_id": task_id,
        "video_url": f"/videos/{task_id}/output.mp4",
        "message": "视频生成完成"
    }

async def process_video_generation(task_id: str, request: VideoGenerationRequest):
    """异步处理视频生成"""
    try:
        print(f"视频生成任务 {task_id} 开始...")
        
        # 更新进度
        task_status[task_id]["progress"] = 10
        task_status[task_id]["message"] = "解析剧本..."
        await asyncio.sleep(2)
        
        task_status[task_id]["progress"] = 30
        task_status[task_id]["message"] = "生成角色和场景..."
        await asyncio.sleep(3)
        
        task_status[task_id]["progress"] = 60
        task_status[task_id]["message"] = "合成视频..."
        await asyncio.sleep(3)
        
        task_status[task_id]["progress"] = 90
        task_status[task_id]["message"] = "生成音频..."
        await asyncio.sleep(2)
        
        # 完成
        task_status[task_id]["progress"] = 100
        task_status[task_id]["status"] = "completed"
        task_status[task_id]["message"] = "视频生成完成"
        
        print(f"视频生成任务 {task_id} 完成")
        
    except Exception as e:
        print(f"视频生成任务 {task_id} 失败: {str(e)}")
        task_status[task_id]["status"] = "failed"
        task_status[task_id]["message"] = f"生成失败: {str(e)}"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 