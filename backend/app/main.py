from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import ui, auth, components
from app.middleware.logging_middleware import LoggingMiddleware

# 配置日志
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在应用启动时执行
    logger.info("应用启动中... 连接数据库和Redis")
    logger.info(f"数据库URL: {settings.DATABASE_URL}")
    logger.info(f"Redis URL: {settings.REDIS_URL}")

    # 这里可以添加数据库和Redis连接初始化

    yield

    # 在应用关闭时执行
    logger.info("应用关闭中...")


# 创建FastAPI应用
app = FastAPI(
    title="SDUI API",
    description="服务器驱动UI API",
    version="0.1.0",
    lifespan=lifespan,
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加日志中间件
app.add_middleware(LoggingMiddleware)

# 注册路由
app.include_router(ui.router, prefix="/api/ui", tags=["UI"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(components.router, prefix="/api/components", tags=["Components"])


@app.get("/")
async def root():
    return {"message": "欢迎使用SDUI API"}
