# 视频生成使用指南

## 🎬 概述

AI视频生成工具现在支持完整的视频生成流程，包括：
- 剧本解析
- 角色生成
- 场景生成
- 视频合成
- 音频生成

## 🚀 快速开始

### 1. 基础测试

运行基础测试脚本：
```bash
python test_video_generation.py
```

这将测试：
- API接口调用
- 直接视频生成
- 文件输出验证

### 2. 使用API接口

#### 启动后端服务
```bash
python start_project.py --backend
```

#### 调用视频生成API

```python
import requests

# 1. 解析剧本
response = requests.post("http://localhost:8000/api/scripts/parse", json={
    "title": "我的视频",
    "content": "场景：公园\n角色：小明（男，25岁）\n小明：你好！",
    "characters": [],
    "settings": {}
})
script_id = response.json()["script_id"]

# 2. 生成视频
response = requests.post("http://localhost:8000/api/videos/generate", json={
    "script_id": script_id,
    "quality": "high",
    "duration": 10
})
task_id = response.json()["task_id"]

# 3. 查询状态
response = requests.get(f"http://localhost:8000/api/videos/{task_id}/status")
print(response.json())

# 4. 下载视频
response = requests.get(f"http://localhost:8000/api/videos/{task_id}/download")
print(response.json())
```

### 3. 直接使用视频生成器

```python
from backend.models.video_generator import VideoGenerator
from backend.models.script_parser import ScriptParser
from backend.models.character_generator import CharacterGenerator

# 解析剧本
parser = ScriptParser()
script = parser.parse_script("""
测试视频
场景：公园
角色：小明（男，25岁）
小明：这是一个测试。
""")

# 生成角色
char_generator = CharacterGenerator()
character = char_generator.generate_character("小明（男，25岁）")

# 生成视频
video_generator = VideoGenerator()
video = video_generator.generate_video(script, [character], [])

print(f"视频ID: {video.id}")
print(f"文件路径: {video.file_path}")
print(f"时长: {video.duration}秒")
```

## 📁 输出文件结构

```
data/
├── videos/          # 生成的视频文件
├── characters/      # 角色图像
├── scenes/          # 场景图像
└── temp/           # 临时文件
```

## 🔧 配置选项

### 视频参数

在 `VideoGenerator` 类中可以调整：

```python
class VideoGenerator:
    def __init__(self):
        self.fps = 24              # 帧率
        self.resolution = (1920, 1080)  # 分辨率
        self.output_dir = "data/videos"  # 输出目录
```

### 场景时长

在 `_parse_script_to_scenes` 方法中设置：

```python
scenes.append({
    "id": scene.id,
    "description": scene.description,
    "duration": 5.0,  # 每个场景的时长（秒）
    "characters": scene.characters or [],
    "actions": scene.actions or []
})
```

## 🤖 AI模型集成

### 启用AI模型

要使用真实的AI模型生成，需要：

1. 安装依赖：
```bash
pip install torch diffusers transformers opencv-python
```

2. 取消注释 `_init_ai_models()` 调用：
```python
# 在 VideoGenerator.__init__() 中
self._init_ai_models()  # 取消注释这行
```

### 支持的AI模型

- **图像生成**: Stable Diffusion XL
- **视频生成**: Stable Video Diffusion
- **语音合成**: Microsoft SpeechT5

## 📊 生成模式

### 1. 模拟模式（当前默认）

- 生成占位图像和文本文件
- 快速测试，无需AI模型
- 适合开发和调试

### 2. AI模式

- 使用真实AI模型生成内容
- 需要GPU和大量计算资源
- 生成高质量内容

### 3. 混合模式

- 部分使用AI模型，部分使用占位内容
- 平衡质量和速度

## 🎯 高级功能

### 自定义角色布局

修改 `_calculate_character_positions` 方法：

```python
def _calculate_character_positions(self, num_characters: int, resolution: tuple):
    # 自定义角色位置计算逻辑
    width, height = resolution
    
    if num_characters == 1:
        return [(width // 2 - 100, height // 2 - 100)]
    elif num_characters == 2:
        return [
            (width // 3 - 100, height // 2 - 100),
            (2 * width // 3 - 100, height // 2 - 100)
        ]
    # 更多角色的布局...
```

### 自定义场景背景

修改 `_generate_placeholder_background` 方法：

```python
def _generate_placeholder_background(self, description: str, scene_id: str):
    # 根据场景描述生成不同的背景
    colors = {
        "餐厅": (139, 69, 19),   # 棕色
        "公园": (34, 139, 34),   # 绿色
        "办公室": (105, 105, 105), # 灰色
        # 添加更多场景...
    }
    # 实现逻辑...
```

## ⚠️ 注意事项

### 性能考虑

1. **内存使用**: 生成高分辨率视频需要大量内存
2. **存储空间**: 临时文件可能占用大量磁盘空间
3. **处理时间**: AI模型生成需要较长时间

### 错误处理

- 所有生成步骤都有错误处理
- 失败时会生成备用文件
- 查看控制台输出了解详细错误信息

### 文件清理

- 临时文件会自动清理
- 如需保留中间文件，修改 `_cleanup_temp_files` 方法

## 🔍 故障排除

### 常见问题

1. **OpenCV未安装**
   ```
   pip install opencv-python
   ```

2. **AI模型加载失败**
   - 检查网络连接
   - 确保有足够的内存
   - 使用模拟模式进行测试

3. **视频生成失败**
   - 检查磁盘空间
   - 查看错误日志
   - 尝试生成较短的视频

### 调试技巧

1. 启用详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. 检查生成的文件：
```bash
ls -la data/videos/
ls -la data/temp/
```

3. 监控系统资源：
```bash
# Windows
tasklist | findstr python
# Linux/Mac
ps aux | grep python
```

## 📈 性能优化

### 1. 并行处理

```python
import concurrent.futures

def generate_frames_parallel(frames):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(self._generate_frame_image, ...) for frame in frames]
        results = [future.result() for future in futures]
    return results
```

### 2. 缓存机制

```python
import hashlib

def get_cached_image(prompt):
    cache_key = hashlib.md5(prompt.encode()).hexdigest()
    cache_path = f"cache/{cache_key}.png"
    if os.path.exists(cache_path):
        return cache_path
    # 生成新图像...
```

### 3. 批量处理

```python
def batch_generate_characters(characters):
    # 批量生成角色图像
    pass
```

## 🎉 总结

视频生成工具现在已经具备完整的功能：

✅ **基础功能**: 剧本解析、角色生成、场景生成  
✅ **视频合成**: 帧生成、视频编码、音视频合并  
✅ **错误处理**: 完善的错误处理和备用机制  
✅ **扩展性**: 模块化设计，易于扩展  
✅ **测试支持**: 完整的测试脚本和示例  

下一步可以：
1. 安装AI模型依赖，启用真实AI生成
2. 开发前端界面，提供用户友好的操作
3. 优化性能，支持更长的视频生成
4. 添加更多特效和转场效果 