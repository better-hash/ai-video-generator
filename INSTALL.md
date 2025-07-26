# AI视频生成工具 - 安装指南

## 🚀 快速开始

### 1. 环境要求

- **Python**: 3.9 或更高版本
- **操作系统**: Windows 10/11, macOS, Linux
- **内存**: 至少 8GB RAM (推荐 16GB+)
- **存储**: 至少 10GB 可用空间
- **GPU**: 可选，但推荐 NVIDIA GPU (用于AI模型加速)

### 2. 安装步骤

#### 步骤1: 克隆项目
```bash
git clone <repository-url>
cd video_agent
```

#### 步骤2: 创建虚拟环境 (推荐)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 步骤3: 安装依赖
```bash
# 方法1: 使用项目脚本
python start_project.py --install

# 方法2: 手动安装核心依赖
pip install fastapi uvicorn pydantic requests Pillow numpy

# 方法3: 安装完整依赖 (如果方法1失败)
pip install -r backend/requirements_simple.txt
```

#### 步骤4: 初始化项目
```bash
python start_project.py --setup
```

#### 步骤5: 运行测试
```bash
python test_basic.py
```

### 3. 启动服务

#### 启动后端服务
```bash
python start_project.py --backend
```
访问: http://localhost:8000/docs

#### 启动前端服务
```bash
python start_project.py --frontend
```
访问: http://localhost:3000

## 🔧 故障排除

### 编码问题 (Windows)
如果遇到编码错误，请尝试：

1. 使用简化的requirements文件：
```bash
pip install -r backend/requirements_simple.txt
```

2. 分步安装核心依赖：
```bash
pip install fastapi uvicorn pydantic requests Pillow numpy
```

### 依赖安装失败
如果某些包安装失败，可以跳过：

```bash
# 安装核心功能包
pip install fastapi uvicorn pydantic requests Pillow numpy

# 可选：安装AI相关包 (需要更多时间)
pip install torch torchvision transformers diffusers
```

### 权限问题
如果遇到权限错误：

```bash
# Windows (以管理员身份运行)
pip install --user fastapi uvicorn

# macOS/Linux
sudo pip install fastapi uvicorn
```

## 📦 依赖说明

### 核心依赖
- **FastAPI**: Web框架
- **Uvicorn**: ASGI服务器
- **Pydantic**: 数据验证
- **Requests**: HTTP客户端
- **Pillow**: 图像处理
- **NumPy**: 数值计算

### AI模型依赖 (可选)
- **Torch**: PyTorch深度学习框架
- **Transformers**: Hugging Face模型库
- **Diffusers**: 扩散模型库
- **OpenCV**: 计算机视觉库

### 数据库依赖 (可选)
- **SQLAlchemy**: ORM框架
- **Redis**: 缓存数据库
- **PostgreSQL**: 关系数据库

## 🎯 验证安装

运行测试脚本验证安装：

```bash
python test_basic.py
```

如果看到以下输出，说明安装成功：

```
🎬 AI视频生成工具 - 基础功能测试
==================================================
🧪 测试基本导入...
✅ FastAPI 导入成功
✅ Uvicorn 导入成功
✅ Pydantic 导入成功
✅ Requests 导入成功
✅ Pillow 导入成功
✅ NumPy 导入成功

📁 创建示例数据...
✅ 创建目录: data
✅ 创建目录: data/characters
✅ 创建目录: data/scenes
✅ 创建目录: data/videos
✅ 创建示例剧本文件

🧪 测试剧本解析功能...
✅ 剧本标题: 浪漫晚餐
✅ 角色数量: 2
✅ 场景数量: 1
✅ 对话数量: 4

🧪 测试角色生成功能...
✅ 生成角色: 小明
✅ 生成角色: 小丽

🎉 所有基础功能测试通过！
```

## 📚 下一步

1. **查看文档**: 阅读 `docs/` 目录下的技术文档
2. **启动服务**: 运行 `python start_project.py --backend`
3. **测试API**: 访问 http://localhost:8000/docs
4. **开发功能**: 根据需求扩展项目功能

## 💡 提示

- 首次运行可能需要下载AI模型，请耐心等待
- 建议在虚拟环境中运行项目
- 如果遇到问题，请查看错误日志或联系技术支持 