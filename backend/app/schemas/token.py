from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str  # 用户ID，使用UUID字符串
    exp: Optional[int] = None
