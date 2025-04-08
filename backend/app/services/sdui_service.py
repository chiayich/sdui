from typing import Any, Dict, List, Optional

from app import crud
from app.crud import organization_node, permission, role
from app.models.user import User
from sqlalchemy.orm import Session

# 原固定配置数据已移除，改为从数据库获取


def get_system_page_config(db: Session, current_user: User) -> Dict[str, Any]:
    """
    生成系统管理主页的UI配置
    """
    # 检查权限
    has_org_permission = _check_user_permission(db, current_user, "organization:view")
    has_role_permission = _check_user_permission(db, current_user, "role:view")
    has_user_permission = _check_user_permission(db, current_user, "user:view")
    has_config_permission = _check_user_permission(db, current_user, "config:view")

    # 生成基础统计数据
    user_count = db.query(User).count()
    roles_count = db.query(crud.role.model).count()
    org_nodes_count = db.query(crud.organization_node.model).count()

    # 动态构建SDUI配置
    return {
        "type": "page",
        "id": "systemManagementPage",
        "title": "系统管理",
        "content": [
            {
                "type": "container",
                "children": [
                    {"type": "title", "level": 2, "content": "系统管理"},
                    {
                        "type": "row",
                        "gutter": 24,
                        "children": [
                            # 组织管理卡片
                            {
                                "type": "col",
                                "span": {"xs": 24, "sm": 12, "md": 8, "lg": 6},
                                "visible": has_org_permission,
                                "children": [
                                    {
                                        "type": "card",
                                        "hoverable": True,
                                        "className": "system-card",
                                        "events": {
                                            "click": {
                                                "type": "navigate",
                                                "target": "/system/organization",
                                            }
                                        },
                                        "children": [
                                            {
                                                "type": "flex",
                                                "alignItems": "center",
                                                "children": [
                                                    {
                                                        "type": "icon",
                                                        "name": "Apartment",
                                                        "className": "card-icon",
                                                    },
                                                    {
                                                        "type": "container",
                                                        "children": [
                                                            {
                                                                "type": "text",
                                                                "content": "组织架构管理",
                                                                "level": "h3",
                                                            },
                                                            {
                                                                "type": "text",
                                                                "content": f"管理公司组织架构及部门({org_nodes_count})",
                                                                "className": "text-muted",
                                                            },
                                                        ],
                                                    },
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            },
                            # 角色管理卡片
                            {
                                "type": "col",
                                "span": {"xs": 24, "sm": 12, "md": 8, "lg": 6},
                                "visible": has_role_permission,
                                "children": [
                                    {
                                        "type": "card",
                                        "hoverable": True,
                                        "className": "system-card",
                                        "events": {
                                            "click": {
                                                "type": "navigate",
                                                "target": "/system/role",
                                            }
                                        },
                                        "children": [
                                            {
                                                "type": "flex",
                                                "alignItems": "center",
                                                "children": [
                                                    {
                                                        "type": "icon",
                                                        "name": "UserFilled",
                                                        "className": "card-icon",
                                                    },
                                                    {
                                                        "type": "container",
                                                        "children": [
                                                            {
                                                                "type": "text",
                                                                "content": "角色权限管理",
                                                                "level": "h3",
                                                            },
                                                            {
                                                                "type": "text",
                                                                "content": f"管理系统角色及权限设置({roles_count})",
                                                                "className": "text-muted",
                                                            },
                                                        ],
                                                    },
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            },
                            # 用户管理卡片
                            {
                                "type": "col",
                                "span": {"xs": 24, "sm": 12, "md": 8, "lg": 6},
                                "visible": has_user_permission,
                                "children": [
                                    {
                                        "type": "card",
                                        "hoverable": True,
                                        "className": "system-card",
                                        "events": {
                                            "click": {
                                                "type": "navigate",
                                                "target": "/system/user",
                                            }
                                        },
                                        "children": [
                                            {
                                                "type": "flex",
                                                "alignItems": "center",
                                                "children": [
                                                    {
                                                        "type": "icon",
                                                        "name": "User",
                                                        "className": "card-icon",
                                                    },
                                                    {
                                                        "type": "container",
                                                        "children": [
                                                            {
                                                                "type": "text",
                                                                "content": "用户管理",
                                                                "level": "h3",
                                                            },
                                                            {
                                                                "type": "text",
                                                                "content": f"管理系统用户及账号权限({user_count})",
                                                                "className": "text-muted",
                                                            },
                                                        ],
                                                    },
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            },
                            # 系统配置卡片
                            {
                                "type": "col",
                                "span": {"xs": 24, "sm": 12, "md": 8, "lg": 6},
                                "visible": has_config_permission,
                                "children": [
                                    {
                                        "type": "card",
                                        "hoverable": True,
                                        "className": "system-card",
                                        "events": {
                                            "click": {
                                                "type": "navigate",
                                                "target": "/system/config",
                                            }
                                        },
                                        "children": [
                                            {
                                                "type": "flex",
                                                "alignItems": "center",
                                                "children": [
                                                    {
                                                        "type": "icon",
                                                        "name": "Setting",
                                                        "className": "card-icon",
                                                    },
                                                    {
                                                        "type": "container",
                                                        "children": [
                                                            {
                                                                "type": "text",
                                                                "content": "系统配置",
                                                                "level": "h3",
                                                            },
                                                            {
                                                                "type": "text",
                                                                "content": "管理系统基础配置项",
                                                                "className": "text-muted",
                                                            },
                                                        ],
                                                    },
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            },
                        ],
                    },
                ],
            }
        ],
        "styles": {
            ".system-card": {
                "height": "130px",
                "cursor": "pointer",
                "transition": "all 0.3s",
            },
            ".system-card:hover": {
                "transform": "translateY(-5px)",
                "boxShadow": "0 2px 12px 0 rgba(0, 0, 0, 0.1)",
            },
            ".card-icon": {"fontSize": "36px", "padding": "20px", "color": "#409eff"},
            ".text-muted": {"color": "#909399", "fontSize": "14px"},
        },
    }


def _check_user_permission(db: Session, user: User, permission_code: str) -> bool:
    """
    检查用户是否拥有特定权限
    """
    # 超级用户拥有所有权限
    if user.is_superuser:
        return True

    # 获取用户角色
    user_roles = crud.role.get_user_roles(db, user_id=user.id)
    if not user_roles:
        return False

    # 检查每个角色是否有该权限
    for role in user_roles:
        perms = crud.role.get_role_permissions(db, role_id=role.id)
        for perm in perms:
            if perm.code == permission_code:
                return True

    return False


def get_system_config(db: Session, user: User) -> Dict:
    """获取系统配置

    基于用户权限获取系统配置，包括导航菜单、全局组件等
    """
    # 获取系统结构配置
    system_structure = crud.sdui_config.get_by_code(db, code="system-structure")
    if not system_structure:
        return {}

    # 获取系统配置内容
    config = system_structure.content

    # 如果用户不是超级管理员，则过滤菜单项
    if not user.is_superuser:
        # 获取用户的所有角色
        user_roles = user.roles
        if not user_roles:
            return filter_config_by_permissions(config, [])

        # 获取所有角色的权限
        permissions = []
        for role in user_roles:
            role_permissions = crud.role.get_role_permissions(db, role_id=role.id)
            permissions.extend([p.code for p in role_permissions])

        # 根据权限过滤菜单
        config = filter_config_by_permissions(config, permissions)

    return config


def get_ui_config(db: Session, code: str, user: User = None) -> Optional[Dict]:
    """
    获取UI配置
    """
    # 从数据库获取配置
    config = crud.sdui_config.get_by_code(db=db, code=code)
    if not config:
        return None

    # 返回配置数据
    return config.config_data


def filter_config_by_permissions(config: Dict, permissions: List[str]) -> Dict:
    """根据权限过滤配置"""
    filtered_config = config.copy()

    # 过滤导航菜单
    if "navigation" in filtered_config and "menuItems" in filtered_config["navigation"]:
        filtered_config["navigation"]["menuItems"] = filter_menu_items(
            filtered_config["navigation"]["menuItems"], permissions
        )

    return filtered_config


def filter_menu_items(menu_items: List[Dict], permissions: List[str]) -> List[Dict]:
    """根据权限过滤菜单项"""
    filtered_items = []

    for item in menu_items:
        # 判断是否有权限访问此菜单
        required_permission = item.get("permission")

        # 如果没有指定权限要求，或者用户有对应权限，则保留此菜单
        if not required_permission or required_permission in permissions:
            # 处理子菜单
            if "children" in item and item["children"]:
                filtered_children = filter_menu_items(item["children"], permissions)
                # 只有当有可访问的子菜单时，才保留父菜单
                if filtered_children:
                    item_copy = item.copy()
                    item_copy["children"] = filtered_children
                    filtered_items.append(item_copy)
            else:
                filtered_items.append(item.copy())

    return filtered_items


def get_user_menu(db: Session, user: User) -> List[Dict]:
    """获取用户菜单"""
    system_config = get_system_config(db, user)

    if not system_config or "navigation" not in system_config:
        return []

    return system_config["navigation"].get("menuItems", [])


def get_page_config(db: Session, code: str, user: User) -> Optional[Dict]:
    """获取页面配置"""
    # 使用统一的UI配置获取函数
    config = get_ui_config(db, code, user)
    if not config:
        return None

    # 如果不是超级管理员，需要检查权限
    if not user.is_superuser:
        # 获取用户所有权限
        user_permissions = get_user_permissions(db, user)

        # 检查页面是否需要特定权限
        required_permission = config.get("permission")
        if required_permission and required_permission not in user_permissions:
            return None

        # 过滤页面组件
        if "components" in config:
            config["components"] = filter_components_by_permissions(
                config["components"], user_permissions
            )

    return config


def filter_components_by_permissions(
    components: List[Dict], permissions: List[str]
) -> List[Dict]:
    """根据权限过滤组件"""
    filtered_components = []

    for component in components:
        # 检查组件权限
        required_permission = component.get("permission")

        if not required_permission or required_permission in permissions:
            component_copy = component.copy()

            # 处理子组件
            if "components" in component and component["components"]:
                component_copy["components"] = filter_components_by_permissions(
                    component["components"], permissions
                )

            filtered_components.append(component_copy)

    return filtered_components


def get_user_permissions(db: Session, user: User) -> List[str]:
    """获取用户所有权限"""
    if user.is_superuser:
        # 超级管理员拥有所有权限
        all_permissions = crud.permission.get_multi(db)
        return [p.code for p in all_permissions]

    # 获取用户的所有角色
    user_roles = user.roles
    if not user_roles:
        return []

    # 汇总所有角色的权限
    permissions = []
    for role in user_roles:
        role_permissions = crud.role.get_role_permissions(db, role_id=role.id)
        permissions.extend([p.code for p in role_permissions])

    # 去重
    return list(set(permissions))
