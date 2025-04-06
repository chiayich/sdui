from fastapi import APIRouter

from app.api.endpoints import organization, login, users, system, sdui

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(organization.router, prefix="/organization", tags=["organization"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(sdui.router, prefix="/sdui", tags=["sdui"]) 