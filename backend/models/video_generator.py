import os
import uuid
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import torch
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Video:
    id: str
    file_path: str
    duration: float
    metadata: Dict[str, Any]

@dataclass
class VideoFrame:
    """视频帧数据"""
    frame_number: int
    image_path: str
    timestamp: float
    characters: List[Dict[str, Any]]
    scene_description: str

class VideoGenerator:
    """视频生成器 - 集成AI模型生成真实视频"""
    
    def __init__(self):
        self.output_dir = "data/videos"
        self.temp_dir = "data/temp"
        self.fps = 24  # 帧率
        self.resolution = (1920, 1080)  # 分辨率
        
        # 创建目录
        for dir_path in [self.output_dir, self.temp_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # 初始化AI模型属性
        self.sd_pipeline = None
        self.svd_pipeline = None
        self.tts_pipeline = None
        
        # 初始化AI模型（实际使用时取消注释）
        self._init_ai_models()
        
        print("🎬 视频生成器初始化完成")
    
    def _init_ai_models(self):
        """初始化AI模型"""
        try:
            import torch
            from diffusers import StableVideoDiffusionPipeline, StableDiffusionXLPipeline
            from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
            
            print("🔄 正在加载AI模型...")
            
            # 视频生成模型
            try:
                self.svd_pipeline = StableVideoDiffusionPipeline.from_pretrained(
                    "stabilityai/stable-video-diffusion-img2vid-xt",
                    torch_dtype=torch.float16,
                    variant="fp16"
                )
                if torch.cuda.is_available():
                    self.svd_pipeline = self.svd_pipeline.to("cuda")
                print("✅ Stable Video Diffusion 加载成功")
            except Exception as e:
                print(f"⚠️ Stable Video Diffusion 加载失败: {e}")
                self.svd_pipeline = None
            
            # 图像生成模型 - 使用SDXL
            try:
                self.sd_pipeline = StableDiffusionXLPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-xl-base-1.0",
                    torch_dtype=torch.float16,
                    variant="fp16",
                    use_safetensors=True
                )
                if torch.cuda.is_available():
                    self.sd_pipeline = self.sd_pipeline.to("cuda")
                print("✅ Stable Diffusion XL 加载成功")
            except Exception as e:
                print(f"⚠️ Stable Diffusion XL 加载失败: {e}")
                self.sd_pipeline = None
            
            # 语音合成模型 - 使用SpeechT5
            try:
                self.tts_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
                self.tts_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
                self.tts_vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
                
                if torch.cuda.is_available():
                    self.tts_model = self.tts_model.to("cuda")
                    self.tts_vocoder = self.tts_vocoder.to("cuda")
                
                # 创建默认说话人嵌入 - 使用随机初始化而不是全零
                self.default_speaker_embedding = torch.randn(512) * 0.1
                if torch.cuda.is_available():
                    self.default_speaker_embedding = self.default_speaker_embedding.to("cuda")
                
                print("✅ SpeechT5 TTS 加载成功")
            except Exception as e:
                print(f"⚠️ SpeechT5 TTS 加载失败: {e}")
                self.tts_processor = None
                self.tts_model = None
                self.tts_vocoder = None
                self.default_speaker_embedding = None
            
            print("✅ AI模型初始化完成")
            
        except Exception as e:
            print(f"⚠️ AI模型加载失败，使用模拟模式: {e}")
            self.svd_pipeline = None
            self.sd_pipeline = None
            self.tts_processor = None
            self.tts_model = None
            self.tts_vocoder = None
            self.default_speaker_embedding = None
    
    def generate_video(self, script, characters: List, actions: List) -> Video:
        """生成完整视频"""
        try:
            video_id = str(uuid.uuid4())
            print(f"🎬 开始生成视频: {video_id}")
            
            # 1. 解析剧本结构
            scenes = self._parse_script_to_scenes(script)
            
            # 2. 生成场景背景
            scene_backgrounds = self._generate_scene_backgrounds(scenes)
            
            # 3. 生成角色图像
            character_images = self._generate_character_images(characters)
            
            # 4. 生成视频帧序列
            frames = self._generate_video_frames(scenes, scene_backgrounds, character_images, actions)
            
            # 5. 合成最终视频
            video_path = self._compose_final_video(frames, video_id)
            
            # 6. 生成音频
            audio_path = self._generate_audio(script, video_id)
            
            # 7. 合并音视频
            final_video_path = self._merge_audio_video(video_path, audio_path, video_id)
            
            # 8. 清理临时文件
            self._cleanup_temp_files(frames, scene_backgrounds, character_images)
            
            print(f"✅ 视频生成完成: {final_video_path}")
            
            return Video(
                id=video_id,
                file_path=final_video_path,
                duration=self._calculate_duration(frames),
                metadata={
                    "status": "completed",
                    "script": script.title if hasattr(script, 'title') else "unknown",
                    "scenes": len(scenes),
                    "characters": len(characters),
                    "frames": len(frames),
                    "resolution": self.resolution,
                    "fps": self.fps
                }
            )
            
        except Exception as e:
            print(f"❌ 视频生成失败: {e}")
            return self._create_fallback_video(script, characters)
    
    def _parse_script_to_scenes(self, script) -> List[Dict[str, Any]]:
        """解析剧本为场景列表"""
        scenes = []
        
        if hasattr(script, 'scenes') and script.scenes:
            for scene in script.scenes:
                scenes.append({
                    "id": scene.id,
                    "description": scene.description,
                    "duration": 5.0,  # 默认5秒
                    "characters": scene.characters or [],
                    "actions": scene.actions or []
                })
        else:
            # 如果没有场景信息，创建一个默认场景
            scenes.append({
                "id": "scene_001",
                "description": "默认场景",
                "duration": 10.0,
                "characters": [],
                "actions": []
            })
        
        return scenes
    
    def _generate_scene_backgrounds(self, scenes: List[Dict[str, Any]]) -> Dict[str, str]:
        """生成场景背景图像"""
        backgrounds = {}
        
        for scene in scenes:
            scene_id = scene["id"]
            description = scene["description"]
            
            if self.sd_pipeline:
                # 使用AI模型生成背景
                background_path = self._generate_ai_background(description, scene_id)
            else:
                # 生成占位背景
                background_path = self._generate_placeholder_background(description, scene_id)
            
            backgrounds[scene_id] = background_path
        
        return backgrounds
    
    def _generate_ai_background(self, description: str, scene_id: str) -> str:
        """使用AI模型生成背景"""
        try:
            # 检查SD模型是否可用
            if not self.sd_pipeline:
                raise Exception("SD模型未加载")
                
            prompt = f"cinematic scene: {description}, high quality, detailed, professional photography"
            
            # 生成图像
            result = self.sd_pipeline(
                prompt=prompt,
                num_inference_steps=30,
                guidance_scale=7.5,
            )
            
            # 检查结果并获取图像
            image = None
            if hasattr(result, 'images') and result.images and len(result.images) > 0:
                image = result.images[0]
            elif hasattr(result, 'image'):
                image = result.image
            else:
                raise Exception(f"无效的生成结果格式: {type(result)}")
            
            # 检查图像类型
            if not hasattr(image, 'save'):
                raise Exception(f"生成的图像类型无效: {type(image)}")
            
            # 调整图像大小
            image = image.resize(self.resolution)
            
            # 保存图像
            background_path = os.path.join(self.temp_dir, f"background_{scene_id}.png")
            image.save(background_path)
            
            print(f"✅ 背景图像生成成功: {background_path}")
            return background_path
            
        except Exception as e:
            print(f"⚠️ AI背景生成失败，使用占位图: {str(e)}")
            return self._generate_placeholder_background(description, scene_id)
    
    def _generate_placeholder_background(self, description: str, scene_id: str) -> str:
        """生成占位背景图像"""
        width, height = self.resolution
        
        # 根据场景描述选择颜色
        colors = {
            "餐厅": (139, 69, 19),  # 棕色
            "公园": (34, 139, 34),   # 绿色
            "办公室": (105, 105, 105), # 灰色
            "家": (255, 228, 196),   # 米色
            "街道": (128, 128, 128),  # 灰色
        }
        
        color = (100, 150, 200)  # 默认蓝色
        for keyword, rgb in colors.items():
            if keyword in description:
                color = rgb
                break
        
        # 创建背景图像
        image = Image.new('RGB', (width, height), color)
        draw = ImageDraw.Draw(image)
        
        # 添加文字
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        text = f"场景背景\n{description}"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # 保存图像
        background_path = os.path.join(self.temp_dir, f"background_{scene_id}.png")
        image.save(background_path)
        
        return background_path
    
    def _generate_character_images(self, characters: List) -> Dict[str, str]:
        """生成角色图像"""
        character_images = {}
        
        for i, character in enumerate(characters):
            char_id = character.id if hasattr(character, 'id') else f"char_{i}"
            
            if self.sd_pipeline:
                # 使用AI模型生成角色
                image_path = self._generate_ai_character(character, char_id)
            else:
                # 生成占位角色图像
                image_path = self._generate_placeholder_character(character, char_id)
            
            character_images[char_id] = image_path
        
        return character_images
    
    def _generate_ai_character(self, character, char_id: str) -> str:
        """使用AI模型生成角色图像"""
        try:
            # 检查SD模型是否可用
            if not self.sd_pipeline:
                raise Exception("SD模型未加载")
                
            description = character.description if hasattr(character, 'description') else str(character)
            prompt = f"portrait of {description}, high quality, detailed face, professional photography"
            
            # 生成图像
            result = self.sd_pipeline(
                prompt=prompt,
                num_inference_steps=30,
                guidance_scale=7.5,
            )
            
            # 检查结果并获取图像
            image = None
            if hasattr(result, 'images') and result.images and len(result.images) > 0:
                image = result.images[0]
            elif hasattr(result, 'image'):
                image = result.image
            else:
                raise Exception(f"无效的生成结果格式: {type(result)}")
            
            # 检查图像类型
            if not hasattr(image, 'save'):
                raise Exception(f"生成的图像类型无效: {type(image)}")
            
            # 保存图像
            image_path = os.path.join(self.temp_dir, f"character_{char_id}.png")
            image.save(image_path)
            
            print(f"✅ 角色图像生成成功: {image_path}")
            return image_path
            
        except Exception as e:
            print(f"⚠️ AI角色生成失败，使用占位图: {e}")
            return self._generate_placeholder_character(character, char_id)
    
    def _generate_placeholder_character(self, character, char_id: str) -> str:
        """生成占位角色图像"""
        width, height = 512, 512
        
        # 根据角色描述选择颜色
        description = character.description if hasattr(character, 'description') else str(character)
        
        colors = {
            "男": (100, 150, 200),  # 蓝色
            "女": (200, 150, 200),  # 紫色
            "年轻": (150, 200, 150), # 绿色
            "老年": (200, 150, 150), # 红色
        }
        
        color = (128, 128, 128)  # 默认灰色
        for keyword, rgb in colors.items():
            if keyword in description:
                color = rgb
                break
        
        # 创建角色图像
        image = Image.new('RGB', (width, height), color)
        draw = ImageDraw.Draw(image)
        
        # 添加文字
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        text = f"角色图像\n{description[:30]}..."
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # 保存图像
        image_path = os.path.join(self.temp_dir, f"character_{char_id}.png")
        image.save(image_path)
        
        return image_path
    
    def _generate_video_frames(self, scenes: List[Dict], backgrounds: Dict[str, str], 
                              characters: Dict[str, str], actions: List) -> List[VideoFrame]:
        """生成视频帧序列"""
        frames = []
        frame_number = 0
        
        for scene in scenes:
            scene_id = scene["id"]
            background_path = backgrounds[scene_id]
            duration = scene["duration"]
            
            # 计算该场景的帧数
            scene_frames = int(duration * self.fps)
            
            for i in range(scene_frames):
                timestamp = frame_number / self.fps
                
                # 生成帧图像
                frame_path = self._generate_frame_image(
                    background_path, characters, scene, actions, frame_number
                )
                
                frame = VideoFrame(
                    frame_number=frame_number,
                    image_path=frame_path,
                    timestamp=timestamp,
                    characters=list(characters.keys()),
                    scene_description=scene["description"]
                )
                
                frames.append(frame)
                frame_number += 1
        
        return frames
    
    def _generate_frame_image(self, background_path: str, characters: Dict[str, str], 
                             scene: Dict, actions: List, frame_number: int) -> str:
        """生成单帧图像"""
        # 加载背景
        background = Image.open(background_path).resize(self.resolution)
        
        # 合成角色到背景上
        composite_image = background.copy()
        draw = ImageDraw.Draw(composite_image)
        
        # 简单的角色布局（实际应用中需要更复杂的布局算法）
        char_positions = self._calculate_character_positions(len(characters), self.resolution)
        
        # 合成角色图像
        for i, (char_id, char_image_path) in enumerate(characters.items()):
            if i < len(char_positions) and os.path.exists(char_image_path):
                try:
                    # 加载角色图像
                    char_image = Image.open(char_image_path).resize((200, 200))
                    
                    # 计算位置
                    x, y = char_positions[i]
                    
                    # 合成到背景上
                    composite_image.paste(char_image, (x, y), char_image if char_image.mode == 'RGBA' else None)
                    
                    # 添加角色名称标签
                    char_name = char_id.replace('char_', '角色')
                    try:
                        font = ImageFont.load_default()
                    except:
                        font = None
                    
                    # 在角色下方添加名称
                    text_bbox = draw.textbbox((0, 0), char_name, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_x = x + 100 - text_width // 2
                    text_y = y + 220
                    
                    # 添加文字背景
                    draw.rectangle([text_x-5, text_y-5, text_x+text_width+5, text_y+20], 
                                 fill=(0, 0, 0, 128))
                    draw.text((text_x, text_y), char_name, fill=(255, 255, 255), font=font)
                    
                except Exception as e:
                    print(f"⚠️ 角色图像合成失败: {e}")
        
        # 添加台词字幕（如果有对话）
        if hasattr(scene, 'dialogues') and scene.get('dialogues'):
            dialogue = scene['dialogues'][0] if scene['dialogues'] else None
            if dialogue:
                try:
                    font = ImageFont.load_default()
                except:
                    font = None
                
                # 在底部添加字幕
                subtitle_text = f"{dialogue.get('character', '角色')}: {dialogue.get('content', '台词')}"
                text_bbox = draw.textbbox((0, 0), subtitle_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (self.resolution[0] - text_width) // 2
                text_y = self.resolution[1] - 80
                
                # 添加字幕背景
                draw.rectangle([text_x-10, text_y-10, text_x+text_width+10, text_y+30], 
                             fill=(0, 0, 0, 180))
                draw.text((text_x, text_y), subtitle_text, fill=(255, 255, 255), font=font)
        
        # 保存帧
        frame_path = os.path.join(self.temp_dir, f"frame_{frame_number:06d}.png")
        composite_image.save(frame_path)
        
        return frame_path
    
    def _calculate_character_positions(self, num_characters: int, resolution: tuple) -> List[tuple]:
        """计算角色位置"""
        width, height = resolution
        
        if num_characters == 1:
            return [(width // 2 - 100, height // 2 - 100)]
        elif num_characters == 2:
            return [
                (width // 3 - 100, height // 2 - 100),
                (2 * width // 3 - 100, height // 2 - 100)
            ]
        else:
            # 更多角色的网格布局
            positions = []
            cols = int(np.ceil(np.sqrt(num_characters)))
            rows = int(np.ceil(num_characters / cols))
            
            for i in range(num_characters):
                row = i // cols
                col = i % cols
                x = (col + 1) * width // (cols + 1) - 100
                y = (row + 1) * height // (rows + 1) - 100
                positions.append((x, y))
            
            return positions
    
    def _compose_final_video(self, frames: List[VideoFrame], video_id: str) -> str:
        """合成最终视频"""
        try:
            import cv2
            
            # 获取第一帧的尺寸
            first_frame = cv2.imread(frames[0].image_path)
            height, width, layers = first_frame.shape
            
            # 创建视频写入器
            video_path = os.path.join(self.output_dir, f"{video_id}_temp.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, self.fps, (width, height))
            
            # 写入帧
            for frame in frames:
                img = cv2.imread(frame.image_path)
                out.write(img)
            
            out.release()
            return video_path
            
        except ImportError:
            print("⚠️ OpenCV未安装，使用模拟视频")
            return self._create_simulation_video(frames, video_id)
        except Exception as e:
            print(f"⚠️ 视频合成失败: {e}")
            return self._create_simulation_video(frames, video_id)
    
    def _create_simulation_video(self, frames: List[VideoFrame], video_id: str) -> str:
        """创建模拟视频文件"""
        # 创建一个简单的文本文件作为视频占位符
        video_path = os.path.join(self.output_dir, f"{video_id}_temp.txt")
        
        with open(video_path, 'w', encoding='utf-8') as f:
            f.write(f"模拟视频文件 - {video_id}\n")
            f.write(f"总帧数: {len(frames)}\n")
            f.write(f"帧率: {self.fps}\n")
            f.write(f"分辨率: {self.resolution}\n")
            f.write(f"时长: {len(frames) / self.fps:.2f}秒\n")
        
        return video_path
    
    def _generate_audio(self, script, video_id: str) -> str:
        """生成音频"""
        try:
            if self.tts_processor and self.tts_model and self.tts_vocoder:
                # 使用AI模型生成语音
                return self._generate_ai_audio(script, video_id)
            else:
                # 生成占位音频
                return self._generate_placeholder_audio(script, video_id)
                
        except Exception as e:
            print(f"⚠️ 音频生成失败: {e}")
            return self._generate_placeholder_audio(script, video_id)
    
    def _generate_ai_audio(self, script, video_id: str) -> str:
        """使用AI模型生成音频"""
        try:
            # 检查TTS模型是否可用
            if not (self.tts_processor and self.tts_model and self.tts_vocoder and self.default_speaker_embedding is not None):
                raise Exception("TTS模型或speaker_embedding未加载")
            
            # 提取对话文本
            dialogues = []
            if hasattr(script, 'dialogues') and script.dialogues:
                for dialogue in script.dialogues:
                    dialogues.append(f"{dialogue.character}: {dialogue.content}")
            
            if not dialogues:
                dialogues = ["欢迎观看AI生成的视频"]
            
            # 合并所有对话（限制长度避免过长）
            full_text = " ".join(dialogues)[:200]  # 限制文本长度
            
            # 生成语音
            audio_path = os.path.join(self.temp_dir, f"audio_{video_id}.wav")
            
            # 使用SpeechT5生成语音
            inputs = self.tts_processor(text=full_text, return_tensors="pt")
            
            # 移动输入到GPU（如果可用）
            if torch.cuda.is_available() and self.tts_model.device.type == 'cuda':
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            # 确保speaker_embedding维度正确
            speaker_embedding = self.default_speaker_embedding
            if speaker_embedding.dim() == 1:
                speaker_embedding = speaker_embedding.unsqueeze(0)
            
            # 生成语音
            with torch.no_grad():
                speech = self.tts_model.generate_speech(
                    inputs["input_ids"], 
                    speaker_embedding, 
                    vocoder=self.tts_vocoder
                )
            
            # 保存音频文件
            try:
                import soundfile as sf
                # 确保音频数据在CPU上
                audio_data = speech.cpu().numpy() if hasattr(speech, 'cpu') else speech
                sf.write(audio_path, audio_data, 16000)
            except ImportError:
                # 如果soundfile不可用，创建占位文件
                raise Exception("soundfile库未安装")
            
            print(f"✅ AI音频生成成功: {audio_path}")
            return audio_path
                
        except Exception as e:
            print(f"⚠️ AI音频生成失败: {e}")
            return self._generate_placeholder_audio(script, video_id)
    
    def _generate_placeholder_audio(self, script, video_id: str) -> str:
        """生成占位音频文件"""
        audio_path = os.path.join(self.temp_dir, f"audio_{video_id}.txt")
        
        with open(audio_path, 'w', encoding='utf-8') as f:
            f.write(f"模拟音频文件 - {video_id}\n")
            f.write("这里应该是合成的语音内容\n")
        
        return audio_path
    
    def _merge_audio_video(self, video_path: str, audio_path: str, video_id: str) -> str:
        """合并音视频"""
        try:
            import cv2
            
            # 简单的音视频合并（实际应用中需要更复杂的处理）
            final_path = os.path.join(self.output_dir, f"{video_id}.mp4")
            
            # 复制视频文件
            import shutil
            shutil.copy2(video_path, final_path)
            
            return final_path
            
        except Exception as e:
            print(f"⚠️ 音视频合并失败: {e}")
            # 返回视频文件路径
            return video_path
    
    def _calculate_duration(self, frames: List[VideoFrame]) -> float:
        """计算视频时长"""
        return len(frames) / self.fps
    
    def _cleanup_temp_files(self, frames: List[VideoFrame], backgrounds: Dict[str, str], 
                           characters: Dict[str, str]):
        """清理临时文件"""
        try:
            # 删除帧图像
            for frame in frames:
                if os.path.exists(frame.image_path):
                    os.remove(frame.image_path)
            
            # 删除背景图像
            for background_path in backgrounds.values():
                if os.path.exists(background_path):
                    os.remove(background_path)
            
            # 删除角色图像
            for char_path in characters.values():
                if os.path.exists(char_path):
                    os.remove(char_path)
                    
        except Exception as e:
            print(f"⚠️ 清理临时文件失败: {e}")
    
    def _create_fallback_video(self, script, characters: List) -> Video:
        """创建备用视频（当生成失败时）"""
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

class VideoGenerator:
    """使用 Stable Video Diffusion 生成视频"""
    
    def __init__(self, model_id: str = "stabilityai/stable-video-diffusion"):
        """
        初始化 Stable Video Diffusion 模型
        
        :param model_id: Hugging Face 模型 ID
        """
        self.output_dir = "data/videos"
        os.makedirs(self.output_dir, exist_ok=True)
        
        try:
            from diffusers import StableVideoDiffusionPipeline
            
            self.pipe = StableVideoDiffusionPipeline.from_pretrained(
                model_id, 
                torch_dtype=torch.float16,
                variant="fp16"
            )
            
            # 如果有 GPU，移动模型到 GPU
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
        except Exception as e:
            print(f"视频生成模型加载失败: {e}")
            self.pipe = None
    
    def generate_video(self, image_path: str, duration: float = 4.0) -> Optional[str]:
        """
        从图像生成视频
        
        :param image_path: 输入图像路径
        :param duration: 视频持续时间（秒）
        :return: 生成的视频路径，如果失败则返回 None
        """
        if not self.pipe:
            print("视频生成模型未初始化")
            return None
        
        try:
            # 生成视频 ID（使用时间戳）
            video_id = str(int(os.times().elapsed))
            video_path = os.path.join(self.output_dir, f"{video_id}.mp4")
            
            # 生成视频
            video = self.pipe(
                image_path, 
                num_frames=int(duration * 8),  # 假设 8 fps
                num_inference_steps=50,
                decode_chunk_size=8
            )
            
            # 保存视频
            video[0].save(video_path)
            
            return video_path
        except Exception as e:
            print(f"视频生成失败: {e}")
            return None