#!/bin/bash

# 停止所有正在运行的Vite进程
pkill -f vite || true

# 等待进程完全停止
sleep 1

# 启动开发服务器，确保监听所有网络接口
cd "$(dirname "$0")"
export NODE_ENV=development
npm run dev -- --host 0.0.0.0

echo "开发服务器已启动，请访问 http://localhost:5173" 