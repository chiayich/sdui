import os
import secrets
from typing import List, Optional
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""
    
    # 环境设置
    DEBUG: bool = True
    ENV: str = "development"
    
    # 应用设置
    PROJECT_NAME: str = "SDUI Backend"
    VERSION: str = "0.1.0"
    SECRET_KEY: str = "your-super-secret-key-sdui-backend-2024"  # 固定密钥
    SERVER_NAME: str = "SDUI API"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    
    # Token设置
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"  # JWT加密算法
    
    # CORS设置
    CORS_ORIGINS: List[str] = ["*"]
    
    # 数据库设置
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "huajin"
    DB_PASSWORD: str = ""
    DB_NAME: str = "sdui"
    DB_SCHEMA: str = "sdui_schema"
    SQLALCHEMY_ECHO: bool = False
    
    # Redis设置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = 10
    
    # 缓存设置
    USE_REDIS_CACHE: bool = True
    REDIS_CACHE_TTL: int = 3600  # 默认1小时
    
    # 数据库功能设置
    USE_DB_FUNCTION: bool = True
    
    # 超级管理员配置
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    USERS_OPEN_REGISTRATION: bool = False
    
    @property
    def DATABASE_URL(self) -> str:
        """获取数据库连接URL（包含schema设置）"""
        auth = f"{self.DB_USER}{':' + self.DB_PASSWORD if self.DB_PASSWORD else ''}"
        return f"postgresql://{auth}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?options=-c%20search_path%3D{self.DB_SCHEMA}"
    
    @property
    def REDIS_URL(self) -> str:
        """获取Redis连接URL"""
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Pydantic v2配置
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"  # 忽略额外的字段
    ) 