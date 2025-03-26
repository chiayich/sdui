#!/bin/bash
set -e

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}      SDUI 开发服务启动脚本         ${NC}"
echo -e "${GREEN}=====================================${NC}"

# 停止可能已存在的服务
echo -e "${YELLOW}正在清理可能运行的旧服务...${NC}"
if [ -f /tmp/frontend.pid ]; then
    pid=$(cat /tmp/frontend.pid)
    if kill -0 $pid 2>/dev/null; then
        echo -e "停止旧的前端服务 (PID: $pid)"
        kill $pid
    fi
    rm /tmp/frontend.pid
fi

if [ -f /tmp/backend.pid ]; then
    pid=$(cat /tmp/backend.pid)
    if kill -0 $pid 2>/dev/null; then
        echo -e "停止旧的后端服务 (PID: $pid)"
        kill $pid
    fi
    rm /tmp/backend.pid
fi

# 启动前端服务
echo -e "${YELLOW}启动前端服务...${NC}"
cd /workspace/frontend
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}安装前端依赖...${NC}"
    npm install
fi

# 使用nohup启动前端服务，并将输出重定向到日志文件
echo -e "${YELLOW}启动前端开发服务器: http://localhost:3000${NC}"
# 后台运行前端服务
nohup npm run dev -- --host 0.0.0.0 --port 3000 > /tmp/frontend.log 2>&1 &
echo $! > /tmp/frontend.pid
echo -e "${GREEN}✅ 前端服务已启动${NC}"

# 启动后端服务
echo -e "${YELLOW}启动后端服务...${NC}"
cd /workspace/backend
echo -e "${YELLOW}启动后端API服务器: http://localhost:8000${NC}"
# 后台运行后端服务
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
echo $! > /tmp/backend.pid
echo -e "${GREEN}✅ 后端服务已启动${NC}"

# 检查是否需要启动监控服务
if [ -f /workspace/config.json ] && [ "$(jq -r '.monitoring.enabled // false' /workspace/config.json)" == "true" ]; then
    echo -e "${YELLOW}启动监控服务...${NC}"
    /workspace/monitoring/start-monitoring.sh
else
    echo -e "${YELLOW}监控服务未配置为自动启动。${NC}"
    echo -e "${YELLOW}可通过以下命令手动启动:${NC}"
    echo -e "${YELLOW}  /workspace/monitoring/start-monitoring.sh${NC}"
fi

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}       所有服务已启动                ${NC}"
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}前端:   ${NC}http://localhost:3000"
echo -e "${GREEN}后端:   ${NC}http://localhost:8000"
echo -e "${GREEN}监控UI: ${NC}http://localhost:9091 (如已启用)"
echo -e "${GREEN}=====================================${NC}"
echo -e "${YELLOW}日志文件位置:${NC}"
echo -e "${YELLOW}- 前端: /tmp/frontend.log${NC}"
echo -e "${YELLOW}- 后端: /tmp/backend.log${NC}"
echo -e "${GREEN}=====================================${NC}" 