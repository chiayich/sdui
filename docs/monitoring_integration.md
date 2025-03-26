# SDUI 监控系统集成指南

本文档介绍如何将 SDUI 项目与监控系统集成，包括如何配置和自动化启动监控服务。

## 配置文件

SDUI 项目使用 JSON 格式的配置文件来控制监控系统。配置文件位于项目根目录：

```
/workspace/config.json
```

如果配置文件不存在，系统将使用默认配置：

```
/workspace/monitoring/default-config.json
```

### 配置文件结构

```json
{
    "monitoring": {
        "enabled": true,          // 是否启用监控系统
        "services": {             // 启用哪些监控服务
            "prometheus": true,   // 指标监控
            "grafana": true,      // 可视化仪表盘
            "skywalking": true,   // 分布式追踪
            "loki": true,         // 日志收集
            "kafka": false,       // 消息队列
            "elk": false          // 生产环境日志系统
        },
        "retention": {            // 数据保留策略
            "prometheus": "15d",  // Prometheus数据保留15天
            "loki": "7d",         // Loki日志保留7天
            "elasticsearch": "30d" // ES数据保留30天
        }
    }
}
```

## 自动启动监控

开发容器配置为在启动时检查监控配置。如果 `monitoring.enabled` 设置为 `true`，将自动启动配置的监控服务。

这是通过在 `.devcontainer/devcontainer.json` 中的 `postStartCommand` 实现的。

## 手动控制监控

您也可以使用监控启动脚本手动控制监控服务：

```bash
# 启动监控服务
/workspace/monitoring/start-monitoring.sh

# 停止所有监控服务
cd /workspace/monitoring && docker compose down

# 停止特定服务
cd /workspace/monitoring && docker compose stop prometheus grafana
```

## 监控系统端点

监控服务启动后，可通过以下地址访问：

| 服务          | 地址                  | 说明                       |
| ------------- | --------------------- | -------------------------- |
| Prometheus    | http://localhost:9090 | 指标收集和查询             |
| Grafana       | http://localhost:9092 | 可视化仪表盘 (admin/admin) |
| SkyWalking UI | http://localhost:9093 | 分布式追踪和APM            |
| Loki          | http://localhost:9094 | 日志聚合 (通过Grafana访问) |

## 集成到应用

### 后端集成

1. **添加指标收集**:

```python
# 在FastAPI应用中添加Prometheus指标
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# 添加Prometheus指标
Instrumentator().instrument(app).expose(app)
```

2. **添加分布式追踪**:

```python
# 集成SkyWalking
from skywalking import agent

# 在应用启动前初始化
agent.start(
    service_name="backend-service",
    collector_address="localhost:11800"
)
```

3. **配置结构化日志**:

```python
# 配置结构化日志
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "line": record.lineno
        }
        if hasattr(record, 'props'):
            log_record.update(record.props)
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# 使用示例
logger = logging.getLogger("app")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

# 输出日志
logger.info("用户登录", extra={"props": {"user_id": 123, "ip": "192.168.1.1"}})
```

### 前端集成

1. **添加前端性能监控**:

```typescript
// 添加SkyWalking浏览器监控
import ClientMonitor from 'skywalking-client-js';

ClientMonitor.register({
  service: 'frontend-service',
  pagePath: location.href,
  serviceVersion: 'v1.0.0',
  collector: {
    url: 'http://localhost:9093/browser/perfData',
  }
});
```

2. **添加前端日志收集**:

```typescript
// 前端日志服务
export default {
  info(message, data = {}) {
    this.log('INFO', message, data);
  },
  
  error(message, error = null, data = {}) {
    this.log('ERROR', message, error, data);
  },
  
  log(level, message, error = null, data = {}) {
    const logData = {
      level,
      message,
      timestamp: new Date().toISOString(),
      data
    };
    
    if (error) {
      logData.error = error.toString();
      logData.stack = error.stack;
    }
    
    // 开发环境输出到控制台
    console.log(logData);
    
    // 发送到后端API
    fetch('/api/logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logData)
    }).catch(err => console.error('Failed to send log:', err));
  }
};
```

## 自定义监控配置

### 自定义Prometheus配置

修改 `/workspace/monitoring/prometheus/config/prometheus.yml` 添加新的抓取目标。

### 自定义Grafana仪表盘

通过Grafana UI创建仪表盘，然后保存为JSON文件到 `/workspace/monitoring/prometheus/dashboards/` 目录。

### 自定义Loki配置

修改 `/workspace/monitoring/loki/config/loki-config.yaml` 和 `/workspace/monitoring/loki/config/promtail-config.yaml` 调整日志收集配置。

## 故障排查

### 权限问题

如果遇到Docker权限问题，请参考 [Docker-in-Docker配置指南](docker_in_docker_setup.md)。

### 端口冲突

如果监控服务端口与其他服务冲突，可修改 `/workspace/monitoring/prometheus/docker-compose.prometheus.yml` 等文件中的端口映射配置。

### 日志无法收集

确保应用日志输出到正确位置，并检查 Promtail 配置是否正确匹配日志路径。 