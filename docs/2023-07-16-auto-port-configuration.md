# 自动端口配置工具实现

**日期**: 2023-07-16
**类别**: 开发工具
**紧急程度**: 中

## 问题描述

在使用开发容器（devcontainer）进行开发时，频繁出现端口冲突问题，特别是在团队成员的不同开发环境中。虽然已经实现了通过环境变量配置端口的机制，但需要手动检查哪些端口已被占用，过程繁琐且容易出错。

## 问题分析

手动检查端口占用情况需要开发者运行多个命令（如`lsof`或`netstat`），然后手动编辑配置文件，流程复杂且容易遗漏。理想情况下，应该有一个自动化工具可以：

1. 检测本地环境中已被占用的端口
2. 为被占用的端口自动选择替代端口
3. 生成正确格式的配置文件

## 解决思路

通过创建一个bash脚本，自动检查关键服务端口的占用情况，并生成适合的`.devcontainer/.env`配置文件。脚本需要：
- 支持多种端口检查方式（lsof, netstat等）
- 自动为占用的端口找到可用的替代端口
- 清晰地展示端口配置结果

## 执行步骤

1. 创建`check_ports.sh`脚本：

```bash
#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 定义要检查的端口和服务名称
SERVICES=("FRONTEND_PORT" "BACKEND_PORT" "POSTGRES_PORT" "REDIS_PORT")
DEFAULT_PORTS=(5173 8000 5432 6379)

# 定义端口占用检查函数
is_port_in_use() {
    if command -v lsof &> /dev/null; then
        lsof -i :"$1" &> /dev/null
        return $?
    elif command -v netstat &> /dev/null; then
        netstat -tuln | grep :"$1" &> /dev/null
        return $?
    else
        (echo > /dev/tcp/localhost/"$1") &> /dev/null
        return $?
    fi
}

# 查找下一个可用端口
find_next_available_port_silent() {
    local port=$1
    while is_port_in_use "$port"; do
        ((port++))
    done
    echo "$port"
}

# 创建env文件
mkdir -p .devcontainer
echo -e "# SDUI开发环境自定义端口配置" > .devcontainer/.env.temp

# 检查每个端口并生成配置
for i in "${!SERVICES[@]}"; do
    service=${SERVICES[$i]}
    default_port=${DEFAULT_PORTS[$i]}
    
    # 检查端口是否被占用
    if is_port_in_use "$default_port"; then
        # 端口被占用，寻找下一个可用端口
        new_port=$(find_next_available_port_silent "$default_port")
        echo -e "$service=$new_port" >> .devcontainer/.env.temp
    fi
done

# 移动临时文件到最终位置
mv .devcontainer/.env.temp .devcontainer/.env
```

2. 为脚本添加执行权限：

```bash
chmod +x check_ports.sh
```

3. 修改README.md添加使用说明：

```markdown
### 自动端口配置

项目提供了一个自动检查宿主机端口占用情况并生成配置的脚本：

```bash
# 运行端口检查脚本
./check_ports.sh
```
```

## 结果验证

1. 运行脚本以检查占用的端口并生成配置
2. 确认脚本正确识别了占用的端口，如Redis和PostgreSQL
3. 查看生成的`.devcontainer/.env`文件，确认格式正确
4. 重建开发容器，验证是否可以使用新的端口配置成功启动

测试结果表明，该脚本可以成功检测端口占用情况，并自动生成有效的配置文件，大大简化了开发环境设置过程。

## 相关资源

- [端口检查脚本](../check_ports.sh)
- [端口配置文档](./port-configuration.md)

## 注意事项

1. 脚本使用了较为基础的bash功能，兼容大多数Unix/Linux/macOS环境
2. 在Windows环境中可能需要通过WSL或Git Bash运行
3. 脚本会检查`lsof`和`netstat`命令是否可用，并选择合适的方法检测端口占用
4. 生成的配置只包含被占用端口的替代值，未被占用的端口会使用默认值 