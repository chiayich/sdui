from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """通过邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """通过用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """创建新用户，包含密码哈希处理"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
            organization_id=obj_in.organization_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """更新用户信息，处理密码哈希"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        # 如果有密码需要更新，则处理哈希
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        """认证用户"""
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """检查用户是否激活"""
        return user.is_active
    
    def is_superuser(self, user: User) -> bool:
        """检查用户是否是超级管理员"""
        return user.is_superuser
    
    def add_roles(self, db: Session, *, user_id: int, role_ids: List[int]) -> User:
        """为用户添加角色"""
        user = self.get(db, id=user_id)
        if not user:
            return None
        
        # 获取角色对象
        from app.models.organization import Role
        roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
        
        # 添加到用户的角色中
        user.roles.extend(roles)
        db.commit()
        db.refresh(user)
        return user
    
    def remove_roles(self, db: Session, *, user_id: int, role_ids: List[int]) -> User:
        """移除用户的角色"""
        user = self.get(db, id=user_id)
        if not user:
            return None
        
        # 过滤掉要移除的角色
        user.roles = [role for role in user.roles if role.id not in role_ids]
        db.commit()
        db.refresh(user)
        return user


user = CRUDUser(User) 