from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


# 基础模型
class SDUIConfigBase(BaseModel):
    code: str
    name: str
    config_type: str
    content: Dict[str, Any]
    description: Optional[str] = None


# 创建模型
class SDUIConfigCreate(SDUIConfigBase):
    pass


# 更新模型
class SDUIConfigUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


# 数据库内模型（包含自动字段）
class SDUIConfigInDB(SDUIConfigBase):
    id: UUID
    version: int
    config_data: Dict[str, Any]
    creator_id: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# 返回模型
class SDUIConfig(SDUIConfigInDB):
    pass


# 查询参数模型
class SDUIConfigQuery(BaseModel):
    code: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None 