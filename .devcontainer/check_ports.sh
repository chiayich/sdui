#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查当前目录，确保脚本在项目根目录执行
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")


# 检测是否由devcontainer自动调用
if [ -n "$VSCODE_REMOTE_CONTAINERS_SESSION" ] || [ -n "$DEVCONTAINER_CLI" ]; then
    AUTO_RUN=true
else
    AUTO_RUN=false
fi

if [ "$AUTO_RUN" = true ]; then
    echo -e "${BLUE}===================================================${NC}"
    echo -e "${BLUE}   DevContainer 自动端口检查                      ${NC}"
    echo -e "${BLUE}===================================================${NC}"
else
    echo -e "${GREEN}===================================================${NC}"
    echo -e "${GREEN}   SDUI 开发容器端口检查和配置生成工具            ${NC}"
    echo -e "${GREEN}===================================================${NC}"
fi

# 定义要检查的端口和服务名称（使用普通数组以提高兼容性）
SERVICES=("FRONTEND_PORT" "BACKEND_PORT" "POSTGRES_PORT" "REDIS_PORT" "PROMETHEUS_PORT" "GRAFANA_PORT" "SKYWALKING_PORT" "LOKI_PORT")
DEFAULT_PORTS=(5173 8000 5432 6379 9090 9091 9093 9094)

# 定义端口占用检查函数
is_port_in_use() {
    if command -v lsof &> /dev/null; then
        lsof -i :"$1" &> /dev/null
        return $?
    elif command -v netstat &> /dev/null; then
        netstat -tuln | grep :"$1" &> /dev/null
        return $?
    else
        # 如果既没有lsof也没有netstat，使用可能存在的简单替代方法
        # 注意: 这可能不是100%可靠的
        (echo > /dev/tcp/localhost/"$1") &> /dev/null
        return $?
    fi
}

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
        "BACKEND")
            # 检查是否为后端服务 (Python, uvicorn等)
            if lsof -i :"$port" | grep -E "python|uvicorn" &> /dev/null; then
                # 再检查是否是我们项目的后端
                local pids=$(lsof -i :"$port" | grep -E "python|uvicorn" | awk '{print $2}')
                for pid in $pids; do
                    if ps -fp $pid | grep -E "backend|uvicorn|python.*${project_name}" &> /dev/null; then
                        echo "our_backend"
                        return 0
                    fi
                done
            fi
            ;;
        "POSTGRES")
            # 检查是否为本地PostgreSQL实例
            if lsof -i :"$port" | grep -q "postgres"; then
                # 检查是否是我们项目的数据库
                if docker ps | grep -E "${project_name}.*postgres|postgres.*${project_name}|${current_dir}.*postgres" &> /dev/null; then
                    echo "our_postgres"
                    return 0
                fi
                echo "local_postgres"
                return 0
            fi
            ;;
        "REDIS")
            # 检查是否为本地Redis实例
            if lsof -i :"$port" | grep -q "redis"; then
                # 检查是否是我们项目的Redis
                if docker ps | grep -E "${project_name}.*redis|redis.*${project_name}|${current_dir}.*redis" &> /dev/null; then
                    echo "our_redis"
                    return 0
                fi
                echo "local_redis"
                return 0
            fi
            ;;
    esac
    
    # 不是我们自己的服务
    echo "other"
    return 1
}

# 查找下一个可用端口（无输出版本，仅返回结果）
find_next_available_port_silent() {
    local port=$1
    while is_port_in_use "$port"; do
        ((port++))
    done
    echo "$port"
}

# 读取现有环境变量值
read_existing_env_values() {
    if [ -f .devcontainer/.env ]; then
        # 从现有的.env文件读取值
        for i in "${!SERVICES[@]}"; do
            service=${SERVICES[$i]}
            
            # 如果存在该环境变量设置，则读取其值
            if grep -q "^$service=" .devcontainer/.env; then
                local value=$(grep "^$service=" .devcontainer/.env | cut -d= -f2)
                CURRENT_PORTS[$i]=$value
            else
                CURRENT_PORTS[$i]=${DEFAULT_PORTS[$i]}
            fi
        done
    else
        # 如果不存在.env文件，则使用默认值
        for i in "${!DEFAULT_PORTS[@]}"; do
            CURRENT_PORTS[$i]=${DEFAULT_PORTS[$i]}
        done
    fi
}

# 创建.devcontainer目录（如果不存在）
mkdir -p .devcontainer

# 初始化当前端口数组
CURRENT_PORTS=()
read_existing_env_values

# 创建env文件内容
echo -e "# SDUI开发环境自定义端口配置" > .devcontainer/.env.temp
echo -e "# 通过端口检查脚本自动生成于 $(date)" >> .devcontainer/.env.temp
echo -e "" >> .devcontainer/.env.temp

# 检查是否存在现有的FOREGROUND设置，如果存在则保留
if [ -f .devcontainer/.env ] && grep -q "FOREGROUND=" .devcontainer/.env; then
    FOREGROUND_VALUE=$(grep "FOREGROUND=" .devcontainer/.env | sed 's/FOREGROUND=//')
    echo -e "# 指定服务启动模式: 0=后台模式, 1=交互式菜单模式" >> .devcontainer/.env.temp
    echo -e "FOREGROUND=$FOREGROUND_VALUE" >> .devcontainer/.env.temp
    echo -e "" >> .devcontainer/.env.temp
else
    # 如果不存在，添加默认设置
    echo -e "# 指定服务启动模式: 0=后台模式, 1=交互式菜单模式" >> .devcontainer/.env.temp
    echo -e "FOREGROUND=0" >> .devcontainer/.env.temp
    echo -e "" >> .devcontainer/.env.temp
fi

# 检查每个端口并生成配置
echo -e "${YELLOW}正在检查端口占用情况...${NC}"
echo -e ""
echo -e "| 服务 | 当前端口 | 状态 | 操作 |"
echo -e "|------|----------|------|------|"

any_port_change=false
services_to_restart=()

for i in "${!SERVICES[@]}"; do
    service=${SERVICES[$i]}
    default_port=${DEFAULT_PORTS[$i]}
    current_port=${CURRENT_PORTS[$i]:-$default_port}
    service_name=$(echo "$service" | sed 's/_PORT//')
    
    # 检查当前端口是否被占用
    if is_port_in_use "$current_port"; then
        # 检查占用此端口的是否是我们自己的服务
        occupier=$(is_port_used_by_our_service "$current_port" "$service_name")
        
        if [[ "$occupier" == our_* ]]; then
            # 端口被我们自己的服务占用，标记需要重启服务
            echo -e "| $service_name | $current_port | ${YELLOW}已被我们的服务占用${NC} | ${GREEN}重启服务${NC} |"
            
            # 保持当前端口设置
            echo -e "# $service_name 当前端口($current_port)被我们自己的服务占用，将重启服务" >> .devcontainer/.env.temp
            echo -e "$service=$current_port" >> .devcontainer/.env.temp
            echo -e "" >> .devcontainer/.env.temp
            
            # 将服务添加到需要重启的列表
            services_to_restart+=("$service_name")
        elif [[ "$occupier" == local_* ]]; then
            # 端口被本地系统服务占用，需要分配新端口
            new_port=$(find_next_available_port_silent "$current_port")
            
            echo -e "| $service_name | $current_port | ${YELLOW}已被本地服务占用${NC} | ${YELLOW}改用端口 $new_port${NC} |"
            
            # 写入新的端口设置 - 确保注释与实际值一致
            echo -e "# $service_name 使用端口 $new_port (原端口 $current_port 已被本地服务占用)" >> .devcontainer/.env.temp
            echo -e "$service=$new_port" >> .devcontainer/.env.temp
            echo -e "" >> .devcontainer/.env.temp
            
            # 标记端口有变更
            if [ "$current_port" != "$new_port" ]; then
                any_port_change=true
            fi
        else
            # 端口被其他不相关的服务占用，需要分配新端口
            new_port=$(find_next_available_port_silent "$current_port")
            
            echo -e "| $service_name | $current_port | ${RED}已被其他服务占用${NC} | ${YELLOW}改用端口 $new_port${NC} |"
            
            # 写入新的端口设置 - 确保注释与实际值一致
            echo -e "# $service_name 使用端口 $new_port (原端口 $current_port 已被占用)" >> .devcontainer/.env.temp
            echo -e "$service=$new_port" >> .devcontainer/.env.temp
            echo -e "" >> .devcontainer/.env.temp
            
            # 标记端口有变更
            if [ "$current_port" != "$new_port" ]; then
                any_port_change=true
            fi
        fi
    else
        # 端口未被占用，继续使用
        echo -e "| $service_name | $current_port | ${GREEN}可用${NC} | ${GREEN}保持不变${NC} |"
        
        # 维持现有设置或使用默认值 - 确保注释与实际值一致
        if [ "$current_port" != "$default_port" ]; then
            # 如果当前端口不是默认端口，保持当前设置
            echo -e "# $service_name 使用自定义端口 $current_port" >> .devcontainer/.env.temp
            echo -e "$service=$current_port" >> .devcontainer/.env.temp
        else
            # 使用默认端口
            echo -e "# $service_name 使用默认端口($default_port)" >> .devcontainer/.env.temp
            # 明确设置默认端口，避免混淆
            echo -e "$service=$default_port" >> .devcontainer/.env.temp
        fi
        echo -e "" >> .devcontainer/.env.temp
    fi
done

# 如果有服务需要重启，保存到配置文件中以便start-dev.sh读取
if [ ${#services_to_restart[@]} -gt 0 ]; then
    echo -e "# 标记需要重启的服务" >> .devcontainer/.env.temp
    echo -e "SERVICES_TO_RESTART=\"${services_to_restart[*]}\"" >> .devcontainer/.env.temp
    echo -e "" >> .devcontainer/.env.temp
fi

# 完成配置文件
echo -e "# 端口配置生成结束" >> .devcontainer/.env.temp
echo -e "# 配置生成时间: $(date)" >> .devcontainer/.env.temp

# 移动临时文件到最终位置
mv .devcontainer/.env.temp .devcontainer/.env

# 根据自动运行状态和端口变更情况输出不同的提示
if [ "$AUTO_RUN" = true ]; then
    echo -e ""
    if [ "$any_port_change" = true ]; then
        echo -e "${BLUE}===================================================${NC}"
        echo -e "${BLUE}   端口配置已更新: .devcontainer/.env             ${NC}"
        echo -e "${BLUE}===================================================${NC}"
    else
        echo -e "${GREEN}===================================================${NC}"
        if [ ${#services_to_restart[@]} -gt 0 ]; then
            echo -e "${GREEN}   无需更改端口配置，需要重启以下服务:          ${NC}"
            for service in "${services_to_restart[@]}"; do
                echo -e "${YELLOW}   - $service${NC}"
            done
        else
            echo -e "${GREEN}   无需更改端口配置或重启服务                  ${NC}"
        fi
        echo -e "${GREEN}===================================================${NC}"
    fi
else
    echo -e ""
    if [ "$any_port_change" = true ]; then
        echo -e "${GREEN}===================================================${NC}"
        echo -e "${GREEN}   端口配置已更新: .devcontainer/.env             ${NC}"
        echo -e "${GREEN}===================================================${NC}"
        echo -e "${YELLOW}你需要重启开发容器应用新的端口配置${NC}"
    else
        echo -e "${GREEN}===================================================${NC}"
        if [ ${#services_to_restart[@]} -gt 0 ]; then
            echo -e "${GREEN}   无需更改端口配置，但需要重启以下服务:        ${NC}"
            for service in "${services_to_restart[@]}"; do
                echo -e "${YELLOW}   - $service${NC}"
            done
            echo -e "${YELLOW}容器启动后，start-dev.sh 将自动重启这些服务${NC}"
        else
            echo -e "${GREEN}   无需更改端口配置                           ${NC}"
        fi
        echo -e "${GREEN}===================================================${NC}"
        echo -e "${YELLOW}可以通过重启服务使用现有配置${NC}"
    fi
    echo -e "${YELLOW}VS Code: Ctrl+Shift+P > Remote-Containers: Rebuild Container${NC}"
    echo -e "${GREEN}===================================================${NC}"
fi 