# SDUI框架数据库Schema设置

**日期**: 2023-05-27
**类别**: 数据库
**紧急程度**: 中

## 问题描述

需要为SDUI框架创建专用的数据库schema，并配置适当的权限，确保数据库服务能正确访问和操作相关表。

## 问题分析

为了确保数据隔离和权限管理，SDUI框架需要一个专用的数据库schema。这样可以将框架的数据与其他应用数据分开管理，并且可以精确控制访问权限。同时，需要确保MCP服务配置正确引用这些schema和表。

## 解决思路

1. 创建专用的`sdui_schema`
2. 将现有的demo表移到新schema
3. 为用户授予适当的权限
4. 更新MCP配置文件，添加schema和表引用
5. 编写测试脚本验证连接和权限

## 执行步骤

1. 创建schema和设置权限

```sql
-- 创建SDUI专用schema
CREATE SCHEMA IF NOT EXISTS sdui_schema;

-- 将表移至新schema（如果表已存在于public schema）
ALTER TABLE IF EXISTS public.sdui_demo SET SCHEMA sdui_schema;

-- 如果表不存在，则在新schema中创建
CREATE TABLE IF NOT EXISTS sdui_schema.sdui_demo (
    id SERIAL PRIMARY KEY,
    component_type VARCHAR(50) NOT NULL,
    component_name VARCHAR(100) NOT NULL,
    properties JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 授予用户对schema的所有权限
GRANT ALL PRIVILEGES ON SCHEMA sdui_schema TO huajin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sdui_schema TO huajin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA sdui_schema TO huajin;

-- 设置默认搜索路径
ALTER USER huajin SET search_path TO sdui_schema, public;
```

2. 更新MCP配置

```json
{
    "configuration": {
        "connection": {
            "host": "localhost",
            "port": 5432,
            "database": "sdui",
            "user": "huajin",
            "password": "",
            "poolSize": 10,
            "idleTimeoutMillis": 30000,
            "schema": "sdui_schema"
        },
        "tables": {
            "components": "sdui_schema.sdui_demo",
            "templates": "sdui_schema.sdui_templates",
            "screens": "sdui_schema.sdui_screens",
            "users": "sdui_schema.sdui_users"
        }
    }
}
```

3. 编写测试脚本验证连接和权限

```javascript
// 相关测试代码可以查看项目根目录的test_db_connection.js
```

## 结果验证

执行以下命令验证设置是否正确：

```bash
# 执行SQL脚本
psql -d sdui -f create_sdui_schema.sql

# 测试连接和权限
node test_db_connection.js
```

测试输出应该显示：
- 成功连接到数据库
- 能够查询sdui_schema.sdui_demo表
- 能够执行插入操作（权限测试）

## 相关资源

- [数据库服务MCP配置](.cursor/mcp/database-service.mcp.json)
- [数据库结构SQL脚本](create_sdui_schema.sql)
- [数据库连接测试脚本](test_db_connection.js)

## 注意事项

- 在不同环境部署时，需要为相应的数据库用户设置正确的权限
- 后续添加新表时，需要确保它们都放在sdui_schema中
- 考虑使用迁移工具管理数据库变更，确保不同环境之间的一致性 