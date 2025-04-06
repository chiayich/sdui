# SDUI配置数据库持久化与连接优化

**日期**: 2024-05-30
**类别**: 后端/数据库
**紧急程度**: 高

## 问题描述

SDUI项目中存在两个主要问题需要解决：

1. **UI配置硬编码**: UI配置目前直接硬编码在`sdui_service.py`文件的`DEFAULT_SDUI_CONFIGS`变量中，而非存储在数据库中，这不利于配置的动态更新和管理。
2. **数据库连接重复定义**: 存在多个地方定义数据库连接配置，如`database.py`和`session.py`，导致连接管理混乱和可能的资源浪费。

## 问题分析

1. **UI配置硬编码问题**:
   - 硬编码配置难以动态修改和管理
   - 无法实现版本控制和历史记录
   - 修改配置需要重新部署应用
   - 不符合最佳实践，应将配置存储在数据库中

2. **数据库连接问题**:
   - 在`database.py`和`session.py`中都定义了数据库连接
   - 连接URL不一致，存在硬编码URL与配置文件URL两种
   - `database.py`使用`databases`库，而`session.py`使用`SQLAlchemy`直接连接
   - 缺乏统一的连接管理策略

## 解决思路

1. **UI配置持久化**:
   - 保留`DEFAULT_SDUI_CONFIGS`作为初始化数据和迁移来源
   - 创建迁移脚本将硬编码配置迁移到数据库
   - 修改相关服务和API使用数据库中的配置
   - 在初始化数据库时执行配置迁移

2. **数据库连接优化**:
   - 统一使用`SQLAlchemy`进行数据库连接
   - 在`database.py`中定义单一的连接管理
   - 重构`session.py`为导入复用模式
   - 优化连接池配置和生命周期管理

## 执行步骤

### 1. UI配置迁移模块实现

创建迁移模块`backend/app/db/migrate_sdui_configs.py`：

```python
import logging
from sqlalchemy.orm import Session
from app import crud
from app.schemas.sdui_config import SDUIConfigCreate
from app.services.sdui_service import DEFAULT_SDUI_CONFIGS

logger = logging.getLogger(__name__)

def migrate_default_configs(db: Session) -> None:
    """将默认的SDUI配置从代码中迁移到数据库"""
    
    logger.info("开始迁移默认SDUI配置到数据库...")
    
    for config in DEFAULT_SDUI_CONFIGS:
        # 检查配置是否已存在
        existing = crud.sdui_config.get_by_code(db, code=config["code"])
        
        if not existing:
            # 创建新配置
            sdui_config_in = SDUIConfigCreate(
                code=config["code"],
                name=config["name"],
                config_type="page",  # 默认为页面类型
                content=config["config_data"],
                description=config.get("description", "")
            )
            
            try:
                new_config = crud.sdui_config.create(db, obj_in=sdui_config_in)
                logger.info(f"成功创建配置: {new_config.code}")
            except Exception as e:
                logger.error(f"创建配置 {config['code']} 失败: {str(e)}")
        else:
            logger.info(f"配置 {config['code']} 已存在，跳过")
    
    logger.info("默认SDUI配置迁移完成")
```

### 2. SDUI服务改造

修改`sdui_service.py`，增加从数据库获取配置的方法：

```python
def get_ui_config(db: Session, code: str, user: User = None) -> Optional[Dict]:
    """
    根据配置代码从数据库获取UI配置
    如果是特殊页面（如system），则动态生成配置
    """
    # 特殊处理system页面，动态生成配置
    if code == "system":
        return get_system_page_config(db, user)
    
    # 其他页面从数据库获取配置
    config = crud.sdui_config.get_by_code(db, code=code)
    if not config:
        return None
    
    return config.content
```

### 3. 数据库连接管理优化

统一数据库连接管理在`database.py`：

```python
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings

logger = logging.getLogger(__name__)

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 连接池预检测
    pool_recycle=3600,   # 一小时后回收连接
    echo=settings.SQLALCHEMY_ECHO  # 是否打印SQL语句
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

async def startup_db() -> None:
    """数据库启动连接"""
    logger.info(f"数据库连接URL: {settings.DATABASE_URL}")
    # 检查数据库连接
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        logger.info("数据库连接成功")
        db.close()
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        raise

async def shutdown_db() -> None:
    """关闭数据库连接"""
    logger.info("关闭数据库连接")
    # SQLAlchemy会自动管理连接池的关闭

def get_db() -> Generator[Session, None, None]:
    """数据库会话依赖项"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

通过依赖项引用重构`session.py`：

```python
from app.db.database import engine, SessionLocal, Base

# 重新导出数据库会话和基类，避免重复定义
# 这个文件保留是为了保持向后兼容性，新代码应直接导入database.py
```

### 4. 创建独立的迁移脚本

创建脚本`backend/migrate_configs.py`：

```python
#!/usr/bin/env python
"""
SDUI 配置数据库迁移脚本
将hardcoded的配置迁移到数据库中
"""
import sys
import os
import logging
from pathlib import Path

# 将backend目录添加到系统路径，以便能够导入app包
sys.path.append(str(Path(__file__).parent))

from app.db.session import SessionLocal
from app.db.migrate_sdui_configs import migrate_default_configs

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("migration.log")
    ]
)

logger = logging.getLogger(__name__)

def main():
    """运行配置迁移"""
    logger.info("开始SDUI配置迁移...")
    
    # 创建数据库会话
    db = SessionLocal()
    try:
        # 执行迁移
        migrate_default_configs(db)
        db.commit()
        logger.info("SDUI配置迁移完成")
    except Exception as e:
        db.rollback()
        logger.error(f"迁移失败: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
```

### 5. 更新初始化数据库流程

在`init_db.py`中增加配置迁移调用：

```python
# 在初始化数据库函数中添加
def init_db(db: Session) -> None:
    # ... 其他初始化代码 ...
    
    # 初始化SDUI配置
    init_sdui_config(db)
    
    # 将默认SDUI配置迁移到数据库
    migrate_default_configs(db)
    
    # ... 其他初始化代码 ...
```

## 结果验证

1. **数据库模型验证**:
   - 检查SDUIConfig模型是否正确定义并能够存储配置数据
   - 验证模型字段映射是否与现有配置数据匹配

2. **数据迁移验证**:
   - 执行迁移脚本，确认所有DEFAULT_SDUI_CONFIGS能正确迁移到数据库
   - 检查迁移后的数据完整性和正确性

3. **服务访问验证**:
   - 验证更新后的服务能正确从数据库获取UI配置
   - 测试特殊页面的动态配置生成逻辑

4. **数据库连接验证**:
   - 监控数据库连接数量，确保不存在连接泄漏
   - 验证应用启动和关闭时连接管理是否正常
   - 检查数据库操作性能是否符合预期

## 相关资源

- [SQLAlchemy连接池文档](https://docs.sqlalchemy.org/en/14/core/pooling.html)
- [FastAPI依赖项文档](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [数据库迁移最佳实践](https://docs.sqlalchemy.org/en/14/core/metadata.html#alembic)

## 注意事项

1. 在生产环境执行迁移前，应先备份现有数据库
2. 迁移脚本具有幂等性，可重复执行而不会导致数据重复
3. 后续所有UI配置的变更应通过API更新数据库，不应再修改代码中的DEFAULT_SDUI_CONFIGS
4. 随着项目发展，可能需要考虑实现配置版本管理机制 