import uuid

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class OrganizationNode(Base):
    """组织节点模型"""

    __tablename__ = "organization_nodes"
    __table_args__ = {"schema": "sdui_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    node_type = Column(String, nullable=False)  # 节点类型：公司、部门、团队等
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sdui_schema.organization_nodes.id"),
        nullable=True,
    )
    path = Column(String, nullable=False)  # 存储节点路径，如 /1/2/3/
    level = Column(Integer, nullable=False)  # 节点层级，从0开始

    # 关系
    children = relationship(
        "OrganizationNode", backref="parent", foreign_keys=[parent_id], remote_side=[id]
    )

    def __repr__(self):
        return f"<OrganizationNode {self.name}>"


class Permission(Base):
    """权限模型"""

    __tablename__ = "permissions"
    __table_args__ = {"schema": "sdui_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(
        UUID(as_uuid=True), ForeignKey("sdui_schema.permissions.id"), nullable=True
    )

    # 关系
    children = relationship(
        "Permission", backref="parent", foreign_keys=[parent_id], remote_side=[id]
    )

    def __repr__(self):
        return f"<Permission {self.name}>"


class Role(Base):
    """角色模型"""

    __tablename__ = "roles"
    __table_args__ = {"schema": "sdui_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_system_role = Column(Boolean, default=False)  # 是否为系统内置角色

    # 角色-权限多对多关系通过RolePermission
    permissions = relationship(
        "Permission", secondary="sdui_schema.role_permissions", backref="roles"
    )
    # 角色-组织权限多对多关系通过RoleOrgPermission
    org_permissions = relationship(
        "OrganizationNode",
        secondary="sdui_schema.role_org_permissions",
        backref="roles",
    )

    def __repr__(self):
        return f"<Role {self.name}>"


# 用户-角色多对多关系表
user_role = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("sdui_schema.users.id"),
        primary_key=True,
    ),
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("sdui_schema.roles.id"),
        primary_key=True,
    ),
    schema="sdui_schema",
)


class RolePermission(Base):
    """角色-权限关联模型"""

    __tablename__ = "role_permissions"
    __table_args__ = {"schema": "sdui_schema"}

    role_id = Column(
        UUID(as_uuid=True), ForeignKey("sdui_schema.roles.id"), primary_key=True
    )
    permission_id = Column(
        UUID(as_uuid=True), ForeignKey("sdui_schema.permissions.id"), primary_key=True
    )


class RoleOrgPermission(Base):
    """角色-组织权限关联模型"""

    __tablename__ = "role_org_permissions"
    __table_args__ = {"schema": "sdui_schema"}

    role_id = Column(
        UUID(as_uuid=True), ForeignKey("sdui_schema.roles.id"), primary_key=True
    )
    org_node_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sdui_schema.organization_nodes.id"),
        primary_key=True,
    )
