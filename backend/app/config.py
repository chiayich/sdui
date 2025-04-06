import os
from typing import List, Optional

# 根据Pydantic版本选择合适的BaseSettings导入
try:
    # Pydantic v2
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    # Pydantic v1
    from pydantic import BaseSettings
    SettingsConfigDict = dict


class Settings(BaseSettings):
    """应用配置"""
    
    # 环境设置
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    ENV: str = os.getenv("ENV", "development")
    
    # 应用设置
    APP_NAME: str = "SDUI API"
    API_PREFIX: str = "/api"
    
    # CORS设置
    CORS_ORIGINS: List[str] = ["*"]
    
    # 数据库设置
    DB_HOST: str = os.getenv("DB_HOST", "localhost")  # 修改为localhost用于本地开发
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "huajin")  # 使用当前系统用户名
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")  # 本地开发环境通常不需要密码
    DB_NAME: str = os.getenv("DB_NAME", "sdui")
    DATABASE_URL: str = f"postgresql://{DB_USER}{':' + DB_PASSWORD if DB_PASSWORD else ''}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "False").lower() in ("true", "1", "t")
    
    # Redis设置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")  # 修改为localhost用于本地开发
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_URL: str = f"redis://{':' + REDIS_PASSWORD + '@' if REDIS_PASSWORD else ''}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    REDIS_MAX_CONNECTIONS: int = int(os.getenv("REDIS_MAX_CONNECTIONS", "10"))
    
    # 缓存设置
    USE_REDIS_CACHE: bool = os.getenv("USE_REDIS_CACHE", "True").lower() in ("true", "1", "t")
    REDIS_CACHE_TTL: int = int(os.getenv("REDIS_CACHE_TTL", "3600"))  # 默认1小时
    
    # 数据库功能设置
    USE_DB_FUNCTION: bool = os.getenv("USE_DB_FUNCTION", "True").lower() in ("true", "1", "t")
    
    # 初始超级管理员
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "admin@example.com")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "admin")
    
    # Pydantic v2配置
    model_config = SettingsConfigDict(case_sensitive=True)


# 导出设置实例
settings = Settings()
