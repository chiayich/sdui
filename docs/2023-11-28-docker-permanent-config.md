# 开发容器Docker配置持久化实现

**日期**: 2023-11-28
**类别**: 工具/DevOps
**紧急程度**: 中

## 问题描述

在开发容器重建(Rebuild Container)后，手动配置的Docker环境变量和客户端设置会丢失，导致每次重建容器后都需要重新配置Docker环境，影响开发效率和监控服务的使用。主要表现为：

1. 手动添加到`~/.bashrc`的Docker环境变量会被重置
2. 手动修改的Docker客户端配置文件(`~/.docker/config.json`)会被重置
3. 导致重建容器后监控服务无法正常启动，需要重新进行Docker配置

## 问题分析

开发容器的本质是一个临时环境，容器重建时会基于Dockerfile和容器配置重新构建，并不会保留上一次运行时的用户修改。具体原因：

1. **容器文件系统特性**：容器重建时，所有未持久化到挂载卷的文件修改都会丢失
2. **用户主目录非持久化**：`/home/vscode/`目录下的修改未被配置为持久化
3. **初始化流程问题**：容器初始化脚本(`init.sh`)中未包含Docker客户端配置

## 解决思路

为了解决这个问题，需要在容器的初始化阶段就完成Docker客户端配置，确保每次容器重建后都能自动应用正确的配置：

1. **修改初始化脚本**：更新`.devcontainer/init.sh`脚本，添加Docker客户端配置部分
2. **自动化配置流程**：自动创建并配置Docker客户端设置文件
3. **环境变量持久化**：确保Docker环境变量被正确添加到`.bashrc`文件中
4. **验证机制**：在初始化脚本中添加验证步骤，确保配置生效

## 执行步骤

1. **修改开发容器初始化脚本**，添加Docker配置部分：

```bash
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
```

2. **确保脚本有执行权限**：

```bash
chmod +x /workspace/.devcontainer/init.sh
```

## 结果验证

通过以下步骤验证解决方案：

1. **重建开发容器**：
   - 在VS Code中，使用命令面板(Ctrl+Shift+P)执行"Dev Containers: Rebuild Container"
   - 或者在开发容器终端执行`exit`后重新连接到容器

2. **验证Docker环境变量**：
```bash
echo $DOCKER_HOST
# 应输出：unix:///var/run/docker.sock
```

3. **验证Docker配置文件**：
```bash
cat ~/.docker/config.json
# 应包含正确的配置，没有desktop相关设置
```

4. **验证Docker功能**：
```bash
docker info
# 应成功显示Docker信息，而不是连接错误
```

5. **启动监控服务**：
```bash
cd /workspace/monitoring && ./start-monitoring.sh
# 服务应该能够正常启动
```

## 相关资源

- [VS Code Dev Containers文档](https://code.visualstudio.com/docs/remote/containers)
- [Docker开发环境最佳实践](https://docs.docker.com/develop/dev-best-practices/)
- 修改的文件:
  - `/workspace/.devcontainer/init.sh`

## 注意事项

1. **初始化脚本执行时机**：初始化脚本会在容器创建后运行，而不是每次启动容器时都运行，因此这些修改只会在Rebuild容器时生效，而不是仅重启容器时。

2. **权限需求**：脚本需要有足够权限访问Docker套接字，确保Docker组权限配置正确。

3. **Docker命令行工具依赖**：确保开发容器中已安装Docker CLI工具，否则验证步骤可能失败。

4. **多用户环境**：在多用户环境中，可能需要为每个用户单独配置Docker权限和环境变量。 