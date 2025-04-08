import uuid
from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""SDUI配置数据库模型

职责：
1. 定义数据库表结构和关系映射
2. 负责与数据库的直接交互
3. 定义字段类型、索引和约束
4. 管理与其他表的关系（如用户表）

主要字段说明：
- id: 主键，UUID类型
- code: 配置唯一标识码，如 system.user, system.role
- name: 配置名称
- category: 配置分类，如 page, component, structure
- config_data: JSON类型，存储实际的UI配置数据
- version: 版本号，用于跟踪配置更新
- description: 配置描述
- is_active: 配置是否启用
"""


class SDUIConfig(Base):
    """SDUI配置模型，存储UI配置数据"""

    __tablename__ = "sdui_configs"
    __table_args__ = (
        Index("ix_sdui_configs_code_category", "code", "category"),
        {"schema": "sdui_schema"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # 配置类型：page, component, structure
    version = Column(Integer, nullable=False, default=1)
    config_data = Column(JSON, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<SDUIConfig {self.code}>"

    # 关联创建者和更新者
    creator_id = Column(
        UUID(as_uuid=True), ForeignKey("sdui_schema.users.id"), nullable=True
    )
    updater_id = Column(
        UUID(as_uuid=True), ForeignKey("sdui_schema.users.id"), nullable=True
    )
    creator = relationship("User", foreign_keys=[creator_id], backref="created_configs")
    updater = relationship("User", foreign_keys=[updater_id], backref="updated_configs")
