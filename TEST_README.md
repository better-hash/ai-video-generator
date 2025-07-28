# 🧪 AI模型测试程序使用指南

本目录包含了针对AI视频生成项目中各个模型的专门测试程序，帮助您验证模型是否正确安装和配置。

## 📋 测试程序列表

### 1. 单独模型测试

#### 🎨 `test_stable_diffusion_xl.py`
**功能**: 测试Stable Diffusion XL图像生成模型
- 加载SDXL模型
- 生成多种风格的测试图像
- 保存生成结果到 `data/test_outputs/sdxl/`
- 验证图像生成质量和性能

```bash
python test_stable_diffusion_xl.py
```

#### 🎬 `test_stable_video_diffusion.py`
**功能**: 测试Stable Video Diffusion视频生成模型
- 加载SVD模型
- 从静态图像生成视频帧序列
- 支持现有图像或自动生成测试图像
- 保存帧序列和视频文件到 `data/test_outputs/svd/`

```bash
python test_stable_video_diffusion.py
```

#### 🎤 `test_speecht5_tts.py`
**功能**: 测试SpeechT5语音合成模型
- 加载SpeechT5 TTS模型和声码器
- 生成英文和中文语音
- 测试不同说话人嵌入
- 保存音频文件到 `data/test_outputs/tts/`

```bash
python test_speecht5_tts.py
```

### 2. 综合测试

#### 🤖 `test_all_models.py`
**功能**: 完整的系统测试和模型验证
- 检查系统要求和依赖库
- 验证模型下载状态
- 运行所有单独模型测试
- 测试模块集成功能
- 生成详细的测试报告

```bash
python test_all_models.py
```

#### ⚡ `test_models_quick.py`
**功能**: 快速模型加载验证（不进行实际生成）
- 快速检查所有模型是否能正确加载
- 验证GPU/CPU配置
- 检查内存使用情况
- 适合日常快速检查

```bash
python test_models_quick.py
```

## 🚀 使用建议

### 首次安装后
1. **运行快速测试**: `python test_models_quick.py`
2. **运行综合测试**: `python test_all_models.py`
3. **根据需要运行单独测试**

### 日常开发
1. **快速验证**: `python test_models_quick.py`
2. **功能验证**: 运行相关的单独测试

### 问题排查
1. **系统问题**: `python test_all_models.py`
2. **特定模型问题**: 运行对应的单独测试

## 📊 测试输出

### 输出目录结构
```
data/test_outputs/
├── sdxl/                 # SDXL生成的图像
│   ├── sdxl_test_1_*.png
│   └── ...
├── svd/                  # SVD生成的视频帧
│   ├── svd_test_1_*/
│   │   ├── frame_000.png
│   │   ├── frame_001.png
│   │   └── video.mp4
│   └── ...
├── tts/                  # TTS生成的音频
│   ├── tts_test_1_*.wav
│   ├── speaker_*.wav
│   └── ...
├── test_report_*.txt     # 综合测试报告
└── quick_test_*.txt      # 快速测试报告
```

## ⚙️ 系统要求

### 最低要求
- **Python**: 3.8+
- **内存**: 16GB RAM
- **存储**: 30GB 可用空间
- **网络**: 稳定的互联网连接（首次下载模型）

### 推荐配置
- **GPU**: 8GB+ VRAM (NVIDIA GPU with CUDA)
- **内存**: 32GB RAM
- **存储**: 50GB+ 可用空间
- **CPU**: 8核心+

### GPU支持
- **CUDA**: 11.8+ (推荐)
- **支持的GPU**: RTX 3060+, RTX 4060+, A100, V100等
- **CPU模式**: 支持但速度较慢

## 🔧 依赖库

确保安装了所有必要的依赖：

```bash
# 安装基础依赖
pip install -r requirements.txt

# 或者安装核心AI库
pip install torch diffusers transformers accelerate safetensors
pip install pillow opencv-python soundfile scipy numpy
```

## 🐛 常见问题

### 1. 模型下载失败
**问题**: 网络连接问题或Hugging Face访问受限
**解决方案**:
- 检查网络连接
- 使用VPN或镜像源
- 手动下载模型文件

### 2. GPU内存不足
**问题**: CUDA out of memory
**解决方案**:
- 关闭其他GPU程序
- 使用CPU模式
- 减少批处理大小

### 3. 依赖库冲突
**问题**: 版本不兼容
**解决方案**:
- 使用虚拟环境
- 更新到推荐版本
- 检查CUDA版本兼容性

### 4. 音频保存失败
**问题**: soundfile或scipy未安装
**解决方案**:
```bash
pip install soundfile scipy
```

## 📈 性能优化

### GPU优化
- 使用混合精度 (fp16)
- 启用内存优化
- 适当的批处理大小

### CPU优化
- 增加线程数
- 使用优化的BLAS库
- 减少模型精度

## 🔍 调试技巧

### 1. 详细日志
```bash
# 启用详细日志
TORCH_LOGS=+dynamo python test_all_models.py
```

### 2. 内存监控
```bash
# 监控GPU内存
nvidia-smi -l 1
```

### 3. 性能分析
```python
# 在代码中添加性能分析
import torch.profiler
with torch.profiler.profile() as prof:
    # 模型推理代码
    pass
print(prof.key_averages().table())
```

## 📞 获取帮助

如果遇到问题：
1. 查看测试报告中的错误信息
2. 检查系统要求和依赖
3. 参考项目文档
4. 提交Issue并附上测试报告

## 🎯 下一步

测试通过后，您可以：
1. 运行完整的视频生成流程
2. 自定义模型参数
3. 集成到您的应用中
4. 进行性能优化

---

**注意**: 首次运行测试时，模型会自动从Hugging Face下载，可能需要较长时间。请确保网络连接稳定。