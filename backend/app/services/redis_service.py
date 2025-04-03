import logging
import redis.asyncio as redis
from fastapi import Depends

from app.config import settings

logger = logging.getLogger(__name__)

# 创建Redis连接池
redis_pool = None

async def startup_redis():
    """初始化Redis连接池"""
    global redis_pool
    logger.info(f"连接Redis: {settings.REDIS_URL}")
    redis_pool = redis.ConnectionPool.from_url(
        settings.REDIS_URL,
        max_connections=settings.REDIS_MAX_CONNECTIONS,
        decode_responses=True
    )
    logger.info("Redis连接池创建成功")

async def shutdown_redis():
    """关闭Redis连接池"""
    global redis_pool
    logger.info("关闭Redis连接池")
    if redis_pool:
        await redis_pool.disconnect()
    redis_pool = None

async def get_redis():
    """获取Redis连接依赖"""
    if not redis_pool:
        await startup_redis()
    
    client = redis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.close() 