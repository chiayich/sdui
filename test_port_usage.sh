#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}启动模拟SDUI服务测试...${NC}"

# 获取当前项目名称
PROJECT_NAME=$(basename "$(pwd)")
echo -e "${GREEN}当前项目名称: $PROJECT_NAME${NC}"

# 模拟前端服务 (使用Python简单HTTP服务器模拟)
echo -e "${YELLOW}启动模拟前端服务在端口5173...${NC}"
python3 -m http.server 5173 --bind 127.0.0.1 &
FRONTEND_PID=$!
echo -e "${GREEN}前端服务已启动，PID: $FRONTEND_PID${NC}"

# 模拟后端服务 (使用Python简单HTTP服务器模拟)
echo -e "${YELLOW}启动模拟后端服务在端口8000...${NC}"
python3 -m http.server 8000 --bind 127.0.0.1 &
BACKEND_PID=$!
echo -e "${GREEN}后端服务已启动，PID: $BACKEND_PID${NC}"

echo -e "${GREEN}服务模拟已完成，现在运行 ./.devcontainer/check_ports.sh 检查端口占用情况${NC}"
echo -e "${RED}完成测试后，请运行 'kill $FRONTEND_PID $BACKEND_PID' 停止模拟服务${NC}"

# 将PID保存到临时文件，方便后续关闭
echo "$FRONTEND_PID $BACKEND_PID" > .test_pids 