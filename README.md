# SDUI框架

基于FastAPI和Vue3的服务器驱动UI框架，实现跨平台一致的UI渲染和动态界面更新。

## 项目概述

本项目实现了一个完整的SDUI（Server-Driven UI）框架，包含后端API、前端渲染引擎和相关工具。通过该框架，可以实现：

- 服务端定义UI结构和内容
- 客户端负责渲染UI
- 无需应用发版即可更新UI
- 支持A/B测试和个性化内容
- 跨平台一致的UI体验

## 技术栈

### 后端
- **FastAPI**: 高性能的异步Python API框架
- **PostgreSQL**: 用于存储UI模板和组件数据
- **Redis**: 提供缓存支持
- **Docker**: 容器化部署

### 前端
- **Vue 3**: 渐进式JavaScript框架
- **Vite**: 现代前端构建工具
- **Pinia**: Vue状态管理库
- **TypeScript**: 类型安全保障

## 快速开始

### 方法1: 使用开发容器 (推荐)

本项目支持VS Code开发容器和GitHub Codespaces，提供完整的开发环境。

1. 使用VS Code打开项目
2. 当提示"Folder contains a Dev Container configuration file"时，点击"Reopen in Container"
3. 等待容器构建和初始化完成
4. 开发服务器将自动启动

更多详情请参阅 [开发容器设置指南](docs/devcontainer-setup.md)

### 方法2: 使用Docker Compose

1. 克隆仓库
```bash
git clone https://github.com/yourusername/sdui-framework.git
cd sdui-framework
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问应用
- 前端: http://localhost:5173
- API: http://localhost:8000
- API文档: http://localhost:8000/docs

更多详情请参阅 [Docker设置指南](docs/docker-setup.md)

### 方法3: 本地开发设置

#### 后端

1. 创建虚拟环境
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 启动开发服务器
```bash
uvicorn app.main:app --reload
```

#### 前端

1. 安装依赖
```bash
cd frontend
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

## 项目结构

```
.
├── backend/                # 后端应用
├── frontend/               # 前端应用
├── docs/                   # 文档
├── .cursor/                # Cursor配置
│   ├── mcp/                # MCP服务配置
│   └── rules/              # Cursor规则
├── .devcontainer/          # 开发容器配置
└── docker-compose.yml      # Docker配置
```

## 文档

- [开发容器设置指南](docs/devcontainer-setup.md)
- [Docker设置指南](docs/docker-setup.md)
- [数据库Schema设置](docs/2023-05-27-sdui-database-schema-setup.md)

## 监控系统

SDUI 框架包含完整的监控和追踪系统，包括 Prometheus, Grafana, SkyWalking 和 Loki。

### 端口配置

为避免与开发服务冲突，监控系统使用以下端口:

| 服务          | 端口 | 访问地址              |
| ------------- | ---- | --------------------- |
| Prometheus    | 9090 | http://localhost:9090 |
| Grafana       | 9092 | http://localhost:9092 |
| SkyWalking UI | 9093 | http://localhost:9093 |
| Loki          | 9094 | http://localhost:9094 |

详细使用指南见 [监控系统使用指南](docs/monitoring_guide.md)。

## 许可证

MIT 