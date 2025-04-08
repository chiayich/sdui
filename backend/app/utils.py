from datetime import datetime, timedelta
from typing import Optional

import jwt
from app.config import settings
from fastapi import HTTPException, status


def generate_password_reset_token(email: str) -> str:
    """生成密码重置令牌"""
    delta = timedelta(hours=24)  # 默认24小时过期
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """验证密码重置令牌"""
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_token["sub"]
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError):
        return None


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    """发送密码重置邮件"""
    # TODO: 实现邮件发送功能
    # 目前仅打印日志
    print(f"Password reset token for {email}: {token}")
    pass
