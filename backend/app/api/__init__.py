from fastapi import APIRouter
from .table_data import router as table_data_router

# 创建主路由器
router = APIRouter()

# 注册子路由器
router.include_router(table_data_router)

# 打印路由信息
print("\nRegistered routes in API Router:")
for route in router.routes:
    print(f"- {route.methods} {route.path}")