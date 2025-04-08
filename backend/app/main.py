import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.api import api_router
from .config import settings
from .routers import auth, components, logs, sdui, ui, ui_templates

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在应用启动时执行
    logger.info("应用启动中...")
    yield
    # 在应用关闭时执行
    logger.info("应用关闭中...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# 设置CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 添加路由
app.include_router(api_router)  # 添加API路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(sdui.router, prefix="/api/sdui", tags=["sdui"])  # 注释掉重复的路由
app.include_router(ui.router, prefix="/api/ui", tags=["ui"])
app.include_router(components.router, prefix="/api/components", tags=["components"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])
app.include_router(ui_templates.router, prefix="/api/templates", tags=["templates"])


@app.get("/")
def root():
    return {"message": "Welcome to SDUI Backend API", "version": settings.VERSION}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
