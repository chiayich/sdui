import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, JSON, ForeignKey, Integer, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class SDUIConfig(Base):
    """SDUI配置模型，存储UI配置数据"""
    
    __tablename__ = "sdui_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    config_type = Column(String, nullable=False)  # 配置类型：page, component, structure
    content = Column(JSON, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 创建联合索引
    __table_args__ = (
        Index('ix_sdui_configs_code_type', 'code', 'config_type'),
    )
    
    def __repr__(self):
        return f"<SDUIConfig {self.code}>"

    # 关联创建者和更新者，使用整数ID
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updater_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    creator = relationship("User", foreign_keys=[creator_id], backref="created_configs")
    updater = relationship("User", foreign_keys=[updater_id], backref="updated_configs") 