# Docker服务重启优化

**日期**: 2023-11-15
**类别**: 工具
**紧急程度**: 中

## 问题描述

在使用Docker Compose管理服务时，发现每次重启服务都必须重启所有服务，即使只有单个服务出现问题或需要更新。这种全量重启方式效率低下，特别是在前端正常但后端需要重启的情况下，会导致开发体验不佳和资源浪费。

## 问题分析

原始的`start-dev.sh`脚本设计只支持启动或重启所有服务，没有提供针对特定服务的重启选项。这导致即使只需要重启单个服务，也必须停止和重启整个应用栈，包括数据库、Redis、前端和后端服务等。

## 解决思路

1. 扩展现有的`start-dev.sh`脚本，添加对单个服务重启的支持
2. 实现基于参数的服务指定，允许用户选择重启特定服务
3. 优化端口检查逻辑，只检查与要重启的服务相关的端口
4. 提供清晰的帮助信息和使用文档

## 执行步骤

1. 修改`.devcontainer/start-dev.sh`脚本，添加单服务重启功能

```bash
# 重启指定服务
restart_service() {
    local service=$1
    
    echo -e "${YELLOW}正在重启服务: $service...${NC}"
    
    # 停止指定服务
    docker compose stop $service
    docker compose rm -f $service
    
    # 检查相关端口
    check_critical_ports $service
    
    # 启动服务
    if [ "$BACKGROUND" = "1" ]; then
        echo -e "${GREEN}以后台模式重启服务 $service...${NC}"
        docker compose up -d $service
    else
        echo -e "${GREEN}以前台模式重启服务 $service，按Ctrl+C停止...${NC}"
        docker compose up $service
    fi
}

# 检查关键端口（优化为只检查相关端口）
check_critical_ports() {
    local service=$1
    
    # 根据服务名检查相应的端口
    case "$service" in
        frontend|all)
            check_and_free_port 5173  # 前端
            check_and_free_port 5174  # 如果使用了备用前端端口
            ;;
        backend|all)
            check_and_free_port 8000  # 后端
            ;;
        db|all)
            check_and_free_port 5432  # PostgreSQL
            ;;
        redis|all)
            check_and_free_port 6379  # Redis
            ;;
        *)
            # 如果是其他服务名或未指定，默认检查所有端口
            check_and_free_port 8000  # 后端
            check_and_free_port 5173  # 前端
            check_and_free_port 5174  # 如果使用了备用前端端口
            check_and_free_port 5432  # PostgreSQL
            check_and_free_port 6379  # Redis
            ;;
    esac
}
```

2. 添加命令行参数处理逻辑

```bash
# 检查是否是重启命令
if [ "$1" = "restart" ]; then
    # 检查是否指定了特定服务
    if [ -n "$2" ]; then
        # 重启特定服务
        restart_service $2
    else
        # 重启所有服务
        echo -e "${YELLOW}正在重启所有服务...${NC}"
        
        # 停止所有服务
        docker compose down
        
        # 检查所有端口
        check_critical_ports all
        
        # 启动所有服务
        if [ "$BACKGROUND" = "1" ]; then
            echo -e "${GREEN}以后台模式重启所有服务...${NC}"
            docker compose up -d
        else
            echo -e "${GREEN}以前台模式重启所有服务，按Ctrl+C停止...${NC}"
            docker compose up
        fi
    fi
    exit 0
fi
```

3. 添加帮助信息显示功能

```bash
# 显示帮助信息
show_help() {
    echo -e "${GREEN}SDUI项目服务管理脚本${NC}"
    echo -e "用法:"
    echo -e "  $0                    - 启动所有服务（前台模式）"
    echo -e "  $0 restart            - 重启所有服务（前台模式）"
    echo -e "  $0 restart <服务名>   - 只重启指定服务（如frontend, backend, db, redis）"
    echo -e ""
    echo -e "环境变量:"
    echo -e "  BACKGROUND=1          - 使用后台模式启动服务"
}

# 显示帮助
if [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi
```

4. 更新文档，添加单个服务重启的说明

```markdown
### 重启服务

1. 重启所有服务（前台模式）:
   ```bash
   bash /workspace/.devcontainer/start-dev.sh restart
   ```

2. 重启所有服务（后台模式）:
   ```bash
   BACKGROUND=1 bash /workspace/.devcontainer/start-dev.sh restart
   ```

3. 只重启特定服务（前台模式）:
   ```bash
   # 只重启后端服务
   bash /workspace/.devcontainer/start-dev.sh restart backend
   
   # 只重启前端服务
   bash /workspace/.devcontainer/start-dev.sh restart frontend
   
   # 只重启数据库服务
   bash /workspace/.devcontainer/start-dev.sh restart db
   
   # 只重启Redis服务
   bash /workspace/.devcontainer/start-dev.sh restart redis
   ```
```

## 结果验证

通过以下方式验证了解决方案的有效性：

1. 使用命令`bash /workspace/.devcontainer/start-dev.sh restart backend`测试只重启后端服务
2. 确认前端、数据库和Redis服务保持运行状态
3. 验证后端服务成功重启并正常运行
4. 测试不同服务的重启命令，包括前端、数据库和Redis

## 相关资源

- [修改后的start-dev.sh脚本](/.devcontainer/start-dev.sh)
- [更新的Docker Compose指南](docs/docker-compose-guide.md)

## 注意事项

1. 服务名称必须与docker-compose.yml中定义的服务名称一致
2. 某些服务间存在依赖关系，单独重启一个服务可能需要确保其依赖服务正常运行
3. 对于数据库服务的重启，需注意可能导致的数据一致性问题 