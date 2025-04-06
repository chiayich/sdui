from typing import Optional, List
from pydantic import BaseModel, EmailStr


# 共享属性
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    organization_id: Optional[int] = None


# 用于创建用户，不包含ID和角色
class UserCreate(UserBase):
    password: str


# 用于更新用户，所有字段都是可选的
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    organization_id: Optional[int] = None


# 数据库模型对应的完整用户信息
class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


# API响应中的用户信息（不包含密码）
class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


# 用户登录请求
class UserLogin(BaseModel):
    username: str
    password: str


# 用户令牌
class Token(BaseModel):
    access_token: str
    token_type: str


# 令牌数据
class TokenPayload(BaseModel):
    sub: Optional[str] = None 