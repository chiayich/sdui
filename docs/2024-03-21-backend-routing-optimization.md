# 后端路由优化与调试

**日期**: 2024-03-21
**类别**: 后端
**紧急程度**: 中

## 问题描述

后端API路由配置存在问题，导致请求无法正确到达对应的处理函数。具体表现为创建记录的请求发送到了错误的URL路径（`/api/table-data/create`），而实际应该是 `/api/table-data`。

## 问题分析

1. 路由注册存在重复前缀：
   - `table_data.py` 中设置了 `/table-data` 前缀
   - `__init__.py` 中又添加了相同的前缀
   - `main.py` 中统一添加了 `/api` 前缀

2. 日志记录不够完整，难以快速定位问题

## 解决思路

1. 统一路由前缀配置：
   - 在 `table_data.py` 中设置基础路由前缀
   - 在 `main.py` 中统一添加 `/api` 前缀
   - 移除 `__init__.py` 中的重复前缀

2. 增强日志记录：
   - 添加请求信息的详细日志
   - 添加数据库操作的详细日志
   - 添加错误追踪和堆栈信息

## 执行步骤

1. 修改 `table_data.py` 中的路由配置：
```python
router = APIRouter(prefix="/table-data")
```

2. 简化 `__init__.py` 中的路由注册：
```python
router = APIRouter()
router.include_router(table_data_router)
```

3. 在 `main.py` 中统一添加API前缀：
```python
app.include_router(api_router, prefix="/api")
```

4. 添加更详细的日志记录

## 结果验证

1. 重启后端服务后，API路由结构如下：
   - POST `/api/table-data/search` - 搜索表格数据
   - POST `/api/table-data` - 创建新记录
   - PUT `/api/table-data/{item_id}` - 更新记录
   - DELETE `/api/table-data/{item_id}` - 删除记录

2. 使用Postman测试API接口，确保请求能够正确到达处理函数

## 相关资源

- [FastAPI路由文档](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [后端代码仓库](backend/app/)

## 注意事项

1. 避免在多个地方重复设置路由前缀
2. 保持完整的请求日志，便于问题定位
3. 定期检查路由配置的正确性 