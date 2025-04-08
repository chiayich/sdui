"""SDUI配置数据验证和序列化模型

职责：
1. 定义数据验证规则和序列化规范
2. 处理API请求和响应的数据结构
3. 提供类型安全和数据转换
4. 定义不同场景的数据模型（创建、更新、查询等）

主要模型说明：
- UIConfigData: UI配置的核心数据结构，定义组件和布局
- SDUIConfigBase: 基础配置模型，包含通用字段
- SDUIConfigCreate: 创建新配置时的数据模型
- SDUIConfigUpdate: 更新配置时的数据模型
- SDUIConfigInDB: 数据库模型映射，包含额外的数据库字段
- SDUIConfigQuery: 查询参数模型，用于过滤和搜索
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


# UI组件属性模型
class UIComponentProps(BaseModel):
    """UI组件属性定义"""

    style: Optional[Dict[str, Any]] = None
    className: Optional[str] = None
    disabled: Optional[bool] = None
    hidden: Optional[bool] = None


# UI组件事件模型
class UIComponentEvent(BaseModel):
    """UI组件事件定义"""

    type: str
    handler: str
    params: Optional[Dict[str, Any]] = None


# UI基础组件模型
class UIBaseComponent(BaseModel):
    """UI基础组件定义"""

    type: str
    id: str
    props: Optional[UIComponentProps] = None
    events: Optional[List[UIComponentEvent]] = None
    children: Optional[List["UIComponent"]] = None


# 容器组件
class UIContainer(UIBaseComponent):
    """容器组件定义"""

    type: Literal["container", "card", "form"] = "container"
    layout: Optional[Dict[str, Any]] = None


# 表单组件
class UIFormComponent(UIBaseComponent):
    """表单组件定义"""

    type: Literal["input", "select", "checkbox", "radio", "date"]
    name: str
    label: Optional[str] = None
    value: Optional[Any] = None
    rules: Optional[List[Dict[str, Any]]] = None


# 展示组件
class UIDisplayComponent(UIBaseComponent):
    """展示组件定义"""

    type: Literal["text", "image", "icon", "table"]
    content: Any = None


# 组合类型
UIComponent = Union[UIContainer, UIFormComponent, UIDisplayComponent]


# UI配置数据模型
class UIConfigData(BaseModel):
    """UI配置数据定义"""

    type: Literal["page", "component", "layout", "structure"]
    id: str
    title: Optional[str] = None
    content: Optional[List[UIComponent]] = None
    layout: Optional[Dict[str, Any]] = None
    styles: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = False


# 基础模型
class SDUIConfigBase(BaseModel):
    code: str = Field(..., description="配置唯一标识码，如 system.user, system.role")
    name: str = Field(..., description="配置名称")
    category: str = Field(..., description="配置分类：system, business, auth 等")
    config_data: UIConfigData
    description: Optional[str] = None


# 创建模型
class SDUIConfigCreate(SDUIConfigBase):
    pass


# 更新模型
class SDUIConfigUpdate(BaseModel):
    name: Optional[str] = None
    config_data: Optional[UIConfigData] = None
    description: Optional[str] = None


# 数据库内模型（包含自动字段）
class SDUIConfigInDB(SDUIConfigBase):
    id: UUID
    version: int
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
    code: Optional[str] = Field(None, description="配置代码")
    category: Optional[str] = Field(None, description="配置分类")
    is_active: Optional[bool] = Field(None, description="是否启用")
