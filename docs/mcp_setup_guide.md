# MCP工具配置指南

## 什么是MCP？

MCP (Model Context Protocol) 是一个开放协议，允许AI助手访问外部工具和数据源。在Cursor中，MCP工具可以大大提升开发效率。

## 配置步骤

### 1. 安装MCP工具

```bash
# 方法1: 使用npm全局安装
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-terminal
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-web-search

# 方法2: 使用项目本地安装
npm install
```

### 2. 配置API密钥

#### GitHub API密钥
1. 访问 https://github.com/settings/tokens
2. 创建新的Personal Access Token
3. 选择需要的权限：repo, read:user, read:email
4. 复制token并替换配置文件中的 `your_github_token_here`

#### Web Search API密钥
1. 访问 https://serper.dev/
2. 注册账号并获取API密钥
3. 替换配置文件中的 `your_serper_api_key_here`

### 3. Cursor设置

1. 打开Cursor设置 (Ctrl+,)
2. 搜索 "MCP" 或 "Model Context Protocol"
3. 启用MCP功能
4. 配置MCP服务器路径

## 可用的MCP工具

### 1. File System MCP
- **功能**: 文件系统操作
- **用途**: 批量处理文件、管理项目结构
- **示例**: 
  - 批量重命名角色图片
  - 整理视频文件
  - 清理临时文件

### 2. Terminal MCP
- **功能**: 命令行操作
- **用途**: 自动化脚本执行、环境管理
- **示例**:
  - 启动FastAPI服务
  - 运行AI模型训练
  - 安装Python依赖

### 3. GitHub MCP
- **功能**: GitHub仓库管理
- **用途**: 代码版本控制、Issue管理
- **示例**:
  - 查看提交历史
  - 创建Pull Request
  - 管理Issues

### 4. Web Search MCP
- **功能**: 网络搜索
- **用途**: 技术调研、问题解决
- **示例**:
  - 搜索最新的AI模型
  - 查找技术文档
  - 解决编程问题

## 使用示例

### 文件管理示例
```
请帮我整理data/characters目录下的所有角色图片，按创建时间排序
```

### 终端操作示例
```
请启动后端服务并检查GPU状态
```

### GitHub操作示例
```
请查看最近的提交历史，并创建一个新的分支用于视频生成功能
```

### 网络搜索示例
```
请搜索最新的Stable Video Diffusion模型信息
```

## 故障排除

### 常见问题

1. **MCP工具未响应**
   - 检查Node.js版本是否兼容
   - 确认MCP工具已正确安装
   - 重启Cursor

2. **API密钥错误**
   - 验证API密钥是否正确
   - 检查密钥权限是否足够
   - 确认网络连接正常

3. **权限问题**
   - 确保有足够的文件系统权限
   - 检查GitHub token权限设置

## 最佳实践

1. **安全性**: 不要在代码中硬编码API密钥
2. **效率**: 合理使用MCP工具，避免过度依赖
3. **备份**: 定期备份重要的MCP配置
4. **更新**: 保持MCP工具版本最新

## 项目特定配置

针对AI视频生成项目，建议的MCP工具使用场景：

1. **模型管理**: 使用File System MCP管理AI模型文件
2. **视频处理**: 使用Terminal MCP自动化视频处理流程
3. **数据管理**: 使用File System MCP整理角色和场景数据
4. **技术调研**: 使用Web Search MCP获取最新AI技术信息 