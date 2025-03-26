from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import ui_templates, components
from .middleware.logging_middleware import LoggingMiddleware
from .routers import logs

app = FastAPI(
    title="SDUI API",
    description="Server-Driven UI API for cross-platform applications",
    version="0.1.0",
)

# 应用日志中间件（需要在CORS前添加）
app.add_middleware(LoggingMiddleware)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(ui_templates.router, prefix="/api", tags=["UI Templates"])
app.include_router(components.router, prefix="/api", tags=["Components"])
app.include_router(logs.router, prefix="/api", tags=["Logs"])


@app.get("/", tags=["Health"])
async def root():
    """API健康检查"""
    return {"status": "healthy", "version": "0.1.0"}
