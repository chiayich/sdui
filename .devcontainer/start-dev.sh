#!/bin/bash
# 这是一个开发环境启动脚本，因为使用devcontainer开发，所以进入容器后避免手动操作，使用环境.env文件配置， 依次启动前后端，及其他需要的服务。

# 设置错误时退出
set -e

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 获取脚本目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 加载环境变量
load_env_file() {
    ENV_FILE="${SCRIPT_DIR}/.env"
    if [ -f "$ENV_FILE" ]; then
        print_info "加载环境变量文件: $ENV_FILE"
        set -a  # 自动导出所有变量
        source "$ENV_FILE"
        set +a
        print_success "环境变量加载完成"
        
        # 显示加载的环境变量
        print_info "使用以下环境变量:"
        echo "FRONTEND_PORT=${FRONTEND_PORT:-5173}"
        echo "BACKEND_PORT=${BACKEND_PORT:-8000}"
        echo "POSTGRES_PORT=${POSTGRES_PORT:-5432}"
        echo "REDIS_PORT=${REDIS_PORT:-6379}"
        
        # 显示监控相关环境变量(如果存在)
        if [ -n "$PROMETHEUS_PORT" ]; then
            echo "PROMETHEUS_PORT=${PROMETHEUS_PORT}"
        fi
        if [ -n "$GRAFANA_PORT" ]; then
            echo "GRAFANA_PORT=${GRAFANA_PORT}"
        fi
        if [ -n "$SKYWALKING_PORT" ]; then
            echo "SKYWALKING_PORT=${SKYWALKING_PORT}"
        fi
        if [ -n "$LOKI_PORT" ]; then
            echo "LOKI_PORT=${LOKI_PORT}"
        fi
    else
        print_warning "环境变量文件不存在: $ENV_FILE，将使用默认值"
        # 设置默认值
        FRONTEND_PORT=5173
        BACKEND_PORT=8000
        POSTGRES_PORT=5432
        REDIS_PORT=6379
        FOREGROUND=1  # 默认使用交互式菜单
    fi
}

# 检查端口是否可用
check_ports() {
    PORT_CHECK_SCRIPT="${SCRIPT_DIR}/check_ports.sh"
    if [ -f "$PORT_CHECK_SCRIPT" ]; then
        print_info "检查端口配置..."
        bash "$PORT_CHECK_SCRIPT"
        
        # 重新加载环境变量，因为端口可能被更新
        load_env_file
        
        print_success "端口配置检查完成"
    else
        print_warning "端口检查脚本不存在: $PORT_CHECK_SCRIPT，将使用配置的端口值"
    fi
}

# 启动后端服务
start_backend() {
    print_info "启动后端服务 (端口: $BACKEND_PORT)..."
    cd "${WORKSPACE_DIR}/backend"
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # 检查是否安装了uvicorn
    if ! command -v uvicorn &> /dev/null; then
        print_warning "未安装uvicorn，尝试安装..."
        pip install uvicorn
    fi
    
    # 启动后端服务
    uvicorn app.main:app --reload --host 0.0.0.0 --port $BACKEND_PORT --log-level debug &
    BACKEND_PID=$!
    print_success "后端服务启动成功 (PID: $BACKEND_PID)"
    cd "${WORKSPACE_DIR}"
}

# 启动前端服务
start_frontend() {
    print_info "启动前端服务 (端口: $FRONTEND_PORT)..."
    cd "${WORKSPACE_DIR}/frontend"
    
    # 检查是否安装了依赖
    if [ ! -d "node_modules" ]; then
        print_warning "未安装前端依赖，尝试安装..."
        npm install
    fi
    
    # 启动前端服务
    npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT &
    FRONTEND_PID=$!
    print_success "前端服务启动成功 (PID: $FRONTEND_PID)"
    cd "${WORKSPACE_DIR}"
}

# 启动监控服务
start_monitoring() {
    MONITORING_SCRIPT="${WORKSPACE_DIR}/monitoring/start-monitoring.sh"
    if [ -f "$MONITORING_SCRIPT" ]; then
        print_info "启动监控服务..."
        # 确保脚本可执行
        chmod +x "$MONITORING_SCRIPT"
        # 执行监控启动脚本
        bash "$MONITORING_SCRIPT"
        print_success "监控服务启动完成"
    else
        print_warning "监控启动脚本不存在: $MONITORING_SCRIPT"
    fi
}

# 启动数据库服务
start_database() {
    print_info "启动数据库服务 (端口: $POSTGRES_PORT)..."
    # 检查Docker是否运行
    if ! docker info &>/dev/null; then
        print_error "Docker未运行，无法启动数据库服务"
        return 1
    fi
    
    # 检查数据库容器是否已存在
    if docker ps -a | grep -q "sdui-db"; then
        # 如果存在但未运行，则启动它
        if ! docker ps | grep -q "sdui-db"; then
            print_info "启动已存在的数据库容器..."
            docker start sdui-db
        fi
        
        # 检查端口是否一致，如不一致则重新创建
        DB_CURRENT_PORT=$(docker port sdui-db 5432/tcp | cut -d ':' -f 2)
        if [ "$DB_CURRENT_PORT" != "$POSTGRES_PORT" ]; then
            print_warning "数据库容器端口 ($DB_CURRENT_PORT) 与配置端口 ($POSTGRES_PORT) 不一致，重新创建容器..."
            docker stop sdui-db
            docker rm sdui-db
            docker run -d --name sdui-db \
                -e POSTGRES_USER=postgres \
                -e POSTGRES_PASSWORD=postgres \
                -e POSTGRES_DB=sdui \
                -p ${POSTGRES_PORT}:5432 \
                -v postgres-data:/var/lib/postgresql/data \
                postgres:14-alpine
        else
            print_info "数据库容器已运行在端口 $POSTGRES_PORT"
        fi
    else
        # 如果不存在，则创建新容器
        print_info "创建新的数据库容器..."
        docker run -d --name sdui-db \
            -e POSTGRES_USER=postgres \
            -e POSTGRES_PASSWORD=postgres \
            -e POSTGRES_DB=sdui \
            -p ${POSTGRES_PORT}:5432 \
            -v postgres-data:/var/lib/postgresql/data \
            postgres:14-alpine
    fi
    
    print_success "数据库服务启动完成"
}

# 启动Redis服务
start_redis() {
    print_info "启动Redis服务 (端口: $REDIS_PORT)..."
    # 检查Docker是否运行
    if ! docker info &>/dev/null; then
        print_error "Docker未运行，无法启动Redis服务"
        return 1
    fi
    
    # 检查Redis容器是否已存在
    if docker ps -a | grep -q "sdui-redis"; then
        # 如果存在但未运行，则启动它
        if ! docker ps | grep -q "sdui-redis"; then
            print_info "启动已存在的Redis容器..."
            docker start sdui-redis
        fi
        
        # 检查端口是否一致，如不一致则重新创建
        REDIS_CURRENT_PORT=$(docker port sdui-redis 6379/tcp | cut -d ':' -f 2)
        if [ "$REDIS_CURRENT_PORT" != "$REDIS_PORT" ]; then
            print_warning "Redis容器端口 ($REDIS_CURRENT_PORT) 与配置端口 ($REDIS_PORT) 不一致，重新创建容器..."
            docker stop sdui-redis
            docker rm sdui-redis
            docker run -d --name sdui-redis \
                -p ${REDIS_PORT}:6379 \
                -v redis-data:/data \
                redis:alpine
        else
            print_info "Redis容器已运行在端口 $REDIS_PORT"
        fi
    else
        # 如果不存在，则创建新容器
        print_info "创建新的Redis容器..."
        docker run -d --name sdui-redis \
            -p ${REDIS_PORT}:6379 \
            -v redis-data:/data \
            redis:alpine
    fi
    
    print_success "Redis服务启动完成"
}

# 交互式菜单
show_menu() {
    clear
    echo "========================================="
    echo "       SDUI 开发环境启动菜单"
    echo "========================================="
    echo "1. 启动所有服务"
    echo "2. 仅启动前后端服务"
    echo "3. 仅启动后端服务"
    echo "4. 仅启动前端服务"
    echo "5. 启动数据库和Redis"
    echo "6. 启动监控服务"
    echo "7. 查看服务状态"
    echo "8. 查看环境配置"
    echo "0. 退出"
    echo "========================================="
    echo -n "请选择 [0-8]: "
    read -r choice

    case $choice in
        1)
            start_database
            start_redis
            start_backend
            start_frontend
            start_monitoring
            sleep 2
            show_menu
            ;;
        2)
            start_database
            start_redis
            start_backend
            start_frontend
            sleep 2
            show_menu
            ;;
        3)
            start_database
            start_redis
            start_backend
            sleep 2
            show_menu
            ;;
        4)
            start_frontend
            sleep 2
            show_menu
            ;;
        5)
            start_database
            start_redis
            sleep 2
            show_menu
            ;;
        6)
            start_monitoring
            sleep 2
            show_menu
            ;;
        7)
            echo ""
            echo "==== 进程状态 ===="
            ps aux | grep -E 'uvicorn|npm run dev' | grep -v grep || echo "没有运行中的前后端服务"
            echo ""
            echo "==== Docker容器状态 ===="
            docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E 'sdui-db|sdui-redis|prometheus|grafana|loki|skywalking' || echo "没有运行中的Docker容器"
            echo ""
            echo "按任意键继续..."
            read -n 1
            show_menu
            ;;
        8)
            echo ""
            echo "环境配置:"
            echo "前端端口: $FRONTEND_PORT"
            echo "后端端口: $BACKEND_PORT"
            echo "数据库端口: $POSTGRES_PORT"
            echo "Redis端口: $REDIS_PORT"
            if [ -n "$PROMETHEUS_PORT" ]; then echo "Prometheus端口: $PROMETHEUS_PORT"; fi
            if [ -n "$GRAFANA_PORT" ]; then echo "Grafana端口: $GRAFANA_PORT"; fi
            if [ -n "$SKYWALKING_PORT" ]; then echo "SkyWalking端口: $SKYWALKING_PORT"; fi
            if [ -n "$LOKI_PORT" ]; then echo "Loki端口: $LOKI_PORT"; fi
            echo ""
            echo "按任意键继续..."
            read -n 1
            show_menu
            ;;
        0)
            print_info "退出菜单"
            exit 0
            ;;
        *)
            print_error "无效选项，请重新选择"
            sleep 1
            show_menu
            ;;
    esac
}

# 停止服务函数
stop_services() {
    print_info "正在停止前后端服务..."
    pkill -f "uvicorn app.main:app" || true
    pkill -f "npm run dev" || true
    print_success "前后端服务已停止"
}

# 启动所有服务
start_all_services() {
    # 启动服务
    if [ "${FOREGROUND:-1}" -eq "0" ]; then
        # 后台模式启动所有服务
        print_info "以后台模式启动所有服务..."
        start_database
        start_redis
        start_backend
        start_frontend
        start_monitoring
        print_success "所有服务已在后台启动"
    else
        # 交互式菜单模式
        show_menu
    fi
}

# 清理函数 - 在脚本异常退出时调用
cleanup() {
    print_warning "脚本执行被中断，正在清理..."
    # 添加任何需要的清理操作
}

# 捕获退出信号
trap cleanup SIGINT SIGTERM

# 主函数
main() {
    print_info "SDUI开发环境启动脚本"
    
    # 停止可能已运行的服务
    stop_services
    
    # 加载环境变量
    load_env_file
    
    # 启动服务
    start_all_services
}

# 执行主函数
main 