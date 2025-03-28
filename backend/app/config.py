from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # 数据库设置
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "sdui")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "sdui_schema")

    # 支持DATABASE_URL环境变量(devcontainer中设置)
    DATABASE_URL_ENV: str = os.getenv("DATABASE_URL", "")

    # Redis设置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # 支持REDIS_URL环境变量(devcontainer中设置)
    REDIS_URL_ENV: str = os.getenv("REDIS_URL", "")

    # 安全设置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sdui_secret_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 缓存设置
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 60 * 5  # 5分钟

    # CORS设置
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # 开发环境前端
        "http://localhost:5174",  # 已映射的开发环境前端
        "http://localhost:8000",  # 开发环境API
        "http://localhost",  # 生产环境
    ]

    # 调试模式
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # 数据库连接字符串
    @property
    def DATABASE_URL(self) -> str:
        # 优先使用环境变量中设置的完整连接字符串
        if self.DATABASE_URL_ENV:
            return self.DATABASE_URL_ENV
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # 异步数据库连接字符串
    @property
    def DATABASE_URL_ASYNC(self) -> str:
        # 优先使用环境变量中设置的连接字符串，但添加异步驱动
        if self.DATABASE_URL_ENV:
            # 替换协议，确保使用异步驱动
            if self.DATABASE_URL_ENV.startswith("postgresql://"):
                return self.DATABASE_URL_ENV.replace(
                    "postgresql://", "postgresql+asyncpg://", 1
                )
            return self.DATABASE_URL_ENV
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Redis连接字符串
    @property
    def REDIS_URL(self) -> str:
        # 优先使用环境变量中设置的完整连接字符串
        if self.REDIS_URL_ENV:
            return self.REDIS_URL_ENV
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建设置实例
settings = Settings()
