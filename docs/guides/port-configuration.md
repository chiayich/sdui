# 端口配置指南

为了避免开发环境和不同服务之间的端口冲突，SDUI框架提供了灵活的端口配置方案。

## 环境变量配置

SDUI框架使用环境变量控制各服务的端口映射。您可以通过以下步骤自定义端口配置：

1. 复制示例环境配置文件：

```bash
# 对于项目根目录的Docker Compose配置
cp .env.example .env

# 对于开发容器配置
cp .devcontainer/.env.example .devcontainer/.env
```

2. 根据您的需要编辑 `.env` 文件：

```
# 编辑项目根目录的环境变量
nano .env

# 编辑开发容器的环境变量
nano .devcontainer/.env
```

## 可用配置选项

| 服务            | 默认端口 | 环境变量           | 说明               |
|----------------|----------|------------------|-------------------|
| 前端开发服务器   | 5173     | FRONTEND_PORT    | Vite开发服务器端口  |
| 后端API服务器    | 8000     | BACKEND_PORT     | FastAPI服务器端口  |
| PostgreSQL      | 5432     | POSTGRES_PORT    | 数据库端口         |
| Redis           | 6379     | REDIS_PORT       | 缓存服务端口       |
| Prometheus      | 9090     | PROMETHEUS_PORT  | 监控服务端口       |
| Grafana         | 9091     | GRAFANA_PORT     | 可视化面板端口     |
| SkyWalking UI   | 9093     | SKYWALKING_PORT  | 链路追踪UI端口     |
| Loki            | 9094     | LOKI_PORT        | 日志聚合服务端口   |

## 注意事项

1. 端口修改后，需要重新启动相关服务才能生效：

```bash
# 重启项目根目录的服务
docker-compose down
docker-compose up -d

# 重新构建开发容器
# 在VS Code中: Ctrl+Shift+P > "Remote-Containers: Rebuild Container"
```

2. 修改端口后，您可能需要相应地调整：

   - 前端服务的API_URL配置（如果修改了后端端口）
   - 监控服务的配置（如果修改了监控相关端口）
   - 其他服务之间的互连配置

3. 在团队开发中，`.env` 文件通常不会提交到版本控制系统。这样，团队中的每个开发者都可以根据自己的本地环境需求配置端口。

## 排查端口冲突

如果您遇到端口冲突，通常会看到类似以下的错误信息：

```
Error starting userland proxy: listen tcp 0.0.0.0:5432: bind: address already in use
```

遇到这种情况，您可以：

1. 使用 `lsof` 或 `netstat` 命令查看哪个进程占用了端口：

```bash
# 在macOS/Linux上
lsof -i :5432
netstat -an | grep 5432

# 在Windows上
netstat -ano | findstr 5432
```

2. 在 `.env` 文件中修改相应的端口配置，使用未被占用的端口

3. 重新启动服务 