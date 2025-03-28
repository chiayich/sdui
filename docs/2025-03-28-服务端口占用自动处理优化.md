# SDUI服务端口占用自动处理优化

**日期**: 2025-03-28
**类别**: 工具
**紧急程度**: 中

## 问题描述

在SDUI开发环境中，当同一项目的服务占用端口时，原有的端口检查机制无法区分是否是项目自身的服务占用，导致服务频繁被重新分配端口号，影响开发效率。特别是当端口未被占用但服务已在运行（可能在其他端口上运行），需要重启服务以使其使用正确配置的端口。

## 问题分析

当前的开发环境存在两个主要挑战：

1. **服务识别问题**：当前端口检查脚本(`check_ports.sh`)无法准确区分端口占用者是否为SDUI自身的服务，导致不必要的端口变更。

2. **端口配置同步问题**：已运行的服务可能使用的是旧的端口配置，与最新的环境配置文件不一致，需要确保服务重启后使用正确的端口配置。

这些问题导致开发环境不稳定，增加了开发者管理环境的负担，破坏了一致性体验。

## 解决思路

1. **增强服务识别**：改进`check_ports.sh`脚本，添加更精确的服务识别机制，能够检测端口占用者是否为SDUI项目的服务，包括Docker容器和本地进程。

2. **端口配置同步**：修改`start-dev.sh`脚本，添加功能检测服务是否使用了环境变量文件中指定的正确端口，如果不是则重启服务使其使用正确配置。

3. **职责分离**：端口占用检测由`check_ports.sh`负责，将检测结果写入环境变量；服务管理和重启由`start-dev.sh`负责，读取环境变量执行相应操作。

## 执行步骤

### 1. 改进`check_ports.sh`脚本

增强检测服务是否为SDUI项目的功能：

```bash
# 检查端口是否被我们自己的服务占用
is_port_used_by_our_service() {
    local port=$1
    local service_name=$2
    
    # 项目名称
    local project_name="sdui"
    
    # 获取当前目录名（项目名）
    local current_dir=$(basename "$(pwd)")
    
    # 检查是否有Docker容器使用此端口
    if docker ps | grep -E "${project_name}|${current_dir}|devcontainer" | grep -q ":$port->"; then
        echo "our_service"
        return 0
    fi
    
    # 检查进程名是否包含我们项目名称
    if command -v lsof &> /dev/null; then
        if lsof -i :"$port" | grep -iE "${project_name}|${current_dir}" &> /dev/null; then
            echo "our_process"
            return 0
        fi
    fi
    
    # 检查特定服务的本地实例
    case "$service_name" in
        "FRONTEND")
            # 检查是否为前端服务 (Node.js, npm, vite等)
            if lsof -i :"$port" | grep -E "node|npm|vite" &> /dev/null; then
                # 再检查是否是我们项目的前端
                local pids=$(lsof -i :"$port" | grep -E "node|npm|vite" | awk '{print $2}')
                for pid in $pids; do
                    if ps -fp $pid | grep -E "frontend|vite|node.*${project_name}" &> /dev/null; then
                        echo "our_frontend"
                        return 0
                    fi
                done
            fi
            ;;
        # ... 其他服务的检测 ...
    esac
    
    # 不是我们自己的服务
    echo "other"
    return 1
}
```

增加对服务占用的处理和标记：

```bash
if [[ "$occupier" == our_* ]]; then
    # 端口被我们自己的服务占用，标记需要重启服务
    echo -e "| $service_name | $current_port | ${YELLOW}已被我们的服务占用${NC} | ${GREEN}重启服务${NC} |"
    
    # 保持当前端口设置
    echo -e "# $service_name 当前端口($current_port)被我们自己的服务占用，将重启服务" >> .devcontainer/.env.temp
    echo -e "$service=$current_port" >> .devcontainer/.env.temp
    
    # 将服务添加到需要重启的列表
    services_to_restart+=("$service_name")
}
```

将需要重启的服务写入环境变量：

```bash
# 如果有服务需要重启，保存到配置文件中以便start-dev.sh读取
if [ ${#services_to_restart[@]} -gt 0 ]; then
    echo -e "# 标记需要重启的服务" >> .devcontainer/.env.temp
    echo -e "SERVICES_TO_RESTART=\"${services_to_restart[*]}\"" >> .devcontainer/.env.temp
fi
```

### 2. 增强`start-dev.sh`脚本

添加检测服务当前使用端口的功能：

```bash
# 函数：检查服务是否使用预期的端口
service_using_expected_port() {
    local service=$1
    local expected_port=$2
    local container_name
    
    # 获取服务的容器名称
    container_name=$(docker compose ps -q $service 2>/dev/null)
    
    if [ -z "$container_name" ]; then
        # 服务不在运行
        return 1
    fi
    
    # 检查容器是否映射了预期的端口
    docker port "$container_name" | grep -q ":$expected_port->"
    return $?
}
```

添加检查并重启使用错误端口的服务的功能：

```bash
# 检查服务是否使用指定的端口，如果不是则重启服务
check_and_restart_if_port_mismatch() {
    local services_to_check=("FRONTEND:frontend:${FRONTEND_PORT:-5173}" 
                           "BACKEND:backend:${BACKEND_PORT:-8000}" 
                           # ... 其他服务 ...)
    
    local services_needing_restart=()
    
    for service_info in "${services_to_check[@]}"; do
        IFS=':' read -r service_name docker_service expected_port <<< "$service_info"
        
        if service_is_running "$docker_service"; then
            if ! service_using_expected_port "$docker_service" "$expected_port"; then
                echo -e "${YELLOW}$service_name 服务正在运行，但未使用预期的端口 $expected_port${NC}"
                services_needing_restart+=("$service_name")
            fi
        fi
    done
    
    if [ ${#services_needing_restart[@]} -gt 0 ]; then
        # ... 处理需要重启的服务 ...
    fi
}
```

1. **改进开发环境启动脚本**

在`.devcontainer/start-dev.sh`中添加以下关键功能：

```bash
# 加载环境变量后再次检查，确保使用最新配置
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
        # 其他环境变量...
    fi
}

# 检查端口配置并更新后重新加载环境变量
check_ports() {
    PORT_CHECK_SCRIPT="${SCRIPT_DIR}/check_ports.sh"
    if [ -f "$PORT_CHECK_SCRIPT" ]; then
        print_info "检查端口配置..."
        bash "$PORT_CHECK_SCRIPT"
        
        # 重新加载环境变量，因为端口可能被更新
        load_env_file
        
        print_success "端口配置检查完成"
    fi
}

# 启动服务前停止可能已经运行的服务
stop_services() {
    print_info "正在停止前后端服务..."
    pkill -f "uvicorn app.main:app" || true
    pkill -f "npm run dev" || true
    print_success "前后端服务已停止"
}
```

2. **数据库和Redis端口同步**

在启动数据库和Redis时，检查容器当前使用端口与配置端口是否一致，如不一致则重新创建容器：

```bash
# 启动数据库服务
start_database() {
    # 检查端口是否一致，如不一致则重新创建
    DB_CURRENT_PORT=$(docker port sdui-db 5432/tcp | cut -d ':' -f 2)
    if [ "$DB_CURRENT_PORT" != "$POSTGRES_PORT" ]; then
        print_warning "数据库容器端口 ($DB_CURRENT_PORT) 与配置端口 ($POSTGRES_PORT) 不一致，重新创建容器..."
        docker stop sdui-db
        docker rm sdui-db
        docker run -d --name sdui-db \
            -p ${POSTGRES_PORT}:5432 \
            -v postgres-data:/var/lib/postgresql/data \
            postgres:14-alpine
    fi
}
```

3. **监控服务端口同步**

通过动态创建docker-compose覆盖文件，确保使用环境变量中的自定义端口：

```bash
# 如果环境变量中有自定义端口，创建临时覆盖文件
if [ -n "$PROMETHEUS_PORT" ] || [ -n "$GRAFANA_PORT" ] || [ -n "$SKYWALKING_PORT" ] || [ -n "$LOKI_PORT" ]; then
    echo -e "${YELLOW}使用自定义端口配置...${NC}"
    cat > docker-compose.env-override.yml << EOF
version: '3.8'
services:
EOF
    
    # 添加各服务自定义端口配置
    if [ -n "$PROMETHEUS_PORT" ]; then
        cat >> docker-compose.env-override.yml << EOF
  prometheus:
    ports:
      - "${PROMETHEUS_PORT}:9090"
EOF
    fi
    
    # 启动监控服务，使用临时覆盖文件
    docker compose -f docker-compose.yml -f docker-compose.env-override.yml up -d $SERVICES
    
    # 清理临时文件
    rm -f docker-compose.env-override.yml
fi
```

## 结果验证

1. 启动脚本现在能够正确处理端口冲突，确保开发环境中的所有服务使用统一的最新端口配置。

2. 测试启动脚本处理以下场景：
   - 首次启动所有服务：正确使用配置的端口
   - 端口冲突后重启：自动调整并使用新端口
   - 配置变更后重启：所有服务同步使用新端口配置

3. 通过`docker ps`和`netstat`验证所有服务端口配置正确：

```
$ docker ps --format "table {{.Names}}\t{{.Ports}}"
NAMES               PORTS
sdui-redis          0.0.0.0:6380->6379/tcp
sdui-db             0.0.0.0:5433->5432/tcp
prometheus          0.0.0.0:9090->9090/tcp
grafana             0.0.0.0:9091->3000/tcp
loki                0.0.0.0:9094->3100/tcp
```

## 相关资源

- [check_ports.sh](.devcontainer/check_ports.sh) - 端口检查脚本
- [start-dev.sh](.devcontainer/start-dev.sh) - 开发环境启动脚本
- [start-monitoring.sh](monitoring/start-monitoring.sh) - 监控服务启动脚本

## 注意事项

1. 脚本依赖于Docker和lsof命令，确保开发环境中安装了相关工具
2. 服务检测基于进程名和容器名规则，如项目结构发生重大变化，需要相应更新检测逻辑
3. 针对特定服务的检测规则可能需要根据具体项目结构进行调整 