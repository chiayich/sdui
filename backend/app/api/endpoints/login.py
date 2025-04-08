from datetime import timedelta
from typing import Any

from app import crud, models, schemas
from app.api import deps
from app.config import settings
from app.core import security
from app.core.security import get_password_hash
from app.crud.crud_user import user as crud_user
from app.db.session import get_db
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="用户未激活")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            str(user.id), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取当前用户信息"""
    return current_user


@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="该邮箱对应的用户不存在",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=str(user.email), email=email, token=password_reset_token
    )
    return {"msg": "密码重置邮件已发送"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="无效的令牌")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="该邮箱对应的用户不存在",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="用户未激活")

    # 使用CRUD方法更新密码
    user_in = {"password": new_password}
    crud.user.update(db, db_obj=user, obj_in=user_in)
    return {"msg": "密码更新成功"}
