#!/bin/bash
set -e

# 输出欢迎信息
echo "========================================"
echo "🚀 SDUI开发环境初始化脚本"
echo "========================================"

# 设置Docker权限
echo "🔧 配置Docker权限..."
if [ -S /var/run/docker.sock ]; then
    # 获取docker.sock的所有者GID
    DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
    
    # 检查docker组是否存在
    if ! getent group $DOCKER_GID > /dev/null; then
        echo "👉 创建docker组 (GID: $DOCKER_GID)..."
        sudo groupadd -g $DOCKER_GID docker_host || true
    fi
    
    # 将当前用户添加到docker组
    GROUP_NAME=$(getent group $DOCKER_GID | cut -d: -f1)
    echo "👉 将当前用户添加到${GROUP_NAME}组..."
    sudo usermod -aG $DOCKER_GID $(whoami)
    
    # 测试Docker权限
    echo "👉 测试Docker权限..."
    docker info > /dev/null 2>&1 && echo "✅ Docker权限配置成功！" || echo "❌ Docker权限配置失败，请尝试重启容器或手动配置权限"
else
    echo "❌ Docker socket不存在，请确保Docker已安装并已将socket挂载到容器中"
fi

# 配置Docker客户端设置
echo "🔧 配置Docker客户端..."

# 创建.docker目录
mkdir -p ~/.docker

# 配置Docker客户端config.json
echo "👉 配置Docker客户端config.json..."
cat > ~/.docker/config.json << 'EOL'
{
    "auths": {},
    "currentContext": "default"
}
EOL

# 配置Docker环境变量
echo "👉 配置Docker环境变量..."
DOCKER_ENV_LINE='export DOCKER_HOST=unix:///var/run/docker.sock'

# 检查并添加DOCKER_HOST环境变量到.bashrc
if ! grep -q "$DOCKER_ENV_LINE" ~/.bashrc; then
    echo "$DOCKER_ENV_LINE" >> ~/.bashrc
    echo "✅ 已添加DOCKER_HOST环境变量到.bashrc"
else
    echo "✅ DOCKER_HOST环境变量已存在"
fi

# 立即生效环境变量
export DOCKER_HOST=unix:///var/run/docker.sock

# 验证Docker配置
echo "👉 验证Docker配置..."
docker info > /dev/null 2>&1 && echo "✅ Docker配置验证成功！" || echo "❌ Docker配置验证失败，请检查DOCKER_HOST环境变量和config.json设置"

# 初始化项目依赖
echo "📦 安装项目依赖..."

# 后端依赖安装
if [ -f /workspace/backend/requirements.txt ]; then
    echo "👉 安装后端Python依赖..."
    cd /workspace/backend
    pip install -r requirements.txt
fi

# 前端依赖安装
if [ -f /workspace/frontend/package.json ]; then
    echo "👉 安装前端Node.js依赖..."
    cd /workspace/frontend
    npm install
fi

# 创建监控所需目录
echo "🔍 创建监控系统目录..."
mkdir -p /workspace/monitoring/{prometheus,skywalking,loki,kafka,elk}/{config,dashboards} 2>/dev/null || true

echo "========================================"
echo "✅ 初始化完成！开发环境已准备就绪"
echo "========================================" 