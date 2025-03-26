#!/bin/bash
# 配置Docker镜像加速脚本

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}正在配置Docker镜像加速...${NC}"

# 检测操作系统
if [ "$(uname)" == "Darwin" ]; then
    # macOS系统
    echo -e "${YELLOW}检测到macOS系统${NC}"
    
    # 检查Docker Desktop是否已配置
    if [ -f ~/Library/Group\ Containers/group.com.docker/settings.json ]; then
        echo -e "${YELLOW}配置Docker Desktop镜像加速...${NC}"
        # 备份原始配置
        cp ~/Library/Group\ Containers/group.com.docker/settings.json ~/Library/Group\ Containers/group.com.docker/settings.json.bak
        
        # 添加镜像配置
        jq '.["registry-mirrors"] = ["https://registry.docker-cn.com", "https://docker.mirrors.ustc.edu.cn", "https://hub-mirror.c.163.com"]' ~/Library/Group\ Containers/group.com.docker/settings.json > ~/Library/Group\ Containers/group.com.docker/settings.json.tmp
        mv ~/Library/Group\ Containers/group.com.docker/settings.json.tmp ~/Library/Group\ Containers/group.com.docker/settings.json
        
        echo -e "${GREEN}Docker Desktop镜像加速配置完成，请重启Docker Desktop生效${NC}"
    else
        echo -e "${YELLOW}未找到Docker Desktop配置文件，请手动配置镜像加速${NC}"
    fi
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Linux系统
    echo -e "${YELLOW}检测到Linux系统${NC}"
    
    # 检查Docker配置目录
    if [ ! -d /etc/docker ]; then
        sudo mkdir -p /etc/docker
    fi
    
    # 配置镜像加速
    echo -e "${YELLOW}配置Docker镜像加速...${NC}"
    echo '{
  "registry-mirrors": [
    "https://registry.docker-cn.com",
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}' | sudo tee /etc/docker/daemon.json
    
    # 重启Docker服务
    echo -e "${YELLOW}重启Docker服务...${NC}"
    if command -v systemctl &> /dev/null; then
        sudo systemctl daemon-reload
        sudo systemctl restart docker
    else
        sudo service docker restart
    fi
    
    echo -e "${GREEN}Docker镜像加速配置完成${NC}"
else
    # 不支持的操作系统
    echo -e "${YELLOW}不支持的操作系统，请手动配置Docker镜像加速${NC}"
fi

echo -e "${GREEN}配置完成!${NC}"
echo -e "${YELLOW}提示: 国内镜像源已配置，依赖安装速度应该会显著提升。${NC}" 