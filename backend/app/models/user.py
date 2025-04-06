from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    
    organization_id = Column(Integer, ForeignKey("organization_nodes.id"), nullable=True)
    organization = relationship("OrganizationNode", backref="users")
    
    # 用户角色关系
    roles = relationship("Role", secondary="user_roles", backref="users")
    
    def __repr__(self):
        return f"<User {self.username}>" 