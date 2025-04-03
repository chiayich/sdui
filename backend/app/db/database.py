import logging
import asyncpg
from fastapi import Depends
from typing import Optional, List, Dict, Any, Union
from databases import Database

from app.config import settings

logger = logging.getLogger(__name__)

# 创建数据库连接
database = Database(settings.DATABASE_URL)

async def startup_db():
    logger.info(f"连接数据库: {settings.DATABASE_URL}")
    if not database.is_connected:
        await database.connect()
    logger.info("数据库连接成功")

async def shutdown_db():
    logger.info("关闭数据库连接")
    if database.is_connected:
        await database.disconnect()

async def get_db():
    """获取数据库连接依赖"""
    if not database.is_connected:
        await database.connect()
    return database 