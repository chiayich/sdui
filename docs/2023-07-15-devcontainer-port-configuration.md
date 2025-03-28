# 开发容器端口冲突问题解决

**日期**: 2023-07-15
**类别**: 开发工具
**紧急程度**: 中

## 问题描述

在使用开发容器（devcontainer）进行开发时，由于宿主机上可能已经运行了一些服务（如PostgreSQL、Redis等），导致容器启动时出现端口冲突问题，无法正常启动全部服务。

## 问题分析

Docker容器映射端口时，如果宿主机上指定的端口已被占用，就会导致服务启动失败。由于不同开发者的本地环境可能运行着不同的服务，需要一个灵活的方式来配置服务端口，以适应不同的开发环境。

主要冲突点：
- PostgreSQL默认使用5432端口
- Redis默认使用6379端口
- 前端开发服务器和后端API服务器也可能与开发者本地其他项目冲突

## 解决思路

通过环境变量来配置服务端口，允许开发者根据自己的本地环境灵活调整各服务的端口映射，而不需要修改代码。

具体方案：
1. 修改docker-compose.yml文件，使用环境变量配置端口映射
2. 创建.env.example示例文件，提供配置参考
3. 更新开发容器启动脚本，支持从环境变量读取端口配置
4. 调整VS Code开发容器配置，确保端口映射正确

## 执行步骤

1. 修改docker-compose.yml文件，使用环境变量配置端口：

```yaml
services:
  # 后端API服务
  sdui-api:
    ports:
      - "${BACKEND_PORT:-8000}:8000"
    # ...

  # 前端服务
  sdui-web:
    ports:
      - "${FRONTEND_PORT:-5173}:5173"
    # ...

  # Redis缓存服务
  redis:
    ports:
      - "${REDIS_PORT:-6379}:6379"
    # ...
```

2. 创建.env.example文件：

```bash
# 前端开发服务器端口 (默认: 5173)
# FRONTEND_PORT=3000

# 后端API服务器端口 (默认: 8000)
# BACKEND_PORT=8001

# PostgreSQL数据库端口 (默认: 5432)
# POSTGRES_PORT=5433

# Redis缓存端口 (默认: 6379)
# REDIS_PORT=6380
```

3. 更新开发容器启动脚本：

```bash
# 加载环境变量
if [ -f /workspace/.devcontainer/.env ]; then
    source /workspace/.devcontainer/.env
fi

# 设置默认端口
FRONTEND_PORT=${FRONTEND_PORT:-5173}
BACKEND_PORT=${BACKEND_PORT:-8000}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
REDIS_PORT=${REDIS_PORT:-6379}

# 使用这些端口
nohup npm run dev -- --host 0.0.0.0 --port ${FRONTEND_PORT} > /tmp/frontend.log 2>&1 &
nohup uvicorn app.main:app --host 0.0.0.0 --port ${BACKEND_PORT} --reload > /tmp/backend.log 2>&1 &
```

4. 更新README.md文件，添加端口配置说明：

```markdown
## 端口配置

为了避免端口冲突，本项目支持通过环境变量自定义服务端口：

| 服务          | 默认端口 | 环境变量           |
| ------------- | -------- | ------------------ |
| 前端开发服务器 | 5173     | FRONTEND_PORT      |
| 后端API服务器  | 8000     | BACKEND_PORT       |
| PostgreSQL    | 5432     | POSTGRES_PORT      |
| Redis         | 6379     | REDIS_PORT         |
```

5. 创建端口配置文档，详细说明配置方法和常见问题

## 结果验证

1. 将开发容器配置拉取到本地环境
2. 创建自定义.env文件，配置不同的端口
3. 重启开发容器，验证服务是否正常启动
4. 确认所有服务都使用了配置中指定的端口

测试表明，通过环境变量可以成功自定义各服务的端口，解决了端口冲突问题。

## 相关资源

- [修改后的docker-compose.yml](../docker-compose.yml)
- [开发容器配置](../.devcontainer/devcontainer.json)
- [端口配置指南](./port-configuration.md)
- [环境变量示例](../.env.example)

## 注意事项

1. .env文件包含本地环境特定的配置，不应该提交到版本控制系统
2. 团队成员应该根据自己的本地环境创建自定义的.env文件
3. 修改端口后，需要重启相关服务才能生效
4. 如果修改了后端API端口，可能需要相应地更新前端的API_URL配置 