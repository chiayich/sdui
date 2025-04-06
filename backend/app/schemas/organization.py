from typing import List, Optional, Union, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

# 基本的组织节点模型
class OrganizationNodeBase(BaseModel):
    name: str
    code: str
    node_type: str
    parent_id: Optional[int] = None


class OrganizationNodeCreate(OrganizationNodeBase):
    pass


class OrganizationNodeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    node_type: Optional[str] = None


class OrganizationNodeInDB(OrganizationNodeBase):
    id: int
    path: str
    level: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class OrganizationNode(OrganizationNodeInDB):
    children: List["OrganizationNode"] = []


# 递归引用
OrganizationNode.update_forward_refs()


# 角色相关模型
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_system_role: bool = False


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleInDB(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Role(RoleInDB):
    pass


# 权限相关模型
class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class PermissionInDB(PermissionBase):
    id: int

    class Config:
        orm_mode = True


class Permission(PermissionInDB):
    pass


# 带有层级结构的权限树节点
class PermissionNode(Permission):
    children: List["PermissionNode"] = []


PermissionNode.update_forward_refs()


# 组织权限相关模型
class RoleOrgPermissionBase(BaseModel):
    role_id: int
    org_node_id: int
    access_type: str = "view"
    include_children: bool = True


class RoleOrgPermissionCreate(RoleOrgPermissionBase):
    pass


class RoleOrgPermissionUpdate(BaseModel):
    access_type: Optional[str] = None
    include_children: Optional[bool] = None


class RoleOrgPermissionInDB(RoleOrgPermissionBase):
    id: int

    class Config:
        orm_mode = True


class RoleOrgPermission(RoleOrgPermissionInDB):
    org_node: Optional[OrganizationNode] = None


# 用于更新角色权限的请求模型
class UpdateRolePermissionsRequest(BaseModel):
    permission_ids: List[int]


class UpdateRoleOrgPermissionsRequest(BaseModel):
    org_permissions: List[RoleOrgPermissionCreate]


# 用于响应权限检查的模型
class PermissionCheckResponse(BaseModel):
    has_permission: bool


# 带有层级结构的组织树节点
class OrganizationTree(OrganizationNode):
    children: List["OrganizationTree"] = []


# 角色权限更新
class RolePermissionUpdate(BaseModel):
    permission_ids: List[int]


# 角色组织权限更新
class RoleOrgPermissionUpdate(BaseModel):
    org_node_ids: List[int] 