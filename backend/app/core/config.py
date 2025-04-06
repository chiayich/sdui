import secrets
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "SDUI API"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    
    # CORS 配置
    CORS_ORIGINS: List[str] = ["*"]
    
    # 数据库配置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "huajin"  # 本地用户名
    POSTGRES_PASSWORD: str = ""     # 本地密码(如果需要)
    POSTGRES_DB: str = "sdui"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # 环境变量中已存在的数据库配置
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_SCHEMA: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        # 优先使用环境变量中的DB_*配置
        if values.get("DB_HOST") and values.get("DB_NAME"):
            db_user = values.get("DB_USER", "")
            db_pass = values.get("DB_PASSWORD", "")
            db_host = values.get("DB_HOST", "")
            db_port = values.get("DB_PORT", "5432")
            db_name = values.get("DB_NAME", "")
            
            if db_user and db_pass:
                return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
            elif db_user:
                return f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"
            else:
                return f"postgresql://{db_host}:{db_port}/{db_name}"
        
        # 否则使用POSTGRES_*配置
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("POSTGRES_SERVER")
        db = values.get("POSTGRES_DB", "")
        
        if password:
            return f"postgresql://{user}:{password}@{host}/{db}"
        else:
            return f"postgresql://{user}@{host}/{db}"

    # 超级管理员配置
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略额外的字段


settings = Settings() 