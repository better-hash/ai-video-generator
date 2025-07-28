import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
import uuid
from PIL import Image
import numpy as np

@dataclass
class Character:
    id: str
    name: str
    description: str
    image_path: str
    voice_model: str
    metadata: Dict[str, Any]

class CharacterGenerator:
    """角色生成器 - 使用Stable Diffusion生成角色形象"""
    
    def __init__(self, model_path: str = "stabilityai/stable-diffusion-xl-base-1.0"):
        self.model_path = model_path
        self.output_dir = "data/characters"
        self.character_templates = self._load_character_templates()
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 初始化AI模型
        self.sd_model = None
        self._init_ai_models()
        
        print(f"角色生成器初始化完成，模型路径: {model_path}")
    
    def _init_ai_models(self):
        """初始化AI模型"""
        try:
            import torch
            from diffusers import StableDiffusionXLPipeline
            
            print("🔄 正在加载角色生成模型...")
            
            self.sd_model = StableDiffusionXLPipeline.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                variant="fp16",
                use_safetensors=True
            )
            
            if torch.cuda.is_available():
                self.sd_model = self.sd_model.to("cuda")
            
            print("✅ Stable Diffusion XL 角色生成模型加载成功")
            
        except Exception as e:
            print(f"⚠️ 角色生成模型加载失败，使用占位模式: {e}")
            self.sd_model = None
    
    def _load_character_templates(self) -> Dict[str, Dict[str, Any]]:
        """加载角色模板"""
        templates = {
            "male": {
                "base_prompt": "portrait of a man, professional, high quality, detailed face",
                "age_ranges": {
                    "young": "young man, 20-30 years old",
                    "middle": "middle-aged man, 30-50 years old", 
                    "elder": "elderly man, 50+ years old"
                },
                "styles": {
                    "formal": "wearing formal suit, business attire",
                    "casual": "wearing casual clothes, relaxed",
                    "elegant": "wearing elegant clothing, sophisticated"
                }
            },
            "female": {
                "base_prompt": "portrait of a woman, professional, high quality, detailed face",
                "age_ranges": {
                    "young": "young woman, 20-30 years old",
                    "middle": "middle-aged woman, 30-50 years old",
                    "elder": "elderly woman, 50+ years old"
                },
                "styles": {
                    "formal": "wearing formal dress, business attire",
                    "casual": "wearing casual clothes, relaxed",
                    "elegant": "wearing elegant dress, sophisticated"
                }
            }
        }
        return templates
    
    def generate_character(self, description: str, name: str = "") -> Character:
        """根据描述生成角色形象"""
        try:
            # 解析角色描述
            char_info = self._parse_character_description(description)
            
            # 生成角色ID
            character_id = str(uuid.uuid4())
            
            # 构建生成提示词
            prompt = self._build_character_prompt(char_info)
            
            # 生成角色图像
            image_path = self._generate_character_image(prompt, character_id)
            
            # 创建角色对象
            character = Character(
                id=character_id,
                name=name or char_info.get("name", "未命名角色"),
                description=description,
                image_path=image_path,
                voice_model=self._select_voice_model(char_info),
                metadata=char_info
            )
            
            # 保存角色信息
            self._save_character_info(character)
            
            return character
            
        except Exception as e:
            print(f"角色生成失败: {str(e)}")
            # 返回默认角色
            return self._create_default_character(description, name)
    
    def generate_character_with_image(self, description: str, image_path: str, name: str = "") -> Character:
        """根据描述和指定图片路径生成角色"""
        try:
            # 解析角色描述
            char_info = self._parse_character_description(description)
            
            # 生成角色ID
            character_id = str(uuid.uuid4())
            
            # 验证图片文件是否存在
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"图片文件不存在: {image_path}")
            
            # 复制图片到角色目录
            new_image_path = os.path.join(self.output_dir, f"{character_id}.png")
            import shutil
            shutil.copy2(image_path, new_image_path)
            
            # 创建角色对象
            character = Character(
                id=character_id,
                name=name or char_info.get("name", "未命名角色"),
                description=description,
                image_path=new_image_path,
                voice_model=self._select_voice_model(char_info),
                metadata=char_info
            )
            
            # 保存角色信息
            self._save_character_info(character)
            
            return character
            
        except Exception as e:
            print(f"角色生成失败: {str(e)}")
            # 返回默认角色
            return self._create_default_character(description, name)
    
    def _parse_character_description(self, description: str) -> Dict[str, Any]:
        """解析角色描述"""
        char_info = {
            "gender": "unknown",
            "age": "middle",
            "style": "casual",
            "appearance": "",
            "personality": "",
            "name": ""
        }
        
        # 性别检测
        if any(word in description for word in ["男", "男人", "男性", "先生", "他"]):
            char_info["gender"] = "male"
        elif any(word in description for word in ["女", "女人", "女性", "女士", "她"]):
            char_info["gender"] = "female"
        
        # 年龄检测
        if any(word in description for word in ["年轻", "20", "30", "青年"]):
            char_info["age"] = "young"
        elif any(word in description for word in ["中年", "40", "50", "成熟"]):
            char_info["age"] = "middle"
        elif any(word in description for word in ["老年", "60", "70", "年长"]):
            char_info["age"] = "elder"
        
        # 风格检测
        if any(word in description for word in ["正式", "西装", "商务", "职业"]):
            char_info["style"] = "formal"
        elif any(word in description for word in ["优雅", "高贵", "精致"]):
            char_info["style"] = "elegant"
        
        # 提取外观描述
        appearance_keywords = ["穿着", "戴", "发型", "眼睛", "头发"]
        for keyword in appearance_keywords:
            if keyword in description:
                start = description.find(keyword)
                end = description.find("，", start)
                if end == -1:
                    end = description.find("。", start)
                if end == -1:
                    end = len(description)
                char_info["appearance"] = description[start:end].strip()
                break
        
        return char_info
    
    def _build_character_prompt(self, char_info: Dict[str, Any]) -> str:
        """构建角色生成提示词"""
        gender = char_info["gender"]
        age = char_info["age"]
        style = char_info["style"]
        appearance = char_info["appearance"]
        
        if gender not in self.character_templates:
            gender = "male"  # 默认男性
        
        template = self.character_templates[gender]
        base_prompt = template["base_prompt"]
        age_prompt = template["age_ranges"].get(age, "")
        style_prompt = template["styles"].get(style, "")
        
        # 组合提示词
        prompt_parts = [base_prompt]
        if age_prompt:
            prompt_parts.append(age_prompt)
        if style_prompt:
            prompt_parts.append(style_prompt)
        if appearance:
            prompt_parts.append(appearance)
        
        # 添加质量提升词
        prompt_parts.extend([
            "high quality", "detailed", "professional photography",
            "studio lighting", "sharp focus", "4k resolution"
        ])
        
        return ", ".join(prompt_parts)
    
    def _generate_character_image(self, prompt: str, character_id: str) -> str:
        """生成角色图像"""
        image_path = os.path.join(self.output_dir, f"{character_id}.png")
        
        if self.sd_model:
            # 使用AI模型生成角色图像
            try:
                print(f"🎨 正在生成角色图像: {prompt[:50]}...")
                
                # 生成图像
                result = self.sd_model(
                    prompt=prompt,
                    negative_prompt="low quality, blurry, distorted, deformed, worst quality, bad anatomy",
                    num_inference_steps=30,
                    guidance_scale=7.5,
                    width=512,
                    height=512
                )
                
                # 检查结果
                if hasattr(result, 'images') and len(result.images) > 0:
                    image = result.images[0]
                    image.save(image_path)
                    print(f"✅ 角色图像生成成功: {image_path}")
                    return image_path
                else:
                    raise Exception("生成结果为空")
                    
            except Exception as e:
                print(f"⚠️ AI角色图像生成失败: {e}")
                # 回退到占位图像
                self._create_placeholder_image(image_path, prompt)
                return image_path
        else:
            # 创建占位图像
            self._create_placeholder_image(image_path, prompt)
            return image_path
    
    def _create_placeholder_image(self, image_path: str, prompt: str):
        """创建占位图像（用于演示）"""
        # 创建一个简单的彩色图像作为占位符
        width, height = 512, 512
        
        # 根据提示词生成不同的颜色
        colors = {
            "male": (100, 150, 200),  # 蓝色系
            "female": (200, 150, 200),  # 紫色系
            "young": (150, 200, 150),  # 绿色系
            "middle": (200, 200, 150),  # 黄色系
            "elder": (200, 150, 150),  # 红色系
        }
        
        # 选择颜色
        color = (128, 128, 128)  # 默认灰色
        for keyword, rgb in colors.items():
            if keyword in prompt.lower():
                color = rgb
                break
        
        # 创建图像
        image = Image.new('RGB', (width, height), color)
        
        # 添加文字
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(image)
        
        # 尝试使用默认字体
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # 绘制文字
        text = f"角色图像\n{prompt[:50]}..."
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        # 保存图像
        image.save(image_path)
        print(f"占位图像已保存: {image_path}")
    
    def _select_voice_model(self, char_info: Dict[str, Any]) -> str:
        """选择语音模型"""
        gender = char_info["gender"]
        age = char_info["age"]
        
        # 简单的语音模型选择逻辑
        if gender == "male":
            if age == "young":
                return "male_young_01"
            elif age == "middle":
                return "male_middle_01"
            else:
                return "male_elder_01"
        else:
            if age == "young":
                return "female_young_01"
            elif age == "middle":
                return "female_middle_01"
            else:
                return "female_elder_01"
    
    def _save_character_info(self, character: Character):
        """保存角色信息"""
        info_path = os.path.join(self.output_dir, f"{character.id}.json")
        
        char_data = {
            "id": character.id,
            "name": character.name,
            "description": character.description,
            "image_path": character.image_path,
            "voice_model": character.voice_model,
            "metadata": character.metadata
        }
        
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(char_data, f, ensure_ascii=False, indent=2)
    
    def _create_default_character(self, description: str, name: str) -> Character:
        """创建默认角色（当生成失败时）"""
        character_id = str(uuid.uuid4())
        image_path = os.path.join(self.output_dir, f"{character_id}_default.png")
        
        # 创建默认占位图像
        self._create_placeholder_image(image_path, "default character")
        
        return Character(
            id=character_id,
            name=name or "默认角色",
            description=description,
            image_path=image_path,
            voice_model="default",
            metadata={"error": "生成失败，使用默认角色"}
        )
    
    def get_character(self, character_id: str) -> Optional[Character]:
        """根据ID获取角色信息"""
        info_path = os.path.join(self.output_dir, f"{character_id}.json")
        
        if os.path.exists(info_path):
            with open(info_path, 'r', encoding='utf-8') as f:
                char_data = json.load(f)
            
            return Character(**char_data)
        
        return None

# 使用示例
if __name__ == "__main__":
    generator = CharacterGenerator()
    
    # 测试角色生成
    test_descriptions = [
        "小明（男，30岁，西装革履，成熟稳重）",
        "小丽（女，28岁，优雅连衣裙，温柔美丽）",
        "老张（男，60岁，慈祥老人，经验丰富）"
    ]
    
    for desc in test_descriptions:
        character = generator.generate_character(desc)
        print(f"生成角色: {character.name}")
        print(f"描述: {character.description}")
        print(f"图像路径: {character.image_path}")
        print(f"语音模型: {character.voice_model}")
        print("---")