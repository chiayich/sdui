# SDUI数据库初始化说明

## 目录结构

```
postgres-init/
├── README.md
├── schemas/
│   ├── 01_create_tables.sql    # 创建数据库表结构
│   └── 02_init_data.sql        # 初始化基础数据
└── data/                       # 环境特定的数据（可选）
    ├── dev/
    └── test/
```

## 初始化顺序

数据库初始化脚本按以下顺序执行：

1. `schemas/01_create_tables.sql`
   - 创建schema
   - 创建基础表结构
   - 创建索引和约束
   - 创建触发器

2. `schemas/02_init_data.sql`
   - 插入基础UI配置
   - 插入组件配置
   - 插入布局配置
   - 建立组件关系

## 表结构说明

### sdui_configs
- 存储所有UI配置（页面、组件、布局等）
- 使用JSONB类型存储灵活的配置内容
- 支持版本控制和审计追踪

### sdui_config_versions
- 记录配置的历史版本
- 支持配置回滚和版本比较

### sdui_config_relations
- 管理配置之间的关系（如页面包含组件）
- 支持组件的复用和组合

### sdui_audit_logs
- 记录所有配置变更
- 支持变更追踪和审计

## 使用说明

1. 确保PostgreSQL服务已启动
2. 创建数据库：
   ```bash
   createdb -U postgres sdui
   ```

3. 执行初始化脚本：
   ```bash
   psql -U postgres -d sdui -f schemas/01_create_tables.sql
   psql -U postgres -d sdui -f schemas/02_init_data.sql
   ```

4. 验证初始化：
   ```sql
   SELECT code, name, config_type FROM sdui_schema.sdui_configs;
   ```

## 环境特定配置

- 开发环境：使用 `data/dev/` 目录下的数据
- 测试环境：使用 `data/test/` 目录下的数据
- 生产环境：仅使用基础配置，通过应用程序管理数据

## 注意事项

1. 所有表都在 `sdui_schema` schema下
2. 使用 `IF NOT EXISTS` 确保脚本可重复执行
3. 使用事务确保数据一致性
4. 保持向后兼容性
