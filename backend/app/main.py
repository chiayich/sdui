from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import ui_templates, components
from .middleware.logging_middleware import LoggingMiddleware
from .routers import logs
from app.api import router as api_router
from app.database import Base, engine, init_db

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SDUI API",
    description="Server-Driven UI API for cross-platform applications",
    version="0.1.0",
    debug=settings.DEBUG  # 使用配置中的 DEBUG 设置
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，方便调试
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 应用日志中间件（放在最后添加，这样它会第一个执行）
app.add_middleware(LoggingMiddleware)

# 初始化数据库
init_db()

# 打印所有路由信息
print("\nAPI Router routes:")
for route in api_router.routes:
    print(f"- {route.methods} {route.path}")

# 路由
app.include_router(
    api_router,
    prefix="/api"  # 在主应用中设置 /api 前缀
)

# 打印所有应用路由
print("\nAll application routes:")
for route in app.routes:
    if hasattr(route, "methods") and hasattr(route, "path"):
        print(f"- {route.methods} {route.path}")

@app.get("/", tags=["Health"])
async def root():
    """API健康检查"""
    return {"status": "healthy", "version": "0.1.0"}
