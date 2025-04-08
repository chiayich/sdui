from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 重新导出数据库会话和基类，避免重复定义
# 这个文件保留是为了保持向后兼容性，新代码应直接导入database.py 