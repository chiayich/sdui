from app.api.endpoints import login, organization, sdui, system, users
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")
api_router.include_router(login.router, prefix="/auth", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    organization.router, prefix="/organization", tags=["organization"]
)
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(sdui.router, prefix="/sdui", tags=["sdui"])
