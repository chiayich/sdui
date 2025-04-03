# SDUI框架

基于FastAPI和Vue3的服务器驱动UI框架，实现跨平台一致的UI渲染和动态界面更新。

## 系统概述

本项目实现了一个完整的SDUI（Server-Driven UI）框架，包含后端API、前端渲染引擎和相关工具。通过该框架，可以实现：

- 服务端定义UI结构和内容
- 客户端负责渲染UI
- 无需应用发版即可更新UI
- 支持A/B测试和个性化内容
- 跨平台一致的UI体验

## 技术架构

### 后端技术

- **FastAPI**: 高性能的异步Python API框架
- **PostgreSQL**: 用于存储UI模板和组件数据
- **Redis**: 提供缓存支持
- **Docker**: 容器化部署

### 前端技术

- **Vue 3**: 渐进式JavaScript框架
- **Vite**: 现代前端构建工具
- **Pinia**: Vue状态管理库
- **TypeScript**: 类型安全保障

## 环境配置指南

### 开发容器环境 (推荐)

本项目支持VS Code开发容器和GitHub Codespaces，提供完整的开发环境。

1. 使用VS Code打开项目
2. 当提示"Folder contains a Dev Container configuration file"时，点击"Reopen in Container"
3. 等待容器构建和初始化完成
4. 开发服务器将自动启动

更多详情请参阅 [开发容器设置指南](docs/guides/devcontainer-setup.md)

### Docker环境配置

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
    docker compose up -d
    ```

4. 访问应用

    - 前端: [http://localhost:5173](http://localhost:5173) (或您在.env中配置的FRONTEND_PORT)
    - API: [http://localhost:8000](http://localhost:8000) (或您在.env中配置的BACKEND_PORT)
    - API文档: [http://localhost:8000/docs](http://localhost:8000/docs) (或您在.env中配置的BACKEND_PORT)

更多详情请参阅 [Docker设置指南](docs/guides/docker-setup.md)

### 本地开发环境

#### 后端服务配置

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

#### 前端服务配置

1. 安装依赖

    ```bash
    cd frontend
    npm install
    ```

2. 启动开发服务器

    ```bash
    npm run dev
    ```

## 项目目录结构

```
.
├── backend/                # 后端应用
│   ├── app/               # 应用代码
│   │   ├── db/           # 数据库模型和工具
│   │   ├── routers/      # API路由
│   │   ├── services/     # 业务服务
│   │   └── middleware/   # 中间件
│   └── requirements.txt   # Python依赖
├── frontend/              # 前端应用
│   ├── src/              # 源代码
│   │   ├── components/   # Vue组件
│   │   ├── stores/       # Pinia状态
│   │   ├── views/        # 页面视图
│   │   └── types/        # TypeScript类型
│   └── package.json      # NPM配置
├── docs/                  # 文档
│   ├── architecture/     # 架构设计文档
│   ├── development/      # 开发文档
│   ├── guides/           # 使用指南
│   └── problems/         # 问题解决方案
├── postgres-init/        # 数据库初始化
│   ├── schemas/          # 数据库模式
│   └── data/            # 示例数据
├── monitoring/           # 监控系统配置
├── .devcontainer/        # 开发容器配置
└── docker-compose.yml    # Docker配置
```

## 系统文档

### 架构设计文档

- [SDUI渲染器实现](docs/architecture/2025-03-28-sdui-renderer-implementation.md)
- [SDUI存储设计](docs/architecture/2025-03-28-sdui-storage-design-summary.md)
- [页面数据存储设计](docs/architecture/2025-03-28-sdui-page-data-storage-design.md)
- [监控系统架构](docs/architecture/monitoring_architecture.md)

### 开发指南文档

- [开发容器设置](docs/guides/devcontainer-setup.md)
- [Docker环境配置](docs/guides/docker-setup.md)
- [日志管理](docs/guides/log_management.md)
- [端口配置](docs/guides/port-configuration.md)

### 监控系统文档

- [监控系统使用指南](docs/architecture/monitoring_guide.md)
- [监控系统集成](docs/architecture/monitoring_integration.md)

## 服务端口配置

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

### 自动端口分配

项目提供了端口自动配置功能，详见 [端口配置指南](docs/guides/port-configuration.md)。

## 系统监控

SDUI 框架包含完整的监控和追踪系统，包括 Prometheus, Grafana, SkyWalking 和 Loki。详细配置和使用说明请参考：

- [监控系统架构](docs/architecture/monitoring_architecture.md)
- [监控系统使用指南](docs/architecture/monitoring_guide.md)
- [监控系统集成](docs/architecture/monitoring_integration.md)

## 开源许可

MIT
