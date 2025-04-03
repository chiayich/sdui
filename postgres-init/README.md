# SDUI数据库设计文档

本目录包含SDUI框架的数据库设计和初始化脚本。这些脚本定义了存储UI模板、组件和相关数据的数据库结构。

## 相关设计文档

- [SDUI存储设计总结](../docs/architecture/2025-03-28-sdui-storage-design-summary.md)
- [页面数据存储设计](../docs/architecture/2025-03-28-sdui-page-data-storage-design.md)

## 数据库目录结构

```
postgres-init/
├── schemas/                # 数据库模式定义（DDL）
│   ├── 01_sdui_tables.sql  # 基础表结构定义
│   └── 02_sdui_functions.sql # 函数和触发器定义
├── data/                   # 示例数据（DML）
│   └── 01_sample_templates.sql # 示例UI模板数据
└── README.md               # 本文档
```

## 数据库表设计

SDUI框架的数据库设计基于以下核心表：

### 基础数据表

1. **ui_templates** - 存储UI模板的基本信息

    - 每个模板对应一个屏幕（如首页、详情页）
    - 包含版本信息和元数据

2. **ui_components** - 存储UI组件信息

    - 组件树结构通过parent_id实现
    - 每个组件包含类型、属性、样式和事件信息
    - 使用JSONB类型存储灵活的属性数据

3. **ui_template_versions** - 存储模板的历史版本

    - 每当模板版本更新时自动创建快照
    - 使用JSONB存储完整的模板和组件树

### 功能扩展表

1. **ui_template_variants** - 存储A/B测试变体配置

    - 用于实现个性化和A/B测试
    - 包含变体选择条件和权重

2. **ui_variant_components** - 存储变体特定的组件覆盖

    - 仅存储与基本模板不同的组件配置

3. **ui_template_usage** - 记录模板使用情况

    - 用于分析和优化
    - 收集性能和设备信息

4. **ui_audit_log** - 记录所有变更的审计日志

    - 跟踪谁在何时进行了何种修改
    - 存储修改前后的完整数据

## 数据库关系模型

```
ui_templates (1) --- (*) ui_components
      |                       |
      |                       |  
      v                       v
ui_template_versions    ui_components (self-referencing)
      |
      |
      v
ui_template_variants (1) --- (*) ui_variant_components
```

## 数据库自动化功能

系统包含几个自动化功能：

1. **自动更新时间戳** - 记录记录的最后修改时间
2. **自动创建版本** - 当模板版本号变更时创建历史快照
3. **审计日志** - 自动记录所有数据变更
4. **递归组件树构建** - 以JSON格式构建完整的组件树

## 数据库初始化流程

数据库初始化应按以下顺序执行脚本：

1. 首先执行表结构定义: `01_sdui_tables.sql`
2. 然后执行函数和触发器: `02_sdui_functions.sql`
3. 最后加载示例数据: `01_sample_templates.sql`

## 部署与配置说明

在开发环境中，这些脚本将自动由Docker容器在启动时执行。在生产环境中，应由数据库管理员按需执行。

### PostgreSQL技术要求

这些脚本要求PostgreSQL 12或更高版本，以支持递归CTE和JSONB功能。

### 数据库连接配置

默认连接参数：

- 数据库: sdui
- 用户: postgres
- 密码: postgres
- 端口: 5432

这些参数可以通过环境变量修改（参见docker-compose.yml）。 