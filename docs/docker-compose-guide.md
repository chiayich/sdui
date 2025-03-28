# Docker Compose 服务管理指南

本文档提供了使用Docker Compose管理SDUI项目服务的简明指南，替代之前复杂的脚本管理方式。

## 启动服务

### 使用启动脚本（推荐）

开发容器启动时会自动以前台模式运行所有服务。如果需要手动启动，可以使用：

```bash
# 前台模式（默认，可以看到所有日志）
bash /workspace/.devcontainer/start-dev.sh

# 后台模式
BACKGROUND=1 bash /workspace/.devcontainer/start-dev.sh

# 重启服务（前台模式）
bash /workspace/.devcontainer/start-dev.sh restart

# 重启服务（后台模式）
BACKGROUND=1 bash /workspace/.devcontainer/start-dev.sh restart
```

启动脚本已增强，会自动检查并尝试释放被占用的端口，解决常见的端口冲突问题。

### 直接使用Docker Compose命令

```bash
# 前台模式（可查看所有日志）
cd /workspace
docker compose up

# 后台模式
cd /workspace
docker compose up -d

# 重启服务
cd /workspace
docker compose down
docker compose up -d  # 或不加 -d 使用前台模式
```

## 基本命令

### 查看服务状态

```bash
docker compose ps
```

### 查看服务日志

查看所有服务的日志：

```bash
docker compose logs
```

实时查看所有服务的日志：

```bash
docker compose logs -f
```

查看特定服务的日志：

```bash
docker compose logs frontend  # 只查看前端服务日志
docker compose logs backend   # 只查看后端服务日志
docker compose logs -f db     # 实时查看数据库日志
```

### 停止服务

```bash
docker compose stop          # 停止所有服务
docker compose stop frontend # 只停止前端服务
```

### 重启服务

```bash
docker compose restart          # 重启所有服务
docker compose restart backend  # 只重启后端服务
```

### 完全关闭并移除容器

```bash
docker compose down
```

### 重建容器并启动

当需要应用Dockerfile或docker-compose.yml的更改时：

```bash
docker compose up --build
```

## 常见场景

### 开发模式（推荐）

在开发过程中，推荐使用前台模式运行服务，以便实时查看所有日志：

```bash
docker compose up
```

如果需要在后台运行某些服务，但同时想要查看特定服务的日志：

```bash
# 先在后台启动所有服务
docker compose up -d

# 然后查看特定服务的日志
docker compose logs -f frontend
```

### 调试数据库

```bash
# 查看数据库日志
docker compose logs -f db

# 连接到数据库容器
docker compose exec db psql -U postgres
```

### 监控服务管理

启动监控服务：

```bash
docker compose -f monitoring/docker-compose.yml up -d
```

查看监控服务日志：

```bash
docker compose -f monitoring/docker-compose.yml logs -f
```

## 访问服务

各服务的访问地址：

| 服务       | 地址                       | 说明            |
| ---------- | -------------------------- | --------------- |
| 前端       | http://localhost:5174      | Vue开发服务器   |
| 后端API    | http://localhost:8000      | FastAPI服务器   |
| API文档    | http://localhost:8000/docs | Swagger API文档 |
| Prometheus | http://localhost:9090      | 监控指标收集    |
| Grafana    | http://localhost:9091      | 监控数据可视化  |
| Loki       | http://localhost:9094      | 日志聚合系统    |

## 常见问题

### 端口冲突问题

如果遇到类似以下错误：

```
Error response from daemon: driver failed programming external connectivity: Bind for 0.0.0.0:8000 failed: port is already allocated
```

表示端口已被占用。解决方法：

1. **使用启动脚本的restart命令**：
   ```bash
   bash /workspace/.devcontainer/start-dev.sh restart
   ```
   脚本会自动检测并尝试释放被占用的端口

2. **手动释放端口**：
   ```bash
   # 查找占用端口的进程
   lsof -i :8000
   
   # 终止进程
   kill -9 <PID>
   ```

3. **修改端口映射**：
   如果无法释放端口，可以修改`.env`或`.devcontainer/.env`文件中的端口配置：
   ```
   BACKEND_PORT=8001  # 修改为未被占用的端口
   ```

### Docker存储空间不足

如果遇到存储空间问题，可以清理未使用的Docker资源：

```bash
# 删除所有未使用的容器、网络、镜像和卷
docker system prune -a --volumes

# 仅删除未使用的镜像
docker image prune -a
```

## 注意事项

1. 首次启动或依赖项变更后，可能需要使用`--build`参数重建容器。
2. 通过`docker-compose.override.yml`可以自定义本地开发环境配置，不影响版本控制。
3. 如果发现端口冲突，可以修改`.devcontainer/.env`文件中的端口配置。
4. 挂载的数据卷会保留数据，即使容器被删除。如需完全清理，需要手动删除卷：`docker compose down -v`

## 服务管理命令

### 启动服务

1. 前台模式启动所有服务（可查看日志输出）:
   ```bash
   bash /workspace/.devcontainer/start-dev.sh
   ```

2. 后台模式启动所有服务:
   ```bash
   BACKGROUND=1 bash /workspace/.devcontainer/start-dev.sh
   ```

### 重启服务

1. 重启所有服务（前台模式）:
   ```bash
   bash /workspace/.devcontainer/start-dev.sh restart
   ```

2. 重启所有服务（后台模式）:
   ```bash
   BACKGROUND=1 bash /workspace/.devcontainer/start-dev.sh restart
   ```

3. 只重启特定服务（前台模式）:
   ```bash
   # 只重启后端服务
   bash /workspace/.devcontainer/start-dev.sh restart backend
   
   # 只重启前端服务
   bash /workspace/.devcontainer/start-dev.sh restart frontend
   
   # 只重启数据库服务
   bash /workspace/.devcontainer/start-dev.sh restart db
   
   # 只重启Redis服务
   bash /workspace/.devcontainer/start-dev.sh restart redis
   ```

4. 只重启特定服务（后台模式）:
   ```bash
   # 只重启后端服务（后台模式）
   BACKGROUND=1 bash /workspace/.devcontainer/start-dev.sh restart backend
   ```

### 使用替代端口启动服务

当遇到端口冲突且无法释放时，可以使用替代端口启动服务：

```bash
# 使用8001端口启动后端服务
bash /workspace/.devcontainer/start-dev.sh alt-port backend 8001

# 后台模式下使用替代端口
BACKGROUND=1 bash /workspace/.devcontainer/start-dev.sh alt-port backend 8001
```

> **注意**：使用替代端口后，需要相应地更新依赖该服务的其他配置。

### 使用Docker Compose直接管理

如果不使用脚本，也可以直接使用Docker Compose命令:

1. 启动所有服务（后台模式）:
   ```bash
   docker compose up -d
   ```

2. 启动所有服务（前台模式）:
   ```bash
   docker compose up
   ```

3. 停止所有服务:
   ```bash
   docker compose down
   ```

4. 重启特定服务:
   ```bash
   docker compose stop backend
   docker compose rm -f backend
   docker compose up -d backend
   ```

5. 查看服务日志:
   ```bash
   # 查看所有服务日志
   docker compose logs -f
   
   # 查看特定服务日志
   docker compose logs -f backend
   ``` 