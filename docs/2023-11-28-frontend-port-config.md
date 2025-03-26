# 前端开发服务端口配置问题解决

**日期**: 2023-11-28
**类别**: 前端/开发环境
**紧急程度**: 中

## 问题描述

前端应用在浏览器中打开时，WebSocket连接持续出现失败错误，导致热更新功能无法正常工作。错误信息显示浏览器在尝试连接默认的Vite开发服务器端口5173，而实际服务运行在端口3000上。

错误信息：
```
WebSocket connection to 'ws://localhost:5173/?token=xxx' failed: Error during WebSocket handshake: net::ERR_CONNECTION_RESET
[vite] server connection lost. polling for restart...
GET http://localhost:5173/ net::ERR_CONNECTION_RESET
```

这导致页面不断尝试重连，影响开发体验。

## 问题分析

通过分析配置文件和运行日志，确定了以下问题：

1. 在`/workspace/.devcontainer/start_services.sh`脚本中，前端服务被配置为使用端口3000：
   ```bash
   npm run dev -- --host 0.0.0.0 --port 3000
   ```

2. 而在`/workspace/frontend/vite.config.ts`中，Vite的服务器配置仍使用默认端口5173：
   ```javascript
   server: {
     host: '0.0.0.0',
     port: 5173,
     strictPort: true,
     // ...
     hmr: {
       clientPort: 5173
     }
   }
   ```

3. 这导致了端口不一致：服务实际运行在3000端口，但客户端代码尝试连接5173端口进行热更新。

## 解决思路

为确保前端开发服务器配置一致性，需要将Vite配置文件中的端口设置与启动脚本中的端口设置保持一致。由于项目已决定使用3000作为前端服务端口，应将Vite配置中的所有5173端口引用更改为3000。

## 执行步骤

1. 修改Vite配置文件`/workspace/frontend/vite.config.ts`：

```javascript
server: {
    host: '0.0.0.0',
    port: 3000,  // 从5173改为3000
    strictPort: true,
    watch: {
        usePolling: true
    },
    cors: true,
    hmr: {
        clientPort: 3000  // 从5173改为3000
    },
    // ...
}
```

2. 停止并重启前端开发服务器：

```bash
# 停止当前运行的前端服务
kill -9 $(ps aux | grep -E "node.*dev|npm.*dev" | grep -v grep | awk '{print $2}')

# 重新启动前端服务
cd /workspace/frontend && npm run dev -- --host 0.0.0.0 --port 3000
```

## 结果验证

修改配置并重启服务后，前端应用可以正常访问http://localhost:3000，WebSocket连接成功建立，热更新功能正常工作。不再出现尝试连接5173端口的错误信息。

## 相关资源

- [Vite配置文档](https://vitejs.dev/config/server-options.html)
- [WebSocket连接调试](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications)

## 注意事项

1. 在开发容器配置中，请确保所有与前端服务相关的端口配置保持一致性，包括：
   - `.devcontainer/devcontainer.json`中的`forwardPorts`
   - `.devcontainer/start_services.sh`中的启动命令
   - `frontend/vite.config.ts`中的服务器端口配置

2. 当修改端口配置后，必须完全重启前端服务，仅刷新浏览器页面可能不足以解决WebSocket连接问题。 