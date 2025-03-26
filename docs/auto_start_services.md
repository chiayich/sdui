# 开发容器自动启动服务实现文档

**日期**: 2023-11-28
**类别**: 工具/DevOps
**紧急程度**: 中

## 概述

本文档描述了SDUI框架开发容器中的服务自动启动机制实现，包括前端服务、后端API和监控系统的自动启动配置。这些自动化机制确保开发者在重建容器后能立即开始工作，无需手动启动各个服务。

## 实现方案

自动启动服务通过以下组件实现：

1. **专用启动脚本** - `.devcontainer/start_services.sh`
2. **开发容器配置** - `.devcontainer/devcontainer.json`中的postStartCommand配置
3. **进程管理机制** - 使用PID文件和日志重定向

### 启动脚本功能

专用启动脚本具有以下功能：

1. **清理已存在服务** - 检测并停止可能已运行的服务进程
2. **前端服务启动** - 启动Vue前端开发服务器（端口3000）
3. **后端服务启动** - 启动FastAPI后端服务（端口8000）
4. **监控服务启动** - 根据配置文件决定是否启动监控服务
5. **状态反馈** - 提供清晰的启动状态和访问地址信息
6. **日志管理** - 将服务日志重定向到指定文件

### 自动启动机制

在开发容器的生命周期中，有两个关键时刻可以执行脚本：

1. **postCreateCommand** - 在容器首次创建后执行（只执行一次）
   - 用于环境初始化和依赖安装

2. **postStartCommand** - 在容器每次启动时执行（包括重建后）
   - 用于启动开发服务和监控服务

## 配置详解

### 启动脚本

`/workspace/.devcontainer/start_services.sh` 脚本的关键部分：

```bash
# 启动前端服务
cd /workspace/frontend
nohup npm run dev -- --host 0.0.0.0 --port 3000 > /tmp/frontend.log 2>&1 &
echo $! > /tmp/frontend.pid

# 启动后端服务
cd /workspace/backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
echo $! > /tmp/backend.pid

# 检查是否需要启动监控服务
if [ -f /workspace/config.json ] && [ "$(jq -r '.monitoring.enabled // false' /workspace/config.json)" == "true" ]; then
    /workspace/monitoring/start-monitoring.sh
fi
```

### 容器配置

`/workspace/.devcontainer/devcontainer.json` 中的自动启动配置：

```json
{
    "postCreateCommand": "bash /usr/local/bin/init.sh",
    "postStartCommand": "bash /workspace/.devcontainer/start_services.sh"
}
```

## 端口配置

为了避免端口冲突，项目采用以下端口规划：

| 服务       | 端口 | 说明           |
| ---------- | ---- | -------------- |
| 前端服务   | 3000 | Vue开发服务器  |
| 后端API    | 8000 | FastAPI服务    |
| Prometheus | 9090 | 指标收集和查询 |
| Grafana    | 9091 | 可视化仪表盘   |
| SkyWalking | 9093 | 分布式追踪     |
| Loki       | 9094 | 日志聚合       |

## 使用方法

### 查看服务状态

开发容器启动后，所有服务应自动启动。可以通过以下方式查看状态：

```bash
# 检查前端服务进程
ps aux | grep "npm run dev"

# 检查后端服务进程
ps aux | grep "uvicorn"

# 检查监控服务容器
docker ps | grep sdui-
```

### 手动启动服务

如果需要手动启动服务：

```bash
# 启动所有服务
bash /workspace/.devcontainer/start_services.sh

# 或单独启动前端
cd /workspace/frontend && npm run dev -- --host 0.0.0.0 --port 3000

# 或单独启动后端
cd /workspace/backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 或单独启动监控服务
/workspace/monitoring/start-monitoring.sh
```

### 查看服务日志

```bash
# 查看前端服务日志
tail -f /tmp/frontend.log

# 查看后端服务日志
tail -f /tmp/backend.log

# 查看监控服务日志
docker logs -f sdui-grafana
docker logs -f sdui-prometheus
```

## 故障排查

### 服务未自动启动

如果服务未自动启动，尝试以下步骤：

1. 检查是否有权限问题：
   ```bash
   ls -la /workspace/.devcontainer/start_services.sh
   # 确保有执行权限，如果没有则添加
   chmod +x /workspace/.devcontainer/start_services.sh
   ```

2. 手动执行启动脚本：
   ```bash
   bash /workspace/.devcontainer/start_services.sh
   ```

3. 检查日志文件中的错误：
   ```bash
   cat /tmp/frontend.log
   cat /tmp/backend.log
   ```

### 端口占用问题

如果端口已被占用，修改配置文件中的端口映射：

1. 前端端口修改 - `/workspace/.devcontainer/start_services.sh`
2. 后端端口修改 - `/workspace/.devcontainer/start_services.sh`
3. 监控端口修改 - `/workspace/monitoring/prometheus/docker-compose.prometheus.yml` 