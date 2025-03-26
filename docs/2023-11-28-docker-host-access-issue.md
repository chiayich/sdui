# Docker主机访问和挂载问题解决

**日期**: 2023-11-28
**类别**: 工具/DevOps
**紧急程度**: 高

## 问题描述

监控服务无法启动，出现两个主要问题：

1. Docker客户端配置错误 - 尝试连接到错误位置 (`/Users/huajin/.docker/run/docker.sock` 而不是 `/var/run/docker.sock`)
2. Docker文件挂载失败 - 错误 `Mounts denied: The path /workspace/monitoring/loki/config/loki-config.yaml is not shared from the host and is not known to Docker`

这些问题导致监控服务无法启动，影响了开发环境中的监控能力。

## 问题分析

1. **Docker客户端配置问题**：
   - Docker客户端被配置为使用macOS主机上的Docker套接字，而不是容器内的套接字
   - `.docker/config.json` 中的 `credsStore` 设置为 "desktop"，试图使用宿主机的凭证存储
   - `currentContext` 设置为 "desktop-linux"，指向不可用的上下文

2. **文件挂载问题**：
   - 在Docker-in-Docker环境中，容器内路径 `/workspace/monitoring/...` 无法被正确挂载
   - Docker Desktop的文件共享限制阻止了访问这些路径
   - 相对路径挂载在Docker-in-Docker环境中不可靠

## 解决思路

针对上述问题，我们采取以下解决策略：

1. **修正Docker客户端配置**：
   - 修改 `.docker/config.json` 移除 `credsStore` 配置
   - 将 `currentContext` 设置为 "default"
   - 添加 `DOCKER_HOST` 环境变量，确保连接到正确的Docker套接字

2. **简化服务配置**：
   - 移除依赖文件挂载的配置
   - 使用服务默认配置而不是自定义配置文件
   - 保留数据卷以确保数据持久化

## 执行步骤

1. **修复Docker客户端配置**：

```bash
# 编辑 ~/.docker/config.json
{
	"auths": {},
	"currentContext": "default"
}

# 在 ~/.bashrc 中添加环境变量
export DOCKER_HOST=unix:///var/run/docker.sock
```

2. **简化Loki配置，避免挂载问题**：

```yaml
services:
  loki:
    image: grafana/loki:2.8.0
    container_name: sdui-loki
    restart: unless-stopped
    ports:
      - "9094:3100"
    volumes:
      - loki-data:/loki
    # 使用默认配置，避免挂载问题
    networks:
      - sdui-monitoring
```

3. **简化Prometheus配置，避免挂载问题**：

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: sdui-prometheus
    restart: unless-stopped
    volumes:
      - prometheus-data:/prometheus
    # 使用默认配置，避免挂载问题
    ports:
      - "9090:9090"
    networks:
      - sdui-monitoring
```

4. **重新网络设置和启动服务**：

```bash
# 删除现有网络
docker network rm sdui-monitoring

# 使用修改后的配置启动服务
./start-monitoring.sh
```

## 结果验证

修复后，服务成功启动：

```
启动监控服务:  prometheus grafana loki
[+] Running 6/6
 ✔ Volume "sdui-monitoring-1743016859_prometheus-data"  Created
 ✔ Volume "sdui-monitoring-1743016859_loki-data"        Created
 ✔ Volume "sdui-monitoring-1743016859_grafana-data"     Created
 ✔ Container sdui-loki                                  Started
 ✔ Container sdui-prometheus                            Started
 ✔ Container sdui-grafana                               Started
```

所有服务都能正常启动，并可通过配置的端口访问：
- Prometheus: http://localhost:9090
- Grafana: http://localhost:9092
- Loki: http://localhost:9094 (通过Grafana访问)

## 相关资源

- [Docker-in-Docker最佳实践](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
- [Docker Desktop文件共享文档](https://docs.docker.com/desktop/settings/mac/#file-sharing)
- 修改的文件:
  - `/home/vscode/.docker/config.json`
  - `/home/vscode/.bashrc`
  - `/workspace/monitoring/loki/docker-compose.loki.yml`
  - `/workspace/monitoring/prometheus/docker-compose.prometheus.yml`

## 注意事项

1. **环境变量持久化**：确保在容器重启后 `DOCKER_HOST` 环境变量依然有效，最好将其添加到 `.bashrc` 文件中。

2. **配置简化的影响**：移除自定义配置文件意味着使用服务的默认配置，可能需要在后续优化中通过其他方式（如环境变量或启动参数）提供自定义配置。

3. **开发容器重建**：如果开发容器重建，需要再次检查和配置Docker客户端设置，可考虑将这些配置添加到开发容器的初始化脚本中。

4. **网络管理**：使用 `export COMPOSE_PROJECT_NAME="sdui-monitoring-$(date +%s)"` 为容器资源添加时间戳前缀，以避免容器名称和资源冲突。 