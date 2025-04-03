# SDUI 框架日志管理

## 概述

SDUI框架集成了一套完整的日志管理系统，包括：

1. **应用服务日志**：前端和后端应用产生的日志
2. **基础设施日志**：包括数据库、Redis等基础服务的日志
3. **监控服务日志**：Prometheus、Grafana、Loki等监控组件的日志

本文档介绍如何使用SDUI框架中的日志查看工具和Loki日志聚合系统来高效管理和排查问题。

## 日志文件位置

在开发环境中，各服务的日志存储位置如下：

- **前端日志**：`/tmp/frontend.log`
- **后端日志**：`/tmp/backend.log`
- **数据库日志**：通过Docker容器访问
- **Redis日志**：通过Docker容器访问
- **监控服务日志**：通过Docker容器访问

## 日志查看工具

SDUI框架提供了一个强大的命令行日志查看工具，可以方便地查看、过滤和跟踪所有服务的日志。

### 基本用法

```bash
# 查看帮助信息
.devcontainer/log_viewer.sh -h

# 查看前端日志
.devcontainer/log_viewer.sh -f

# 查看后端日志
.devcontainer/log_viewer.sh -b

# 查看所有服务日志
.devcontainer/log_viewer.sh -a

# 持续查看前端和后端日志（类似于tail -f）
.devcontainer/log_viewer.sh -f -b -t

# 查看前端和后端日志中包含"error"的内容
.devcontainer/log_viewer.sh -f -b -g error

# 查看监控服务日志
.devcontainer/log_viewer.sh -m
```

### 工具参数说明

日志查看工具支持以下参数：

- `-a, --all`：显示所有服务的日志
- `-f, --frontend`：显示前端服务日志
- `-b, --backend`：显示后端服务日志
- `-d, --db`：显示数据库日志
- `-r, --redis`：显示Redis日志
- `-m, --monitoring`：显示监控服务日志(Grafana,Prometheus,Loki)
- `-g, --grep PATTERN`：过滤显示包含指定模式的日志行
- `-l, --lines LINES`：显示每个日志的行数(默认: 50)
- `-t, --tail`：持续显示日志更新(类似tail -f)
- `-c, --clear`：清除所有日志文件
- `-h, --help`：显示帮助信息

### 集成到服务管理工具

日志查看工具已集成到SDUI服务管理工具中，可以通过以下命令快速访问：

```bash
.devcontainer/sdui_services.sh logs
```

## Loki 日志聚合系统

除了命令行工具外，SDUI框架还集成了Grafana Loki作为日志聚合系统，提供更强大的日志检索和可视化能力。

### Loki 架构

SDUI框架中的Loki系统由以下组件组成：

- **Loki**：负责存储和查询日志
- **Promtail**：负责收集容器日志并发送给Loki
- **Grafana**：提供日志可视化界面

### 访问Loki日志

1. 确保监控服务已启动：
   ```bash
   /workspace/monitoring/start-monitoring.sh
   ```

2. 访问Grafana界面：http://localhost:9091 (用户名/密码: admin/admin)

3. 在Grafana中选择"Explore"菜单

4. 在数据源下拉框中选择"Loki"

5. 使用LogQL查询语法搜索日志，例如：
   ```
   {container=~"sdui.*"}
   ```

### 常用LogQL查询示例

```
# 查询所有容器的日志
{container=~"sdui.*"}

# 查询特定容器的日志
{container="sdui-frontend"}

# 查询包含错误的日志
{container=~"sdui.*"} |= "error"

# 查询特定时间范围内的日志
{container=~"sdui.*"} | logfmt | time > "2023-03-20T10:00:00Z"

# 统计错误次数
sum(count_over_time({container=~"sdui.*"} |= "error"[1h])) by (container)
```

## 日志最佳实践

为了更有效地使用日志系统进行问题排查，建议遵循以下最佳实践：

1. **合理设置日志级别**：开发环境使用DEBUG级别，生产环境使用INFO级别

2. **结构化日志**：使用JSON格式记录结构化数据，便于后期分析

3. **包含上下文信息**：日志中包含请求ID、用户ID等上下文信息，便于追踪问题

4. **关注错误和警告**：定期查看ERROR和WARNING级别的日志，及时发现问题

5. **设置告警**：对关键错误设置告警规则，及时通知开发团队

## 故障排查

当遇到系统问题时，可以按照以下步骤使用日志工具进行排查：

1. 查看应用服务日志中的错误：
   ```bash
   .devcontainer/log_viewer.sh -f -b -g "error|exception|fail" -t
   ```

2. 检查相关基础设施日志：
   ```bash
   .devcontainer/log_viewer.sh -d -r -g "error" -t
   ```

3. 如果涉及监控服务问题，查看监控服务日志：
   ```bash
   .devcontainer/log_viewer.sh -m -g "error" -t
   ```

4. 使用Loki进行更复杂的日志分析，例如查找特定时间段内的错误模式。

## 总结

SDUI框架的日志管理系统提供了全面的日志收集、查看和分析能力，帮助开发团队高效排查问题。通过命令行工具和Loki系统的结合使用，可以满足从简单查看到复杂分析的各种需求。 