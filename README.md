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

2. 自定义端口配置（可选）
```bash
# 复制示例环境配置文件
cp .devcontainer/.env.example .devcontainer/.env

# 编辑 .env 文件，根据需要修改端口号
nano .devcontainer/.env
```

3. 启动服务
```bash
docker-compose up -d
```

4. 访问应用
- 前端: http://localhost:5173 (或您在.env中配置的FRONTEND_PORT)
- API: http://localhost:8000 (或您在.env中配置的BACKEND_PORT)
- API文档: http://localhost:8000/docs (或您在.env中配置的BACKEND_PORT)

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

## 端口配置

为了避免端口冲突，本项目支持通过环境变量自定义服务端口：

| 服务          | 默认端口 | 环境变量           |
| ------------- | -------- | ------------------ |
| 前端开发服务器 | 5173     | FRONTEND_PORT      |
| 后端API服务器  | 8000     | BACKEND_PORT       |
| PostgreSQL    | 5432     | POSTGRES_PORT      |
| Redis         | 6379     | REDIS_PORT         |
| Prometheus    | 9090     | PROMETHEUS_PORT    |
| Grafana       | 9091     | GRAFANA_PORT       |
| SkyWalking UI | 9093     | SKYWALKING_PORT    |
| Loki          | 9094     | LOKI_PORT          |

### 自动端口配置

项目提供了一个自动检查宿主机端口占用情况并生成配置的脚本：

```bash
# 运行端口检查脚本
./check_ports.sh
```

此脚本会检查默认端口是否被占用，并自动生成`.devcontainer/.env`文件，为被占用的端口分配替代端口。运行脚本后，重新构建开发容器即可应用新的端口配置。

您也可以通过复制 `.devcontainer/.env.example` 为 `.devcontainer/.env` 并手动修改其中的值来自定义端口。

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