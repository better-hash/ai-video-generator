import os
from typing import Dict, Any
from dataclasses import dataclass
from PIL import Image

# 添加 Stable Diffusion 依赖
from diffusers import StableDiffusionXLPipeline
import torch

@dataclass
class Scene:
    id: str
    description: str
    background_path: str
    metadata: Dict[str, Any]

class SceneGenerator:
    """场景生成器，使用 Stable Diffusion XL 生成场景图像"""
    
    def __init__(self, model_id: str = "stabilityai/stable-diffusion-xl-base-1.0"):
        """
        初始化 Stable Diffusion XL 模型
        
        :param model_id: Hugging Face 模型 ID
        """
        self.output_dir = "data/scenes"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 加载 Stable Diffusion XL 模型
        try:
            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                model_id, 
                torch_dtype=torch.float16,
                variant="fp16",
                use_safetensors=True
            )
            
            # 如果有 GPU，移动模型到 GPU
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
        except Exception as e:
            print(f"模型加载失败: {e}")
            self.pipe = None
    
    def generate_scene(self, scene_description: str) -> Scene:
        """
        使用 Stable Diffusion XL 生成场景图像
        
        :param scene_description: 场景描述
        :return: Scene 对象
        """
        # 生成唯一场景ID（使用时间戳）
        scene_id = str(int(os.times().elapsed))
        image_path = os.path.join(self.output_dir, f"{scene_id}.png")
        
        # 生成图像
        generated_image = self._generate_image(scene_description)
        
        if generated_image:
            generated_image.save(image_path)
        else:
            # 如果生成失败，回退到占位图像
            self._create_placeholder_image(image_path, scene_description)
        
        return Scene(
            id=scene_id,
            description=scene_description,
            background_path=image_path,
            metadata={
                "type": "ai_generated", 
                "model": "Stable Diffusion XL"
            }
        )
    
    def _generate_image(self, description: str, width: int = 1024, height: int = 768) -> Image.Image:
        """
        使用 Stable Diffusion XL 生成图像
        
        :param description: 图像描述
        :param width: 图像宽度
        :param height: 图像高度
        :return: 生成的图像
        """
        if not self.pipe:
            print("模型未初始化，无法生成图像")
            return None
        
        try:
            # 生成高质量图像的提示词
            prompt = f"High-quality, detailed scene: {description}. Photorealistic, cinematic lighting."
            
            # 生成图像
            image = self.pipe(
                prompt=prompt, 
                negative_prompt="low quality, blurry, sketch, cartoon, worst quality",
                height=height, 
                width=width,
                num_inference_steps=50,  # 推理步数
                guidance_scale=7.5  # 引导尺度
            ).images[0]
            
            return image
        except Exception as e:
            print(f"图像生成失败: {e}")
            return None
    
    def _create_placeholder_image(self, image_path: str, description: str):
        """创建占位图像（保留原有实现）"""
        width, height = 1024, 768
        image = Image.new('RGB', (width, height), (100, 150, 200))
        
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        text = f"场景背景\n{description[:50]}..."
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        image.save(image_path) 