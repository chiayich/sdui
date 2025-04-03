# 环境变量端口映射问题解决

**日期**: 2024-03-28
**类别**: 后端/Docker
**紧急程度**: 中

## 问题描述

在开发环境中，通过 `.devcontainer/.env` 更新后端服务端口（BACKEND_PORT）后，Docker Compose 启动服务时没有正确应用该环境变量，导致服务仍尝试绑定到默认的 8000 端口，引发"port is already allocated"错误。

## 问题分析

分析发现主要原因有两个：

1. `.env` 文件中的环境变量没有被正确加载到当前环境中
2. 启动脚本 `start-dev.sh` 没有在生成 Docker Compose 配置时正确应用环境变量

Docker Compose 虽然可以通过 `env_file` 指令加载环境变量文件，但这些变量仅在容器内部可见，不会影响主机的端口映射配置。而服务的端口映射定义在 `docker-compose.yml` 文件中，需要在启动服务前确保这些变量已经正确加载到环境中。

## 解决思路

主要解决方案包括两部分：

1. 在启动服务前显式加载 `.env` 文件中的环境变量
2. 根据加载的环境变量动态生成 Docker Compose 覆盖配置文件

通过这种方式，可以确保 Docker Compose 在启动服务时使用正确的端口映射配置，而不需要修改原始的 Docker Compose 文件或完全重建容器。

## 执行步骤

1. 修改 `start-dev.sh` 脚本，在开始位置添加环境变量加载逻辑：

```bash
# 加载环境变量
ENV_FILE="/workspace/.devcontainer/.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}加载环境变量文件: $ENV_FILE${NC}"
    set -a  # 自动导出所有变量
    source "$ENV_FILE"
    set +a
    
    # 显示关键环境变量
    echo -e "${GREEN}使用以下环境变量:${NC}"
    echo -e "FRONTEND_PORT=${FRONTEND_PORT:-5173}"
    echo -e "BACKEND_PORT=${BACKEND_PORT:-8000}"
    echo -e "POSTGRES_PORT=${POSTGRES_PORT:-5432}"
    echo -e "REDIS_PORT=${REDIS_PORT:-6379}"
else
    echo -e "${YELLOW}未找到环境变量文件，使用默认配置${NC}"
fi
```

2. 修改 `restart_service` 函数，以支持从环境变量读取端口配置：

```bash
# 如果是后端服务且环境变量中有非默认端口
elif [ "$service" = "backend" ] && [ -n "$BACKEND_PORT" ] && [ "$BACKEND_PORT" != "8000" ]; then
    echo -e "${YELLOW}使用环境变量中的端口 $BACKEND_PORT 启动 $service 服务...${NC}"
    # 创建临时的docker-compose覆盖文件
    cat > docker-compose.port-override.yml << EOF
version: '3.8'
services:
  backend:
    ports:
      - "$BACKEND_PORT:8000"
EOF
    
    # 启动服务
    if [ "$BACKGROUND" = "1" ]; then
        echo -e "${GREEN}以后台模式重启服务 $service (端口 $BACKEND_PORT)...${NC}"
        docker compose -f docker-compose.yml -f docker-compose.port-override.yml up -d $service
    else
        echo -e "${GREEN}以前台模式重启服务 $service (端口 $BACKEND_PORT)，按Ctrl+C停止...${NC}"
        docker compose -f docker-compose.yml -f docker-compose.port-override.yml up $service
    fi
    
    # 清理临时文件
    rm -f docker-compose.port-override.yml
```

3. 修改默认启动逻辑，支持从环境变量中读取端口映射：

```bash
# 如果环境变量中有自定义端口，创建临时覆盖文件
if [ -n "$FRONTEND_PORT" ] || [ -n "$BACKEND_PORT" ] || [ -n "$POSTGRES_PORT" ] || [ -n "$REDIS_PORT" ]; then
    echo -e "${YELLOW}使用自定义端口配置...${NC}"
    cat > docker-compose.env-override.yml << EOF
version: '3.8'
services:
EOF
    
    # 添加各服务配置
    # ...
    
    # 使用临时覆盖文件启动服务
    docker compose -f docker-compose.yml -f docker-compose.env-override.yml up -d
    
    # 清理临时文件
    rm -f docker-compose.env-override.yml
else
    # 使用默认配置启动
    docker compose up -d
fi
```

## 结果验证

修改完成后，通过以下步骤验证：

1. 编辑 `.devcontainer/.env` 文件，设置 `BACKEND_PORT=8001`
2. 运行 `bash /workspace/.devcontainer/start-dev.sh`
3. 观察输出，确认脚本正确加载环境变量并使用端口 8001
4. 使用 `docker ps` 检查容器的端口映射，确认后端服务映射到 8001 端口

验证结果表明，后端服务现在能够正确使用 `.env` 文件中指定的端口，不再出现端口冲突。

## 相关资源

- `docker-compose.yml`: Docker Compose 主配置文件
- `.devcontainer/.env`: 环境变量配置文件
- `.devcontainer/start-dev.sh`: 服务启动脚本

## 注意事项

1. 当 `.env` 文件被修改后，需要重新运行 `start-dev.sh` 脚本才能应用新的环境变量
2. 临时覆盖文件在使用后会被自动删除，不会影响原始配置文件
3. 本解决方案不需要完全重建容器，大大减少了开发环境配置的时间 