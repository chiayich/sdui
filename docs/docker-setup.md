# SDUI框架Docker设置指南

**日期**: 2023-05-28
**类别**: 部署
**紧急程度**: 中

## 项目描述

本项目是一个基于Docker的SDUI（服务器驱动UI）框架，包含前端、后端和缓存服务。前端使用Vue 3，后端使用FastAPI，通过PostgreSQL存储数据，Redis用于缓存。

## 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- PostgreSQL 14+
- 至少2GB RAM

## 项目结构

```
.
├── backend/                # 后端FastAPI应用
│   ├── app/                # 应用源码
│   │   ├── main.py         # 应用入口
│   │   ├── config.py       # 配置文件
│   │   ├── routers/        # API路由
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # 数据验证模式
│   │   └── services/       # 业务逻辑服务
│   ├── requirements.txt    # 依赖列表
│   └── Dockerfile          # 后端Docker配置
├── frontend/               # 前端Vue应用
│   ├── src/                # 源代码
│   │   ├── main.ts         # 入口文件
│   │   ├── App.vue         # 根组件
│   │   ├── router/         # 路由
│   │   ├── components/     # 组件
│   │   ├── views/          # 视图
│   │   └── stores/         # 状态管理
│   ├── package.json        # 依赖配置
│   └── Dockerfile          # 前端Docker配置
├── docs/                   # 文档
├── docker-compose.yml      # Docker Compose配置
└── README.md               # 项目说明
```

## 启动步骤

1. 确保数据库已设置好（参考docs/database-setup.md）

2. 构建并启动服务
```bash
docker-compose up -d
```

3. 检查服务是否正常运行
```bash
docker-compose ps
```

4. 访问应用
   - 前端: http://localhost:5173
   - API: http://localhost:8000
   - API文档: http://localhost:8000/docs

## 常见问题解决

### 问题: 无法连接到PostgreSQL数据库

解决方案:
- 检查PostgreSQL服务是否正在运行
- 验证环境变量中的数据库连接信息
- 确保sdui_schema已创建并授权

### 问题: 前端开发服务器启动失败

解决方案:
- 检查node_modules是否已安装
- 尝试删除node_modules后重新安装
- 检查端口5173是否被占用

## 开发模式

在开发过程中，可以使用以下命令来实时查看日志：

```bash
docker-compose logs -f
```

要单独重启某个服务：

```bash
docker-compose restart [service_name]
```

## 注意事项

- 不要在生产环境中使用默认的密钥
- 确保数据库定期备份
- 开发环境中的Hot Reload可能导致性能下降 