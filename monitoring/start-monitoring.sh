#!/bin/bash
set -e

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

# 启动监控服务
echo -e "${GREEN}启动监控服务: $SERVICES${NC}"
docker compose -f docker-compose.yml up -d $SERVICES --remove-orphans

# 检查启动状态
echo -e "${YELLOW}检查服务状态...${NC}"
sleep 3
docker compose -f docker-compose.yml ps

echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}   监控服务状态   ${NC}"
echo -e "${GREEN}====================================${NC}"

# 显示访问地址
if [ "$PROMETHEUS_ENABLED" == "true" ]; then
    echo -e "${GREEN}Prometheus 地址: ${NC}http://localhost:9090"
fi

if [ "$GRAFANA_ENABLED" == "true" ]; then
    echo -e "${GREEN}Grafana 地址: ${NC}http://localhost:9091 ${YELLOW}(用户名/密码: admin/admin)${NC}"
fi

if [ "$SKYWALKING_ENABLED" == "true" ]; then
    echo -e "${GREEN}SkyWalking UI 地址: ${NC}http://localhost:9093"
fi

if [ "$LOKI_ENABLED" == "true" ]; then
    echo -e "${GREEN}Loki 地址: ${NC}http://localhost:9094 ${YELLOW}(通过Grafana访问)${NC}"
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