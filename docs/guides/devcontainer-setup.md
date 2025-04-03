# SDUI框架开发容器设置指南

**日期**: 2023-05-29
**类别**: 开发环境
**紧急程度**: 中

## 开发容器介绍

本项目提供了完整的开发容器配置，使用VS Code的Remote Containers扩展或GitHub Codespaces可以快速创建一致的开发环境。开发容器包含了所有必要的工具和依赖，包括Python、Node.js、PostgreSQL和Redis。

## 环境要求

- Docker 20.10+
- VS Code 1.60+
- Remote - Containers扩展

或者：
- GitHub账号（使用Codespaces）

## 使用方法

### 本地使用VS Code Remote Containers

1. 确保已安装所需软件：
   - Docker Desktop
   - Visual Studio Code
   - Remote - Containers扩展

2. 克隆仓库并打开VS Code
```bash
git clone https://github.com/yourusername/sdui-framework.git
cd sdui-framework
code .
```

3. 当VS Code提示"Folder contains a Dev Container configuration file"时，点击"Reopen in Container"。
   或者手动点击左下角的绿色图标，选择"Reopen in Container"。

4. 等待容器构建和初始化完成（首次构建可能需要几分钟）。

### 使用GitHub Codespaces

1. 在GitHub仓库页面，点击"Code"按钮，然后选择"Open with Codespaces"。

2. 点击"New codespace"创建一个新的Codespace。

3. 等待Codespace创建和初始化完成。

## 开发容器特性

开发环境配置了以下特性：

- Python 3.11环境
- Node.js 18.x
- PostgreSQL 14 客户端和服务器
- Redis服务器
- VS Code扩展：
  - Python和TypeScript/Vue.js开发工具
  - Docker工具
  - Git工具
  - 代码格式化工具
- 自动格式化和代码检查（通过pre-commit）
- 开发服务器自动启动

## 端口映射

以下端口会自动映射到本地机器：

- 5173: 前端开发服务器(Vite)
- 8000: 后端API服务器(FastAPI)
- 6379: Redis服务器
- 5432: PostgreSQL服务器

## 初始化流程

容器启动时会自动执行以下初始化步骤：

1. 创建PostgreSQL数据库结构
2. 创建必要的表和插入测试数据
3. 安装前端和后端依赖
4. 配置Git pre-commit钩子
5. 启动开发服务器

## 常见问题

### 问题: PostgreSQL连接问题

解决方案:
```
在容器中连接PostgreSQL时，使用主机名"db"而非"localhost"，例如：
psql -h db -U postgres -d sdui
```

### 问题: 前端开发服务器未自动启动

解决方案:
```
cd /workspace/frontend
npm run dev
```

### 问题: 后端开发服务器未自动启动

解决方案:
```
cd /workspace/backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 自定义开发容器

如需自定义开发容器，可编辑以下文件：

- `.devcontainer/devcontainer.json`: 容器配置、扩展和设置
- `.devcontainer/docker-compose.yml`: 服务配置
- `.devcontainer/Dockerfile`: 开发容器构建定义
- `.devcontainer/init.sh`: 容器初始化脚本

修改这些文件后，需要重新构建容器（在VS Code中使用"Rebuild Container"命令）。 