from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.services import sdui_service

router = APIRouter()


@router.get("/config", response_model=Dict)
def get_system_config(
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """获取系统配置"""
    # 获取当前用户可访问的系统模块和功能
    system_config = sdui_service.get_system_config(db, current_user)
    if not system_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System configuration not found"
        )
    return system_config


@router.get("/menu", response_model=List[Dict])
def get_system_menu(
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """获取系统菜单"""
    # 获取当前用户可访问的菜单
    menu = sdui_service.get_user_menu(db, current_user)
    return menu


@router.get("/info", response_model=Dict)
def get_system_info() -> Any:
    """获取系统信息"""
    return {
        "name": "SDUI System",
        "version": "1.0.0",
        "description": "Server-Driven UI System",
        "apiVersion": "v1",
    } 