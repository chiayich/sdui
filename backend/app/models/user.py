import uuid

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "sdui_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # 用户角色关系
    roles = relationship("Role", secondary="sdui_schema.user_roles", backref="users")

    def __repr__(self):
        return f"<User {self.username}>"
