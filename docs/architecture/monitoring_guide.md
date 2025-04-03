# SDUI 监控系统使用指南

## 端口配置

为避免与开发环境中的其他服务冲突，监控系统使用以下端口:

| 服务           | 端口        | 访问地址               |
| -------------- | ----------- | ---------------------- |
| Prometheus     | 9090        | http://localhost:9090  |
| Grafana        | 9091        | http://localhost:9091  |
| SkyWalking UI  | 9093        | http://localhost:9093  |
| Loki           | 9094        | http://localhost:9094  |
| Node Exporter  | 9100        | http://localhost:9100  |
| SkyWalking OAP | 11800/12800 | http://localhost:11800 |
| Elasticsearch  | 9200/9300   | http://localhost:9200  |

## 启动监控系统

在宿主机（不是开发容器内）执行以下命令启动监控系统:

```bash
cd monitoring
docker compose up -d prometheus grafana skywalking loki
```

## 访问监控面板

### Grafana (指标和日志可视化)

访问 [http://localhost:9091](http://localhost:9091)

- 默认用户名: `admin`
- 默认密码: `admin`

Grafana已预配置了以下数据源:
- Prometheus (指标监控)
- Loki (日志聚合)
- SkyWalking (APM数据)

### SkyWalking UI (分布式追踪)

访问 [http://localhost:9093](http://localhost:9093)

在SkyWalking UI中，你可以:
- 查看服务拓扑图
- 跟踪请求调用链
- 分析服务性能指标

### Prometheus (指标查询)

访问 [http://localhost:9090](http://localhost:9090)

Prometheus提供了强大的PromQL查询语言，可用于:
- 查询自定义指标
- 设置告警规则
- 分析性能趋势

## 常见场景使用指南

### 1. 链路追踪查询

1. 打开 SkyWalking UI (http://localhost:9093)
2. 导航到 "Trace" 页面
3. 设置搜索条件:
   - 服务名称
   - 时间范围
   - 关键词
   - 最小持续时间
4. 查看搜索结果并点击特定追踪ID查看详情
5. 在追踪视图中，可以看到:
   - 完整的调用链
   - 每个调用的时间开销
   - 调用关系图
   - 关联的日志

### 2. 系统指标监控

1. 打开 Grafana (http://localhost:9091)
2. 导航到预配置的仪表板:
   - "System Metrics" - 基础设施指标
   - "Service Metrics" - 应用服务指标
   - "JVM Metrics" - Java应用性能
   - "Node.js Metrics" - Node.js应用性能
3. 查看实时和历史指标数据
4. 使用时间选择器调整查看时间范围

### 3. 日志查询和分析

1. 打开 Grafana (http://localhost:9091)
2. 点击左侧菜单的 "Explore"
3. 选择 "Loki" 数据源
4. 使用LogQL查询语言:
   - `{app="backend"}` - 查询后端服务日志
   - `{app="frontend"}` - 查询前端服务日志
   - `{app="backend"} |= "error"` - 查询包含"error"的后端日志
   - `{app="backend"} |~ "error|warning"` - 使用正则表达式查询
5. 点击日志条目查看详情
6. 利用标签筛选和时间范围缩小结果范围

## 故障排查指南

### 服务无法访问

1. 检查Docker容器是否正在运行:
   ```bash
   docker ps | grep sdui
   ```

2. 查看容器日志:
   ```bash
   docker logs sdui-grafana
   docker logs sdui-skywalking-ui
   docker logs sdui-loki
   docker logs sdui-prometheus
   ```

3. 确认端口没有被其他服务占用:
   ```bash
   netstat -tuln | grep 909
   ```

### 追踪数据未显示

1. 确认应用已正确配置SkyWalking Agent
2. 检查OAP服务是否正常:
   ```bash
   docker logs sdui-skywalking-oap
   ```
3. 验证应用和OAP服务之间的网络连接

### 日志未收集

1. 检查日志文件路径是否正确
2. 确认Promtail配置正确:
   ```bash
   docker logs sdui-promtail
   ```
3. 验证Loki服务是否正常:
   ```bash
   docker logs sdui-loki
   ```

## 开发环境集成

### 后端服务集成

1. 添加SkyWalking Agent依赖:
   ```python
   pip install apache-skywalking
   ```

2. 在应用入口添加:
   ```python
   from skywalking import agent
   
   agent.start(
       service_name="your-service-name",
       collector_address="localhost:11800"
   )
   ```

3. 添加Prometheus指标收集:
   ```python
   from prometheus_fastapi_instrumentator import Instrumentator
   
   app = FastAPI()
   
   # 添加Prometheus指标
   Instrumentator().instrument(app).expose(app)
   ```

### 前端服务集成

1. 添加SkyWalking前端监控:
   ```bash
   npm install skywalking-client-js
   ```

2. 在应用入口添加:
   ```javascript
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