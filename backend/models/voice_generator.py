import os
import torch
from typing import Optional, Dict, Any
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan

class VoiceGenerator:
    """使用 Microsoft SpeechT5 生成语音"""
    
    def __init__(self, 
                 model_id: str = "microsoft/speecht5_tts",
                 vocoder_id: str = "microsoft/speecht5_hifigan"):
        """
        初始化 SpeechT5 语音合成模型
        
        :param model_id: 文本转语音模型
        :param vocoder_id: 声码器模型
        """
        self.output_dir = "data/voices"
        os.makedirs(self.output_dir, exist_ok=True)
        
        try:
            # 加载处理器
            self.processor = SpeechT5Processor.from_pretrained(model_id)
            
            # 加载文本转语音模型
            self.model = SpeechT5ForTextToSpeech.from_pretrained(model_id)
            
            # 加载声码器
            self.vocoder = SpeechT5HifiGan.from_pretrained(vocoder_id)
            
            # 如果有 GPU，移动模型到 GPU
            if torch.cuda.is_available():
                self.model = self.model.to("cuda")
                self.vocoder = self.vocoder.to("cuda")
        except Exception as e:
            print(f"语音生成模型加载失败: {e}")
            self.processor = None
            self.model = None
            self.vocoder = None
    
    def generate_voice(self, 
                       text: str, 
                       speaker_embedding: Optional[torch.Tensor] = None,
                       language: str = 'zh-CN') -> Optional[str]:
        """
        生成语音
        
        :param text: 要转换为语音的文本
        :param speaker_embedding: 说话人嵌入（可选）
        :param language: 语言代码
        :return: 生成的语音文件路径
        """
        if not self.model or not self.processor:
            print("语音生成模型未初始化")
            return None
        
        try:
            # 生成语音 ID（使用时间戳）
            voice_id = str(int(os.times().elapsed))
            voice_path = os.path.join(self.output_dir, f"{voice_id}.wav")
            
            # 处理输入文本
            inputs = self.processor(text=text, return_tensors="pt")
            
            # 如果没有提供说话人嵌入，使用默认嵌入
            if speaker_embedding is None:
                # 使用预训练的默认说话人嵌入
                speaker_embedding = torch.zeros(512)
            
            # 生成语音
            speech = self.model.generate_speech(
                inputs["input_ids"], 
                speaker_embedding, 
                vocoder=self.vocoder
            )
            
            # 保存语音文件
            torch.save(speech.squeeze(), voice_path)
            
            return voice_path
        except Exception as e:
            print(f"语音生成失败: {e}")
            return None
    
    def load_speaker_embedding(self, embedding_path: Optional[str] = None) -> Optional[torch.Tensor]:
        """
        加载说话人嵌入
        
        :param embedding_path: 说话人嵌入文件路径
        :return: 说话人嵌入张量
        """
        if embedding_path and os.path.exists(embedding_path):
            try:
                return torch.load(embedding_path)
            except Exception as e:
                print(f"加载说话人嵌入失败: {e}")
        
        return None 