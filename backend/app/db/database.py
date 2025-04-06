import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings

logger = logging.getLogger(__name__)

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 连接池预检测
    pool_recycle=3600,   # 一小时后回收连接
    echo=getattr(settings, "SQLALCHEMY_ECHO", False)  # 是否打印SQL语句，默认不打印
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

async def startup_db() -> None:
    """数据库启动连接"""
    logger.info(f"数据库连接URL: {settings.DATABASE_URL}")
    # 检查数据库连接
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        logger.info("数据库连接成功")
        db.close()
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        raise

async def shutdown_db() -> None:
    """关闭数据库连接"""
    logger.info("关闭数据库连接")
    # SQLAlchemy会自动管理连接池的关闭

def get_db() -> Generator[Session, None, None]:
    """数据库会话依赖项"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 