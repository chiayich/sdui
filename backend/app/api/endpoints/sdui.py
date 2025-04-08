from typing import Any, Dict, List, Optional

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.sdui_config import (
    SDUIConfig,
    SDUIConfigCreate,
    SDUIConfigQuery,
    SDUIConfigUpdate,
    UIConfigData,
)
from app.services.sdui_service import get_ui_config
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/structure", response_model=UIConfigData)
def get_structure(
    config_type: str = None,
    theme: str = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> UIConfigData:
    """
    获取系统结构配置，包括导航和全局组件

    - config_type: 配置类型，如"default"、"mobile"等
    - theme: 主题，如"light"、"dark"等
    """
    # 构建查询条件
    filters = {"config_type": "structure"}

    # 添加配置类型过滤
    if config_type and theme:
        # 尝试查找带有类型和主题的特定配置
        specific_config = crud.sdui_config.get_by_code(
            db=db, code=f"structure-{config_type}-{theme}"
        )
        if specific_config:
            # 将 SQLAlchemy 模型转换为 Pydantic 模型
            config = SDUIConfig.from_orm(specific_config)
            return config.config_data
    elif config_type:
        # 尝试查找带有类型的配置
        specific_config = crud.sdui_config.get_by_code(
            db=db, code=f"structure-{config_type}"
        )
        if specific_config:
            # 将 SQLAlchemy 模型转换为 Pydantic 模型
            config = SDUIConfig.from_orm(specific_config)
            return config.config_data

    # 如果没有特定配置或未指定类型，则查找一般结构配置
    structure_config = crud.sdui_config.get_by_code(db=db, code="structure")

    # 如果没有找到标准结构配置，则尝试获取系统结构配置
    if not structure_config:
        system_structure_config = crud.sdui_config.get_by_code(
            db=db, code="system-structure"
        )
        if system_structure_config:
            # 将 SQLAlchemy 模型转换为 Pydantic 模型
            config = SDUIConfig.from_orm(system_structure_config)
            return config.config_data

        # 如果都找不到，则抛出异常
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="系统结构配置未找到，请先初始化系统配置",
        )

    # 将 SQLAlchemy 模型转换为 Pydantic 模型
    config = SDUIConfig.from_orm(structure_config)
    return config.config_data


@router.get("/{code}", response_model=UIConfigData)
def get_ui_config_endpoint(
    code: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> UIConfigData:
    """
    获取UI配置，根据配置代码从数据库获取最新版本的配置
    """
    # 使用服务获取配置
    config = get_ui_config(db, code, current_user)

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"UI配置 {code} 不存在"
        )

    # 将 SQLAlchemy 模型转换为 Pydantic 模型
    config = SDUIConfig.from_orm(config)
    return config.config_data


@router.get("/configs/", response_model=List[SDUIConfig])
def list_configs(
    query: SDUIConfigQuery = Depends(),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> List[SDUIConfig]:
    """
    获取SDUI配置列表，仅超级管理员可访问
    """
    if query.category:
        return crud.sdui_config.get_by_category(db=db, category=query.category)

    # 构建查询条件
    filters = {}
    if query.code:
        filters["code"] = query.code
    if query.is_active is not None:
        filters["is_active"] = query.is_active

    return crud.sdui_config.get_multi(db=db, **filters)


@router.post("/configs/", response_model=SDUIConfig)
def create_config(
    config_in: SDUIConfigCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> SDUIConfig:
    """
    创建新的SDUI配置，仅超级管理员可访问
    """
    # 检查是否已存在相同code的配置
    existing = crud.sdui_config.get_by_code(db=db, code=config_in.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"配置代码 {config_in.code} 已存在",
        )

    # 添加创建者ID
    if current_user:
        config_in.creator_id = current_user.id

    return crud.sdui_config.create(db=db, obj_in=config_in)


@router.put("/configs/{code}", response_model=SDUIConfig)
def update_config(
    code: str,
    config_in: SDUIConfigUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> SDUIConfig:
    """
    更新SDUI配置，创建新版本，仅超级管理员可访问
    """
    config = crud.sdui_config.get_by_code(db=db, code=code)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"配置 {code} 不存在"
        )

    # 更新基本信息
    update_data = {k: v for k, v in config_in.dict(exclude_unset=True).items()}

    # 添加更新者ID
    if current_user:
        update_data["updater_id"] = current_user.id

    config = crud.sdui_config.update(db=db, db_obj=config, obj_in=update_data)

    return config
