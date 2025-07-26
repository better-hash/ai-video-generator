import re
from typing import List, Dict, Any
from dataclasses import dataclass
import json

@dataclass
class Character:
    name: str
    description: str
    gender: str = ""
    age: str = ""
    appearance: str = ""

@dataclass
class Scene:
    id: str
    description: str
    location: str
    time: str = ""
    characters: List[str] = None
    actions: List[str] = None

@dataclass
class Dialogue:
    character: str
    content: str
    emotion: str = ""

@dataclass
class Script:
    title: str
    characters: List[Character]
    scenes: List[Scene]
    dialogues: List[Dialogue]
    metadata: Dict[str, Any]

class ScriptParser:
    """剧本解析器"""
    
    def __init__(self):
        self.character_pattern = r"角色[：:]\s*(.+)"
        self.scene_pattern = r"场景[：:]\s*(.+)"
        self.dialogue_pattern = r"([^：:]+)[：:]\s*(.+)"
    
    def parse_script(self, script_text: str) -> Script:
        """解析剧本文本"""
        lines = script_text.strip().split('\n')
        
        # 提取标题
        title = self._extract_title(lines)
        
        # 提取角色
        characters = self._extract_characters(lines)
        
        # 提取场景
        scenes = self._extract_scenes(lines)
        
        # 提取对话
        dialogues = self._extract_dialogues(lines)
        
        # 构建剧本对象
        script = Script(
            title=title,
            characters=characters,
            scenes=scenes,
            dialogues=dialogues,
            metadata={
                "total_scenes": len(scenes),
                "total_characters": len(characters),
                "total_dialogues": len(dialogues)
            }
        )
        
        return script
    
    def _extract_title(self, lines: List[str]) -> str:
        """提取标题"""
        for line in lines:
            if line.strip() and not line.startswith(('场景', '角色', '：', ':')):
                return line.strip()
        return "未命名剧本"
    
    def _extract_characters(self, lines: List[str]) -> List[Character]:
        """提取角色信息"""
        characters = []
        character_names = set()
        
        for line in lines:
            # 匹配角色描述
            match = re.search(self.character_pattern, line)
            if match:
                char_desc = match.group(1).strip()
                
                # 解析角色描述
                char_info = self._parse_character_description(char_desc)
                if char_info.name and char_info.name not in character_names:
                    characters.append(char_info)
                    character_names.add(char_info.name)
        
        return characters
    
    def _parse_character_description(self, desc: str) -> Character:
        """解析角色描述"""
        # 简单的角色描述解析
        # 格式: 角色名（性别，年龄，外观描述）
        name = desc
        gender = ""
        age = ""
        appearance = ""
        
        # 提取括号内的信息
        bracket_match = re.search(r"（(.+)）", desc)
        if bracket_match:
            bracket_content = bracket_match.group(1)
            name = desc.split('（')[0].strip()
            
            # 解析括号内的信息
            parts = bracket_content.split('，')
            if len(parts) >= 1:
                gender = parts[0].strip()
            if len(parts) >= 2:
                age = parts[1].strip()
            if len(parts) >= 3:
                appearance = parts[2].strip()
        
        return Character(
            name=name,
            description=desc,
            gender=gender,
            age=age,
            appearance=appearance
        )
    
    def _extract_scenes(self, lines: List[str]) -> List[Scene]:
        """提取场景信息"""
        scenes = []
        scene_id = 1
        
        for line in lines:
            match = re.search(self.scene_pattern, line)
            if match:
                scene_desc = match.group(1).strip()
                scene = Scene(
                    id=f"scene_{scene_id}",
                    description=scene_desc,
                    location=scene_desc,
                    characters=[],
                    actions=[]
                )
                scenes.append(scene)
                scene_id += 1
        
        return scenes
    
    def _extract_dialogues(self, lines: List[str]) -> List[Dialogue]:
        """提取对话信息"""
        dialogues = []
        
        for line in lines:
            match = re.search(self.dialogue_pattern, line)
            if match and not line.startswith(('场景', '角色')):
                character = match.group(1).strip()
                content = match.group(2).strip()
                
                # 跳过空对话
                if content:
                    dialogue = Dialogue(
                        character=character,
                        content=content,
                        emotion=self._detect_emotion(content)
                    )
                    dialogues.append(dialogue)
        
        return dialogues
    
    def _detect_emotion(self, text: str) -> str:
        """简单的情感检测"""
        emotion_keywords = {
            "愤怒": ["生气", "愤怒", "恼火", "气愤"],
            "悲伤": ["难过", "伤心", "悲伤", "哭泣"],
            "高兴": ["开心", "高兴", "快乐", "兴奋"],
            "紧张": ["紧张", "担心", "焦虑", "害怕"],
            "平静": ["平静", "冷静", "淡定"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return emotion
        
        return "中性"
    
    def to_dict(self, script: Script) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "title": script.title,
            "characters": [
                {
                    "name": char.name,
                    "description": char.description,
                    "gender": char.gender,
                    "age": char.age,
                    "appearance": char.appearance
                }
                for char in script.characters
            ],
            "scenes": [
                {
                    "id": scene.id,
                    "description": scene.description,
                    "location": scene.location,
                    "time": scene.time,
                    "characters": scene.characters,
                    "actions": scene.actions
                }
                for scene in script.scenes
            ],
            "dialogues": [
                {
                    "character": dialogue.character,
                    "content": dialogue.content,
                    "emotion": dialogue.emotion
                }
                for dialogue in script.dialogues
            ],
            "metadata": script.metadata
        }

# 使用示例
if __name__ == "__main__":
    parser = ScriptParser()
    
    sample_script = """
    浪漫晚餐
    
    场景：高级餐厅
    角色：小明（男，30岁，西装革履，成熟稳重）
    角色：小丽（女，28岁，优雅连衣裙，温柔美丽）
    
    小明：今晚的月亮真美。
    小丽：是啊，和你一起看更美。
    小明：你总是这么会说话。
    小丽：我只是说出心里话而已。
    """
    
    result = parser.parse_script(sample_script)
    print(json.dumps(parser.to_dict(result), ensure_ascii=False, indent=2)) 