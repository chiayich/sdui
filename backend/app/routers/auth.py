import logging
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from app.core.security import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..config import settings
from ..db.session import get_db
from ..models.user import User as DBUser

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由
router = APIRouter()


# 模型定义
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    class Config:
        from_attributes = True


class UserInDB(User):
    id: str
    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    logger.info(
        f"验证密码: plain_password={plain_password}, hashed_password={hashed_password}"
    )
    try:
        result = bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
        logger.info(f"验证结果: {result}")
        return result
    except Exception as e:
        logger.error(f"密码验证出错: {e}")
        return False


def get_user(db: Session, username: str) -> Optional[UserInDB]:
    """从数据库获取用户"""
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if user:
        return UserInDB(
            id=str(user.id),
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
    return None


def authenticate_user(db: Session, username: str, password: str) -> Optional[UserInDB]:
    """认证用户"""
    logger.info(f"尝试认证用户: {username}")
    user = get_user(db, username)
    if not user:
        logger.warning(f"用户不存在: {username}")
        return None
    logger.info(f"找到用户: {user.username}, 正在验证密码")
    if not verify_password(password, user.hashed_password):
        logger.warning(f"密码验证失败: {username}")
        return None
    logger.info(f"用户认证成功: {username}")
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="账户已禁用")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    """登录获取访问令牌"""
    logger.info(f"收到登录请求: username={form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"认证失败: username={form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    logger.info(f"生成访问令牌成功: username={user.username}")
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    """获取当前用户信息"""
    return current_user


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
