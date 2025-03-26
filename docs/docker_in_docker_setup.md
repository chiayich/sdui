# 在开发容器中配置Docker

本文档介绍如何在VSCode开发容器中启用Docker功能，以便在容器内运行Docker命令。

## 方法一：配置Docker Socket挂载（推荐）

### 1. 修改开发容器配置

编辑 `.devcontainer/docker-compose.yml` 文件，添加Docker socket挂载：

```yaml
services:
  app:
    # ... 现有配置 ...
    volumes:
      - ..:/workspace:cached
      # 添加Docker socket挂载
      - /var/run/docker.sock:/var/run/docker.sock:cached
```

### 2. 更新权限配置脚本

编辑或创建 `.devcontainer/init.sh` 文件，添加以下内容来自动修复权限：

```bash
#!/bin/bash

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
    docker info > /dev/null 2>&1 && echo "✅ Docker权限配置成功！" || echo "❌ Docker权限配置失败，请尝试重启容器"
else
    echo "❌ Docker socket不存在，请确保Docker已安装并已将socket挂载到容器中"
fi
```

### 3. 确保脚本执行权限

```bash
chmod +x .devcontainer/init.sh
```

### 4. 重建开发容器

1. 打开VSCode命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）
2. 运行 "Remote-Containers: Rebuild Container"
3. 等待容器重建完成

## 方法二：使用Docker-in-Docker特性

如果您无法访问宿主机的Docker socket或需要隔离的Docker环境，可以使用Docker-in-Docker特性。

### 1. 修改 `.devcontainer/devcontainer.json`

```json
{
  // ... 现有配置 ...
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  }
}
```

### 2. 重建开发容器

1. 打开VSCode命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）
2. 运行 "Remote-Containers: Rebuild Container"
3. 等待容器重建完成

## 方法三：使用Docker CLI并连接宿主机Docker

如果以上方法不适用，可以在容器中安装Docker CLI并配置连接到宿主机Docker。

### 1. 在容器中安装Docker CLI

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce-cli docker-compose-plugin
```

### 2. 配置Docker环境变量

将以下内容添加到 `.bashrc` 或 `.zshrc` 文件中：

```bash
export DOCKER_HOST=tcp://host.docker.internal:2375
```

### 3. 在宿主机上启用Docker远程API

#### Linux:

```bash
sudo nano /etc/docker/daemon.json
```

添加以下内容：

```json
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"]
}
```

重启Docker：

```bash
sudo systemctl restart docker
```

#### macOS:

在Docker Desktop中，转到 "Preferences" -> "Docker Engine"，然后添加：

```json
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"]
}
```

点击 "Apply & Restart"。

## 验证配置

重建容器后，运行以下命令验证Docker是否正常工作：

```bash
docker info
docker run --rm hello-world
```

如果配置正确，这些命令应该成功执行，且不会出现权限错误。

## 注意事项

1. 挂载Docker socket方法会让容器内操作能够影响宿主机Docker环境，请确保仅在开发环境中使用。

2. Docker-in-Docker特性的缺点是会消耗更多资源，且容器内的Docker网络与宿主机隔离。

3. 在使用远程API方法时，请确保添加适当的安全限制，避免暴露Docker API到公共网络。 