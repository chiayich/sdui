#!/bin/bash
set -e

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 加载环境变量
ENV_FILE="/workspace/.devcontainer/.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}加载环境变量文件: $ENV_FILE${NC}"
    set -a  # 自动导出所有变量
    source "$ENV_FILE"
    set +a
    
    # 显示监控相关环境变量
    echo -e "${GREEN}使用以下环境变量:${NC}"
    echo -e "PROMETHEUS_PORT=${PROMETHEUS_PORT:-9090}"
    echo -e "GRAFANA_PORT=${GRAFANA_PORT:-9091}"
    echo -e "SKYWALKING_PORT=${SKYWALKING_PORT:-9093}"
    echo -e "LOKI_PORT=${LOKI_PORT:-9094}"
else
    echo -e "${YELLOW}未找到环境变量文件，使用默认配置${NC}"
fi

# 定义配置文件路径
CONFIG_FILE="/workspace/config.json"
DEFAULT_CONFIG_FILE="/workspace/monitoring/default-config.json"

# 打印标题
echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}   SDUI 监控服务启动脚本   ${NC}"
echo -e "${GREEN}====================================${NC}"

# 检查Docker是否可用
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}错误: Docker 不可用!${NC}"
    echo -e "${YELLOW}请确保 Docker socket 已挂载且权限正确。${NC}"
    echo -e "${YELLOW}参考文档: /workspace/docs/docker_in_docker_setup.md${NC}"
    exit 1
fi

# 确保在监控目录下
cd "$(dirname "$0")"

# 读取配置文件，如果不存在使用默认配置
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}全局配置文件不存在，使用默认配置...${NC}"
    
    # 检查默认配置是否存在，不存在则创建
    if [ ! -f "$DEFAULT_CONFIG_FILE" ]; then
        echo -e "${YELLOW}创建默认配置文件...${NC}"
        cat > "$DEFAULT_CONFIG_FILE" << EOL
{
    "monitoring": {
        "enabled": true,
        "services": {
            "prometheus": true,
            "grafana": true,
            "skywalking": true,
            "loki": true,
            "kafka": false,
            "elk": false
        }
    }
}
EOL
    fi
    CONFIG_FILE="$DEFAULT_CONFIG_FILE"
fi

# 检查jq是否可用，用于解析JSON
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}安装jq工具...${NC}"
    apt-get update && apt-get install -y jq
fi

# 读取配置
echo -e "${YELLOW}读取监控配置...${NC}"
MONITORING_ENABLED=$(jq -r '.monitoring.enabled // false' "$CONFIG_FILE")

if [ "$MONITORING_ENABLED" != "true" ]; then
    echo -e "${YELLOW}监控服务未启用，如需启用请在配置文件中设置 monitoring.enabled=true${NC}"
    exit 0
fi

# 读取各服务配置
PROMETHEUS_ENABLED=$(jq -r '.monitoring.services.prometheus // false' "$CONFIG_FILE")
GRAFANA_ENABLED=$(jq -r '.monitoring.services.grafana // false' "$CONFIG_FILE")
SKYWALKING_ENABLED=$(jq -r '.monitoring.services.skywalking // false' "$CONFIG_FILE")
LOKI_ENABLED=$(jq -r '.monitoring.services.loki // false' "$CONFIG_FILE")
KAFKA_ENABLED=$(jq -r '.monitoring.services.kafka // false' "$CONFIG_FILE")
ELK_ENABLED=$(jq -r '.monitoring.services.elk // false' "$CONFIG_FILE")

# 构建启动命令
SERVICES=""
[ "$PROMETHEUS_ENABLED" == "true" ] && SERVICES="$SERVICES prometheus"
[ "$GRAFANA_ENABLED" == "true" ] && SERVICES="$SERVICES grafana"
[ "$SKYWALKING_ENABLED" == "true" ] && SERVICES="$SERVICES skywalking"
[ "$LOKI_ENABLED" == "true" ] && SERVICES="$SERVICES loki"
[ "$KAFKA_ENABLED" == "true" ] && SERVICES="$SERVICES kafka"
[ "$ELK_ENABLED" == "true" ] && SERVICES="$SERVICES elk"

# 检查是否有服务需要启动
if [ -z "$SERVICES" ]; then
    echo -e "${YELLOW}未配置任何监控服务，请在配置文件中启用至少一个服务${NC}"
    exit 0
fi

# 使用唯一的网络名称，避免冲突
NETWORK_NAME="sdui-monitoring"

# 如果网络已存在，先删除它
echo -e "${YELLOW}检查监控网络: ${NETWORK_NAME}${NC}"
if docker network inspect ${NETWORK_NAME} &> /dev/null; then
    echo -e "${YELLOW}移除已存在的网络...${NC}"
    docker network rm ${NETWORK_NAME} || true
fi

# 创建网络
echo -e "${YELLOW}创建监控网络: ${NETWORK_NAME}${NC}"
docker network create ${NETWORK_NAME}

# 设置COMPOSE_PROJECT_NAME避免名称冲突
export COMPOSE_PROJECT_NAME="sdui-monitoring-$(date +%s)"

# 如果环境变量中有自定义端口，创建临时覆盖文件
if [ -n "$PROMETHEUS_PORT" ] || [ -n "$GRAFANA_PORT" ] || [ -n "$SKYWALKING_PORT" ] || [ -n "$LOKI_PORT" ]; then
    echo -e "${YELLOW}使用自定义端口配置...${NC}"
    cat > docker-compose.env-override.yml << EOF
version: '3.8'
services:
EOF
    
    # 添加Prometheus服务配置
    if [ -n "$PROMETHEUS_PORT" ]; then
        cat >> docker-compose.env-override.yml << EOF
  prometheus:
    ports:
      - "${PROMETHEUS_PORT}:9090"
EOF
    fi
    
    # 添加Grafana服务配置
    if [ -n "$GRAFANA_PORT" ]; then
        cat >> docker-compose.env-override.yml << EOF
  grafana:
    ports:
      - "${GRAFANA_PORT}:3000"
EOF
    fi
    
    # 添加SkyWalking服务配置
    if [ -n "$SKYWALKING_PORT" ]; then
        cat >> docker-compose.env-override.yml << EOF
  ui:
    ports:
      - "${SKYWALKING_PORT}:8080"
EOF
    fi
    
    # 添加Loki服务配置
    if [ -n "$LOKI_PORT" ]; then
        cat >> docker-compose.env-override.yml << EOF
  loki:
    ports:
      - "${LOKI_PORT}:3100"
EOF
    fi
    
    # 启动监控服务，使用临时覆盖文件
    echo -e "${GREEN}启动监控服务: $SERVICES${NC}"
    docker compose -f docker-compose.yml -f docker-compose.env-override.yml up -d $SERVICES --remove-orphans
    
    # 清理临时文件
    rm -f docker-compose.env-override.yml
else
    # 启动监控服务
    echo -e "${GREEN}启动监控服务: $SERVICES${NC}"
    docker compose -f docker-compose.yml up -d $SERVICES --remove-orphans
fi

# 检查启动状态
echo -e "${YELLOW}检查服务状态...${NC}"
sleep 3
docker compose -f docker-compose.yml ps

echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}   监控服务状态   ${NC}"
echo -e "${GREEN}====================================${NC}"

# 显示访问地址，使用环境变量中的端口
if [ "$PROMETHEUS_ENABLED" == "true" ]; then
    echo -e "${GREEN}Prometheus 地址: ${NC}http://localhost:${PROMETHEUS_PORT:-9090}"
fi

if [ "$GRAFANA_ENABLED" == "true" ]; then
    echo -e "${GREEN}Grafana 地址: ${NC}http://localhost:${GRAFANA_PORT:-9091} ${YELLOW}(用户名/密码: admin/admin)${NC}"
fi

if [ "$SKYWALKING_ENABLED" == "true" ]; then
    echo -e "${GREEN}SkyWalking UI 地址: ${NC}http://localhost:${SKYWALKING_PORT:-9093}"
fi

if [ "$LOKI_ENABLED" == "true" ]; then
    echo -e "${GREEN}Loki 地址: ${NC}http://localhost:${LOKI_PORT:-9094} ${YELLOW}(通过Grafana访问)${NC}"
fi

if [ "$KAFKA_ENABLED" == "true" ]; then
    echo -e "${GREEN}Kafka UI 地址: ${NC}http://localhost:8080"
fi

if [ "$ELK_ENABLED" == "true" ]; then
    echo -e "${GREEN}Kibana 地址: ${NC}http://localhost:5601"
fi

echo -e "${GREEN}====================================${NC}"
echo -e "${YELLOW}完整监控使用指南: ${NC}docs/monitoring_guide.md"
echo -e "${GREEN}====================================${NC}" 