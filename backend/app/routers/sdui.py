from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, models
from app.api.deps import get_db, get_current_active_user
from app.services import sdui_service

router = APIRouter(prefix="/api/sdui", tags=["sdui"])


@router.get("/structure", response_model=Dict)
def get_structure(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """获取系统结构配置
    
    返回系统导航结构、全局组件等配置
    """
    system_config = sdui_service.get_system_config(db, current_user)
    if not system_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="系统配置不存在"
        )
    return system_config


@router.get("/ui/{config_code}", response_model=Dict)
def get_ui_config(
    config_code: str,
    component_ids: Optional[List[str]] = Query(None),
    include_children: bool = True,
    include_data: bool = True,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """获取UI配置
    
    返回指定配置代码的UI配置，可选择性包含子组件和数据
    """
    # 获取页面配置
    config = sdui_service.get_page_config(db, config_code, current_user)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"配置 {config_code} 不存在或无权访问"
        )
    
    # 如果指定了组件ID，只返回这些组件
    if component_ids and "components" in config:
        filtered_components = []
        for component in config["components"]:
            if component.get("id") in component_ids:
                filtered_components.append(component)
        config["components"] = filtered_components
    
    # 如果不包含子组件，则移除所有子组件
    if not include_children and "components" in config:
        for component in config["components"]:
            if "components" in component:
                del component["components"]
    
    return config


@router.get("/component/{component_code}", response_model=Dict)
def get_component_config(
    component_code: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """获取组件配置
    
    返回指定组件代码的配置
    """
    # 获取组件配置
    component_config = crud.sdui_config.get_by_code(db, code=component_code)
    if not component_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"组件配置 {component_code} 不存在"
        )
    
    # 检查权限
    if not current_user.is_superuser:
        user_permissions = sdui_service.get_user_permissions(db, current_user)
        required_permission = component_config.content.get("permission")
        if required_permission and required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此组件配置"
            )
    
    return component_config.content


@router.get("/public/{config_code}", response_model=Dict)
def get_public_ui_config(
    config_code: str,
    db: Session = Depends(get_db),
) -> Any:
    """获取公共UI配置，无需认证
    
    返回指定配置代码的UI配置，适用于登录页等公共页面
    """
    config = crud.sdui_config.get_by_code(db, code=config_code)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"公共配置 {config_code} 不存在"
        )
    
    # 检查是否为公共配置
    if not config.content.get("is_public", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此配置不允许公开访问"
        )
    
    return config.content 