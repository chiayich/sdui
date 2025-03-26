# 监控系统数据持久化方案设计

**日期**: 2023-06-12
**类别**: 架构/运维
**紧急程度**: 中

## 问题描述

当前监控系统(Prometheus, Grafana, SkyWalking, Loki)使用的是Docker默认的卷存储机制，存在以下问题：

1. 数据持久性不足：容器或卷删除会导致监控历史数据丢失
2. 备份机制缺失：无法对监控数据进行定期备份和恢复
3. 存储容量限制：随着项目规模增长，默认存储方案难以扩展
4. 性能限制：在数据量增长后可能出现性能瓶颈

这些问题在开发环境中影响较小，但在测试和生产环境中可能导致重要监控数据丢失，影响问题排查和系统优化。

## 问题分析

监控系统包含多个组件，每个组件有不同的数据存储特性：

1. **Prometheus**: 
   - 存储时序数据，写入频繁
   - 默认使用本地文件系统
   - 数据增长速度取决于监控指标数量和采集频率

2. **Grafana**:
   - 存储仪表板配置、用户信息和快照
   - 默认使用SQLite
   - 数据增长较慢，但配置非常重要

3. **Loki**:
   - 存储日志数据，写入非常频繁
   - 包含索引和日志块
   - 数据增长速度快，需要良好的压缩和生命周期管理

4. **SkyWalking**:
   - 存储追踪数据和性能指标
   - 使用ElasticSearch作为存储后端
   - 数据量大且增长迅速

## 解决思路

采用多层次的持久化策略，根据不同组件的特性选择适合的存储方案：

1. **共同原则**:
   - 将配置与数据分离
   - 实现自动备份机制
   - 定义明确的数据保留策略
   - 提供监控存储状态的指标

2. **存储方案选择**:
   - 开发环境：使用主机挂载卷，便于调试和访问
   - 测试环境：使用NFS或类似的网络存储
   - 生产环境：使用云服务提供的托管存储服务

3. **组件特定策略**:
   - Prometheus: 使用远程写入功能，支持长期存储
   - Grafana: 替换SQLite为PostgreSQL数据库
   - Loki: 配置对象存储用于长期日志保存
   - SkyWalking: 优化ElasticSearch集群配置

## 执行步骤

### 1. Prometheus持久化配置

```yaml
# docker-compose.prometheus.yml
services:
  prometheus:
    # ... 现有配置 ...
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - /data/prometheus:/prometheus
    command:
      # ... 现有命令 ...
      - --storage.tsdb.retention.time=30d
      - --storage.tsdb.retention.size=50GB
      - --storage.tsdb.wal-compression
```

定期备份脚本：

```bash
#!/bin/bash
# /etc/cron.daily/backup-prometheus

DATE=$(date +%Y%m%d)
PROM_DATA="/data/prometheus"
BACKUP_DIR="/backups/prometheus"

# 创建快照
curl -XPOST http://localhost:9090/api/v1/admin/tsdb/snapshot

# 备份快照
mkdir -p $BACKUP_DIR
cp -r $PROM_DATA/snapshots/* $BACKUP_DIR/$DATE/

# 保留最近30天的备份
find $BACKUP_DIR -type d -mtime +30 -exec rm -rf {} \;
```

### 2. Grafana持久化配置

```yaml
# docker-compose.prometheus.yml
services:
  grafana:
    # ... 现有配置 ...
    environment:
      # ... 现有环境变量 ...
      - GF_DATABASE_TYPE=postgres
      - GF_DATABASE_HOST=postgres
      - GF_DATABASE_NAME=grafana
      - GF_DATABASE_USER=grafana
      - GF_DATABASE_PASSWORD=grafana_password
    volumes:
      - /data/grafana:/var/lib/grafana
```

添加PostgreSQL服务:

```yaml
services:
  postgres:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=grafana_password
      - POSTGRES_USER=grafana
      - POSTGRES_DB=grafana
    volumes:
      - postgres-data:/var/lib/postgresql/data
```

### 3. Loki持久化配置

```yaml
# docker-compose.loki.yml
services:
  loki:
    # ... 现有配置 ...
    volumes:
      - ./config/loki-config.yaml:/etc/loki/local-config.yaml:ro
      - /data/loki:/loki
```

生产环境Loki配置:

```yaml
# loki-config.yaml
storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/index_cache
    shared_store: s3
  aws:
    s3: 
      endpoint: minio:9000
      insecure: true
      bucketnames: loki-data
      access_key_id: minio
      secret_access_key: minio123
      s3forcepathstyle: true

compactor:
  working_directory: /loki/compactor
  shared_store: s3
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150

limits_config:
  retention_period: 90d
```

### 4. SkyWalking持久化配置

```yaml
# docker-compose.skywalking.yml
services:
  elasticsearch:
    # ... 现有配置 ...
    volumes:
      - /data/elasticsearch:/usr/share/elasticsearch/data
    environment:
      # ... 现有环境变量 ...
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
```

ElasticSearch索引生命周期管理:

```json
PUT _ilm/policy/skywalking-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_age": "1d",
            "max_size": "50gb"
          }
        }
      },
      "warm": {
        "min_age": "2d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "7d",
        "actions": {
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

## 结果验证

1. **数据保留测试**:
   - 验证Prometheus数据在指定时间范围内可查询
   - 确认Loki日志保留符合配置要求
   - 测试SkyWalking追踪数据保留期限

2. **备份恢复测试**:
   - 模拟故障并从备份恢复Prometheus数据
   - 验证Grafana配置备份与恢复
   - 测试从对象存储恢复Loki日志

3. **性能测试**:
   - 在高负载下测量查询响应时间
   - 监控存储系统资源使用率
   - 评估配置调整对性能的影响

## 相关资源

- [Prometheus存储文档](https://prometheus.io/docs/prometheus/latest/storage/)
- [Grafana数据库配置](https://grafana.com/docs/grafana/latest/administration/configuration/#database)
- [Loki存储配置](https://grafana.com/docs/loki/latest/configuration/examples/)
- [SkyWalking存储文档](https://skywalking.apache.org/docs/main/v9.0.0/en/setup/backend/backend-storage/)

## 注意事项

1. 在实施存储更改前，确保已备份现有数据
2. 监控组件的数据增长速率，及时调整存储容量
3. 定期测试备份恢复流程
4. 生产环境应使用加密和访问控制保护监控数据
5. 考虑监控数据合规性和隐私问题 