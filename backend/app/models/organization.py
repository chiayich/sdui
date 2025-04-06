from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrganizationNode(Base):
    """组织节点模型"""
    __tablename__ = "organization_nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True)
    node_type = Column(String, nullable=False)  # 节点类型：公司、部门、团队等
    parent_id = Column(Integer, ForeignKey("organization_nodes.id"), nullable=True)
    path = Column(String, nullable=False)  # 存储节点路径，如 /1/2/3/
    level = Column(Integer, nullable=False)  # 节点层级，从0开始
    
    # 关系
    children = relationship("OrganizationNode", 
                          backref="parent",
                          foreign_keys=[parent_id],
                          remote_side=[id])


class Permission(Base):
    """权限模型"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("permissions.id"), nullable=True)
    
    # 关系
    children = relationship("Permission", 
                          backref="parent",
                          foreign_keys=[parent_id],
                          remote_side=[id])


class Role(Base):
    """角色模型"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    is_system_role = Column(Boolean, default=False)  # 是否为系统内置角色
    
    # 角色-权限多对多关系通过RolePermission
    permissions = relationship("Permission", secondary="role_permissions", backref="roles")
    # 角色-组织权限多对多关系通过RoleOrgPermission
    org_permissions = relationship("OrganizationNode", secondary="role_org_permissions", backref="roles")


# 用户-角色多对多关系表
user_role = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)


class RolePermission(Base):
    """角色-权限关联模型"""
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)


class RoleOrgPermission(Base):
    """角色-组织权限关联模型"""
    __tablename__ = "role_org_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    org_node_id = Column(Integer, ForeignKey("organization_nodes.id"), primary_key=True)