import logging
import uuid
from typing import Generator, Optional

from app.config import settings
from app.crud.crud_user import user as crud_user
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

# 配置日志
logger = logging.getLogger(__name__)

# OAuth2 token URL
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/access-token")


def get_db() -> Generator:
    """获取数据库会话"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """从token中获取当前用户"""
    try:
        # 记录token解析开始
        logger.debug(f"开始解析认证token")

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if not token_data.sub:
            logger.warning("Token payload 中缺少 sub 字段")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.debug(f"Token解析成功，用户ID: {token_data.sub}")

    except JWTError as e:
        logger.error(f"JWT解析错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError as e:
        logger.error(f"Token数据验证错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # token中的sub是hex格式的UUID字符串，需要先转换回UUID对象
        user_id = uuid.UUID(token_data.sub)
        user = crud_user.get(db, id=user_id)
        if not user:
            logger.warning(f"未找到ID为 {user_id} 的用户")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
            )
        logger.debug(f"成功获取用户信息: {user.username}")
        return user
    except ValueError as e:
        logger.error(f"用户ID格式错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的用户ID格式",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前活跃用户"""
    if not crud_user.is_active(current_user):
        logger.warning(f"用户 {current_user.username} 未激活")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="用户未激活")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """获取当前超级管理员用户"""
    if not crud_user.is_superuser(current_user):
        logger.warning(f"用户 {current_user.username} 尝试访问超级管理员接口")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="权限不足，需要超级管理员权限"
        )
    return current_user
