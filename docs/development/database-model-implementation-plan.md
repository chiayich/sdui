# SDUI 数据库模型实现计划

**日期**: 2024-04-05
**作者**: 技术团队
**状态**: 草稿

## 概述

本文档详细说明SDUI项目的数据库模型设计和实现计划，作为从内存数据向持久化存储迁移的指导。文档包含数据库表设计、关系定义、索引策略和迁移计划。

## 数据库技术选择

- **数据库系统**: PostgreSQL 14+
- **ORM框架**: SQLAlchemy 2.0
- **迁移工具**: Alembic
- **连接池**: asyncpg

## 数据模型设计

### 1. UI模板表 (ui_templates)

存储UI页面模板的基本信息。

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UITemplate(Base):
    __tablename__ = "ui_templates"
    
    id = Column(Integer, primary_key=True)
    template_key = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String(20), nullable=False)
    platform = Column(String(20), nullable=False, default="web")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(50), nullable=True)
```

### 2. 组件表 (components)

存储UI组件的详细配置。

```python
class Component(Base):
    __tablename__ = "components"
    
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("ui_templates.id", ondelete="CASCADE"))
    component_key = Column(String(50), nullable=False)
    component_type = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey("components.id", ondelete="CASCADE"), nullable=True)
    position = Column(Integer, nullable=False)
    properties = Column(JSONB, nullable=False, default={})
    style = Column(JSONB, nullable=False, default={})
    events = Column(JSONB, nullable=False, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    template = relationship("UITemplate", back_populates="components")
    parent = relationship("Component", back_populates="children", remote_side=[id])
    children = relationship("Component", back_populates="parent")
```

### 3. 模板变体表 (template_variants)

支持A/B测试和个性化的模板变体。

```python
class TemplateVariant(Base):
    __tablename__ = "template_variants"
    
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("ui_templates.id", ondelete="CASCADE"))
    variant_name = Column(String(50), nullable=False)
    conditions = Column(JSONB, nullable=False, default={})
    weight = Column(Integer, default=50)  # 权重，用于A/B测试流量分配
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    template = relationship("UITemplate", back_populates="variants")
```

### 4. 数据源表 (data_sources)

定义UI组件数据源的配置。

```python
class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True)
    source_key = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(20), nullable=False)  # api, static, compute
    config = Column(JSONB, nullable=False)
    cache_ttl = Column(Integer, default=0)  # 缓存时间，0表示不缓存
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### 5. 组件数据绑定表 (component_bindings)

定义组件与数据源的绑定关系。

```python
class ComponentBinding(Base):
    __tablename__ = "component_bindings"
    
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey("components.id", ondelete="CASCADE"))
    data_source_id = Column(Integer, ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=True)
    property_path = Column(String(100), nullable=False)  # 组件属性路径
    binding_type = Column(String(20), nullable=False)  # direct, expression, computed
    binding_value = Column(Text, nullable=False)  # 绑定值或表达式
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    component = relationship("Component", back_populates="bindings")
    data_source = relationship("DataSource", back_populates="bindings")
```

## 索引策略

```sql
-- UI模板表索引
CREATE INDEX idx_ui_templates_platform ON ui_templates(platform);
CREATE INDEX idx_ui_templates_is_active ON ui_templates(is_active);

-- 组件表索引
CREATE INDEX idx_components_template_id ON components(template_id);
CREATE INDEX idx_components_parent_id ON components(parent_id);
CREATE INDEX idx_components_component_type ON components(component_type);

-- 模板变体表索引
CREATE INDEX idx_template_variants_template_id ON template_variants(template_id);
CREATE INDEX idx_template_variants_is_active ON template_variants(is_active);

-- 组件数据绑定表索引
CREATE INDEX idx_component_bindings_component_id ON component_bindings(component_id);
CREATE INDEX idx_component_bindings_data_source_id ON component_bindings(data_source_id);
```

## 查询优化

关键查询场景及优化策略：

1. **获取模板及其组件树**:
   ```python
   # 使用递归CTE查询组件树
   async def get_template_with_components(template_key):
       async with db.transaction():
           # 获取模板
           template = await db.fetch_one(
               "SELECT * FROM ui_templates WHERE template_key = $1", 
               template_key
           )
           
           if not template:
               return None
               
           # 使用递归CTE获取组件树
           components = await db.fetch_all(
               """
               WITH RECURSIVE component_tree AS (
                   SELECT c.*, 0 AS level
                   FROM components c
                   WHERE c.template_id = $1 AND c.parent_id IS NULL
                   
                   UNION ALL
                   
                   SELECT c.*, ct.level + 1
                   FROM components c
                   JOIN component_tree ct ON c.parent_id = ct.id
               )
               SELECT * FROM component_tree ORDER BY level, position
               """,
               template["id"]
           )
           
           # 构建组件树
           # ...
   ```

2. **基于条件选择模板变体**:
   ```python
   # 查找匹配的模板变体
   async def find_matching_variant(template_id, context):
       # 使用JSONB操作符匹配条件
       variant = await db.fetch_one(
           """
           SELECT * FROM template_variants
           WHERE template_id = $1
             AND is_active = true
             AND (start_date IS NULL OR start_date <= NOW())
             AND (end_date IS NULL OR end_date >= NOW())
             AND conditions @> $2::jsonb
           ORDER BY weight DESC
           LIMIT 1
           """,
           template_id, json.dumps(context)
       )
       return variant
   ```

## 迁移策略

### 1. 初始化迁移

使用Alembic创建初始迁移脚本：

```bash
# 初始化Alembic
alembic init migrations

# 生成初始迁移
alembic revision --autogenerate -m "Create initial tables"

# 应用迁移
alembic upgrade head
```

### 2. 数据填充

创建数据种子脚本，迁移现有的硬编码模板：

```python
# backend/app/db/seed.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.db_models import UITemplate, Component

async def seed_demo_templates():
    """填充演示模板数据"""
    async with AsyncSession(get_db()) as session:
        # 检查是否已存在
        existing = await session.execute(
            select(UITemplate).where(UITemplate.template_key == "home")
        )
        if existing.first():
            print("演示数据已存在，跳过")
            return
            
        # 创建首页模板
        home_template = UITemplate(
            template_key="home",
            name="首页",
            description="应用首页",
            version="1.0.0",
            platform="web"
        )
        session.add(home_template)
        await session.flush()
        
        # 添加组件
        # ...
        
        await session.commit()
        print("演示数据填充完成")

if __name__ == "__main__":
    asyncio.run(seed_demo_templates())
```

## 数据库访问层设计

### 1. 数据库连接

```python
# backend/app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)

async def get_db():
    """获取数据库会话"""
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
```

### 2. 数据库模型操作

```python
# backend/app/db/crud/template_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional

from app.models.db_models import UITemplate, Component

class TemplateCRUD:
    """UI模板数据库操作"""
    
    @staticmethod
    async def get_template(db: AsyncSession, template_key: str) -> Optional[UITemplate]:
        """获取模板"""
        result = await db.execute(
            select(UITemplate).where(UITemplate.template_key == template_key)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_template_components(db: AsyncSession, template_id: int) -> List[Component]:
        """获取模板组件"""
        result = await db.execute(
            select(Component)
            .where(Component.template_id == template_id)
            .order_by(Component.parent_id.nullsfirst(), Component.position)
        )
        return result.scalars().all()
    
    @staticmethod
    async def create_template(db: AsyncSession, template_data: dict) -> UITemplate:
        """创建模板"""
        template = UITemplate(**template_data)
        db.add(template)
        await db.flush()
        return template
    
    @staticmethod
    async def update_template(db: AsyncSession, template_id: int, template_data: dict) -> Optional[UITemplate]:
        """更新模板"""
        await db.execute(
            update(UITemplate)
            .where(UITemplate.id == template_id)
            .values(**template_data)
        )
        await db.flush()
        result = await db.execute(
            select(UITemplate).where(UITemplate.id == template_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def delete_template(db: AsyncSession, template_id: int) -> bool:
        """删除模板"""
        result = await db.execute(
            delete(UITemplate).where(UITemplate.id == template_id)
        )
        await db.flush()
        return result.rowcount > 0
```

## 下一步实施计划

1. **迁移准备** (1天)
   - 配置数据库连接
   - 设置Alembic
   - 创建ORM模型

2. **数据库实施** (2天)
   - 生成并应用迁移
   - 开发数据访问层
   - 创建数据种子

3. **API集成** (2天)
   - 重构现有API使用数据库
   - 完善错误处理
   - 添加数据验证

## 风险与缓解措施

1. **性能风险**:
   - 复杂查询可能影响响应时间
   - 缓解：实现缓存层，优化查询，添加适当索引

2. **数据一致性**:
   - 复杂组件树更新可能导致不一致
   - 缓解：使用事务，实现乐观锁

3. **迁移风险**:
   - 从硬编码数据到数据库的迁移可能引入问题
   - 缓解：编写完整测试，实施分阶段迁移 