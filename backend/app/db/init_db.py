import logging
from sqlalchemy.orm import Session
import os
import pathlib
from app.core.config import settings
from app.models import User, Permission, Role, RolePermission
from app.schemas.user import UserCreate
from app.crud.crud_user import CRUDUser
from app.crud.base import CRUDBase
from app.core.security import get_password_hash
from sqlalchemy import create_engine, text
import importlib.resources as pkg_resources

from app import crud, schemas
from app.db import base  # noqa: F401
from app.models.organization import OrganizationNode
from app.db.migrate_sdui_configs import migrate_default_configs


logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """初始化数据库，创建超级管理员用户和默认权限"""
    
    # 创建初始超级管理员
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            username="admin",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        logger.info(f"初始化超级管理员用户: {user.username}")
    
    # 创建系统角色
    admin_role = crud.role.get_by_name(db, name="系统管理员")
    if not admin_role:
        role_in = schemas.RoleCreate(
            name="系统管理员",
            description="具有所有系统权限的角色",
            is_system_role=True
        )
        admin_role = crud.role.create(db, obj_in=role_in)
        logger.info(f"初始化系统管理员角色: {admin_role.name}")
    
    # 给超级管理员分配系统管理员角色
    if admin_role not in user.roles:
        crud.user.add_roles(db, user_id=user.id, role_ids=[admin_role.id])
        logger.info(f"给用户 {user.username} 分配了 {admin_role.name} 角色")
    
    # 创建基础权限
    base_permissions = [
        {"code": "system:config:view", "name": "查看系统配置"},
        {"code": "system:config:edit", "name": "编辑系统配置"},
        {"code": "user:view", "name": "查看用户信息"},
        {"code": "user:create", "name": "创建用户"},
        {"code": "user:edit", "name": "编辑用户信息"},
        {"code": "user:delete", "name": "删除用户"},
        {"code": "role:view", "name": "查看角色"},
        {"code": "role:create", "name": "创建角色"},
        {"code": "role:edit", "name": "编辑角色"},
        {"code": "role:delete", "name": "删除角色"},
        {"code": "permission:view", "name": "查看权限"},
        {"code": "permission:assign", "name": "分配权限"},
        {"code": "org:view", "name": "查看组织结构"},
        {"code": "org:create", "name": "创建组织节点"},
        {"code": "org:edit", "name": "编辑组织节点"},
        {"code": "org:delete", "name": "删除组织节点"},
    ]
    
    permission_ids = []
    for perm_data in base_permissions:
        perm = crud.permission.get_by_code(db, code=perm_data["code"])
        if not perm:
            perm_in = schemas.PermissionCreate(
                code=perm_data["code"],
                name=perm_data["name"],
                description=perm_data.get("description", "")
            )
            perm = crud.permission.create(db, obj_in=perm_in)
            logger.info(f"初始化权限: {perm.name}")
        permission_ids.append(perm.id)
    
    # 给系统管理员角色分配所有权限
    if permission_ids:
        crud.role.update_permissions(db, role_id=admin_role.id, permission_ids=permission_ids)
        logger.info(f"给角色 {admin_role.name} 分配了所有基础权限")
    
    # 创建根组织节点
    root_node = db.query(OrganizationNode).filter(
        OrganizationNode.code == "root",
        OrganizationNode.parent_id.is_(None)
    ).first()
    
    if not root_node:
        org_in = schemas.OrganizationNodeCreate(
            name="根组织",
            code="root",
            node_type="company"
        )
        root_node = crud.organization_node.create_with_path(db, obj_in=org_in)
        logger.info(f"初始化根组织节点: {root_node.name}")
    
    # 初始化SDUI配置
    init_sdui_config(db)

    # 同时初始化标准结构配置
    init_structure_config(db)

    # 初始化首页配置
    init_home_config(db)

    # 初始化数据配置
    init_data_config(db)

    # 将默认SDUI配置迁移到数据库
    migrate_default_configs(db)

    # 运行初始化SQL文件
    engine = db.bind
    sql_dir = pathlib.Path(__file__).parent.parent.parent.parent / "sqls"
    
    if sql_dir.exists():
        for sql_file in sorted(sql_dir.glob("*.sql")):
            print(f"Executing SQL file: {sql_file}")
            with open(sql_file, "r") as f:
                sql = f.read()
                try:
                    with engine.connect() as conn:
                        conn.execute(text(sql))
                        conn.commit()
                    print(f"Successfully executed SQL file: {sql_file}")
                except Exception as e:
                    print(f"Error executing SQL file {sql_file}: {e}")


def init_home_config(db: Session) -> None:
    """初始化首页SDUI配置"""
    # 检查是否已存在首页配置
    home_config = crud.sdui_config.get_by_code(db, code="home")
    if not home_config:
        # 创建首页配置，使用商品流通示例配置
        home_config_data = {
            "type": "page",
            "pageKey": "instruction",
            "version": "1.0",
            "title": "流通指令",
            "layout": {
                "type": "admin",
                "header": {
                    "title": "商品通",
                    "logo": "/static/logos/logo.png",
                    "userInfo": {
                        "name": "baosheng",
                        "role": "超级管理员"
                    },
                    "style": {
                        "background": "#001529",
                        "color": "#fff",
                        "padding": "0 24px",
                        "height": "48px",
                        "boxShadow": "0 1px 4px rgba(0,21,41,.08)"
                    }
                },
                "sider": {
                    "width": 200,
                    "theme": "dark",
                    "menu": [
                        {
                            "key": "flow",
                            "icon": "shopping-cart",
                            "title": "商品流通",
                            "children": [
                                {
                                    "key": "workbench",
                                    "title": "商品流通工作台",
                                    "route": "/flow/workbench"
                                },
                                {
                                    "key": "collection",
                                    "title": "集货",
                                    "route": "/flow/collection"
                                },
                                {
                                    "key": "instruction",
                                    "title": "流通指令",
                                    "route": "/flow/instruction",
                                    "active": True
                                },
                                {
                                    "key": "simulation",
                                    "title": "仿真评估",
                                    "route": "/flow/simulation"
                                },
                                {
                                    "key": "overview",
                                    "title": "门店概览",
                                    "route": "/flow/overview"
                                }
                            ]
                        },
                        {
                            "key": "system",
                            "icon": "setting",
                            "title": "系统管理",
                            "children": [
                                {
                                    "key": "user",
                                    "title": "用户管理",
                                    "route": "/system/user"
                                },
                                {
                                    "key": "role",
                                    "title": "角色管理",
                                    "route": "/system/role"
                                },
                                {
                                    "key": "permission",
                                    "title": "权限管理",
                                    "route": "/system/permission"
                                },
                                {
                                    "key": "organization",
                                    "title": "组织管理",
                                    "route": "/system/organization"
                                }
                            ]
                        }
                    ]
                }
            },
            "content": [
                {
                    "type": "filterBar",
                    "id": "mainFilter",
                    "props": {
                        "items": [
                            {
                                "type": "select",
                                "id": "flowType",
                                "props": {
                                    "placeholder": "宝胜阿迪达斯-调出方视角",
                                    "style": { "width": "200px" },
                                    "options": [
                                        { "value": "option1", "label": "宝胜阿迪达斯-调出方视角-调出方排序" },
                                        { "value": "option2", "label": "竖版导出模板" },
                                        { "value": "option3", "label": "宝胜阿迪达斯-调出方主视角" },
                                        { "value": "option4", "label": "宝胜阿迪达斯-调入方主视角" },
                                        { "value": "option5", "label": "系统默认配置" }
                                    ],
                                    "defaultValue": "option1"
                                }
                            },
                            {
                                "type": "datePicker",
                                "id": "flowDate",
                                "props": {
                                    "placeholder": "请选择日期",
                                    "value": "2025-04-03",
                                    "style": { "width": "150px" }
                                },
                                "bindings": {
                                    "value": {
                                        "type": "state",
                                        "source": "searchForm.flowDate"
                                    }
                                }
                            },
                            {
                                "type": "select",
                                "id": "bizType",
                                "props": {
                                    "placeholder": "业务动作类型",
                                    "style": { "width": "150px" },
                                    "options": [
                                        { "value": "daily", "label": "日常补货" },
                                        { "value": "rolling", "label": "滚动铺货" },
                                        { "value": "expansion", "label": "扩铺" },
                                        { "value": "collection", "label": "集货" },
                                        { "value": "reorder", "label": "翻单" },
                                        { "value": "storeChange", "label": "换店" },
                                        { "value": "return", "label": "返仓" }
                                    ]
                                }
                            }
                        ],
                        "actions": [
                            {
                                "type": "button",
                                "id": "searchBtn",
                                "text": "查询",
                                "props": {
                                    "type": "primary"
                                }
                            },
                            {
                                "type": "button",
                                "id": "resetBtn",
                                "text": "重置"
                            }
                        ]
                    }
                },
                {
                    "type": "table",
                    "id": "flowTable",
                    "props": {
                        "columns": [
                            {
                                "title": "",
                                "dataIndex": "select",
                                "width": 40,
                                "align": "center"
                            },
                            {
                                "title": "行号",
                                "dataIndex": "lineNo",
                                "width": 60,
                                "align": "center"
                            },
                            {
                                "title": "业务动作",
                                "dataIndex": "bizAction",
                                "width": 100
                            },
                            {
                                "title": "调出区域",
                                "dataIndex": "outRegion",
                                "width": 100
                            },
                            {
                                "title": "调出方",
                                "dataIndex": "outStore",
                                "width": 200
                            }
                        ],
                        "dataSource": [
                            {
                                "key": "1",
                                "lineNo": 1,
                                "bizAction": "日常补货",
                                "outRegion": "浙江区部",
                                "outStore": "宝胜金华通道中心仓"
                            },
                            {
                                "key": "2",
                                "lineNo": 2,
                                "bizAction": "日常补货",
                                "outRegion": "浙江区部",
                                "outStore": "宝胜金华通道北仓"
                            }
                        ],
                        "pagination": {
                            "pageSize": 10,
                            "showTotal": True
                        },
                        "style": {
                            "background": "#fff"
                        }
                    }
                }
            ],
            "state": {
                "currentMenu": {
                    "type": "string",
                    "default": "instruction"
                },
                "flowType": {
                    "type": "string",
                    "default": ""
                },
                "flowDate": {
                    "type": "string",
                    "default": "2025-04-03"
                },
                "bizType": {
                    "type": "string",
                    "default": ""
                }
            }
        }
        
        sdui_config_in = schemas.SDUIConfigCreate(
            code="home",
            name="系统首页",
            config_type="page",
            content=home_config_data
        )
        home_config = crud.sdui_config.create(db, obj_in=sdui_config_in)
        logger.info("初始化首页SDUI配置")


def init_sdui_config(db: Session) -> None:
    """初始化系统结构SDUI配置"""
    # 系统结构配置
    system_structure = crud.sdui_config.get_by_code(db, code="system-structure")
    if not system_structure:
        system_structure_data = {
            "navigation": {
                "type": "sider",
                "logo": "/static/logos/logo.png",
                "title": "SDUI系统",
                "items": [
                    {
                        "key": "dashboard",
                        "label": "仪表盘",
                        "icon": "dashboard",
                        "route": "/dashboard"
                    },
                    {
                        "key": "flow",
                        "label": "商品流通",
                        "icon": "shopping-cart",
                        "items": [
                            {
                                "key": "workbench",
                                "label": "商品流通工作台",
                                "route": "/flow/workbench"
                            },
                            {
                                "key": "collection",
                                "label": "集货",
                                "route": "/flow/collection"
                            },
                            {
                                "key": "instruction",
                                "label": "流通指令",
                                "route": "/flow/instruction"
                            },
                            {
                                "key": "simulation",
                                "label": "仿真评估",
                                "route": "/flow/simulation"
                            },
                            {
                                "key": "overview",
                                "label": "门店概览",
                                "route": "/flow/overview"
                            }
                        ]
                    },
                    {
                        "key": "system",
                        "label": "系统管理",
                        "icon": "setting",
                        "items": [
                            {
                                "key": "user",
                                "label": "用户管理",
                                "route": "/system/user"
                            },
                            {
                                "key": "role",
                                "label": "角色管理",
                                "route": "/system/role"
                            },
                            {
                                "key": "permission",
                                "label": "权限管理",
                                "route": "/system/permission"
                            },
                            {
                                "key": "organization",
                                "label": "组织管理",
                                "route": "/system/organization"
                            }
                        ]
                    }
                ]
            },
            "header": {
                "type": "header",
                "userMenu": {
                    "type": "dropdown",
                    "items": [
                        {
                            "key": "profile",
                            "label": "个人资料",
                            "route": "/profile"
                        },
                        {
                            "key": "settings",
                            "label": "设置",
                            "route": "/settings"
                        },
                        {
                            "key": "logout",
                            "label": "退出登录",
                            "action": "logout"
                        }
                    ]
                }
            }
        }
        
        sdui_config_in = schemas.SDUIConfigCreate(
            code="system-structure",
            name="系统结构配置",
            config_type="structure",
            content=system_structure_data
        )
        system_structure = crud.sdui_config.create(db, obj_in=sdui_config_in)
        logger.info("初始化系统结构SDUI配置") 


def init_structure_config(db: Session) -> None:
    """初始化系统结构SDUI配置，如果不存在则创建"""
    # 检查是否已存在结构配置
    structure_config = crud.sdui_config.get_by_code(db, code="structure")
    if not structure_config:
        # 创建系统结构配置
        structure_data = {
            "navigation": {
                "type": "sider",
                "logo": "/static/logos/logo.png",
                "title": "SDUI系统",
                "items": [
                    {
                        "key": "dashboard",
                        "label": "仪表盘",
                        "icon": "dashboard",
                        "route": "/dashboard"
                    },
                    {
                        "key": "flow",
                        "label": "商品流通",
                        "icon": "shopping-cart",
                        "items": [
                            {
                                "key": "workbench",
                                "label": "商品流通工作台",
                                "route": "/flow/workbench"
                            },
                            {
                                "key": "collection",
                                "label": "集货",
                                "route": "/flow/collection"
                            },
                            {
                                "key": "instruction",
                                "label": "流通指令",
                                "route": "/flow/instruction"
                            },
                            {
                                "key": "simulation",
                                "label": "仿真评估",
                                "route": "/flow/simulation"
                            },
                            {
                                "key": "overview",
                                "label": "门店概览",
                                "route": "/flow/overview"
                            }
                        ]
                    },
                    {
                        "key": "system",
                        "label": "系统管理",
                        "icon": "setting",
                        "items": [
                            {
                                "key": "user",
                                "label": "用户管理",
                                "route": "/system/user"
                            },
                            {
                                "key": "role",
                                "label": "角色管理",
                                "route": "/system/role"
                            },
                            {
                                "key": "permission",
                                "label": "权限管理",
                                "route": "/system/permission"
                            },
                            {
                                "key": "organization",
                                "label": "组织管理",
                                "route": "/system/organization"
                            }
                        ]
                    }
                ]
            },
            "header": {
                "type": "header",
                "userMenu": {
                    "type": "dropdown",
                    "items": [
                        {
                            "key": "profile",
                            "label": "个人资料",
                            "route": "/profile"
                        },
                        {
                            "key": "settings",
                            "label": "设置",
                            "route": "/settings"
                        },
                        {
                            "key": "logout",
                            "label": "退出登录",
                            "action": "logout"
                        }
                    ]
                }
            },
            "global_components": []
        }
        
        sdui_config_in = schemas.SDUIConfigCreate(
            code="structure",
            name="系统结构配置",
            config_type="structure",
            content=structure_data
        )
        structure_config = crud.sdui_config.create(db, obj_in=sdui_config_in)
        logger.info("初始化系统结构SDUI配置") 


def init_data_config(db: Session) -> None:
    """初始化数据配置，提供前端组件需要的数据源"""
    
    # 检查是否已存在门店数据配置
    stores_config = crud.sdui_config.get_by_code(db, code="data/stores")
    if not stores_config:
        # 创建门店数据配置
        stores_data = [
            { "value": "store1", "label": "宝胜金华通道中心仓" },
            { "value": "store2", "label": "宝胜金华通道北仓" },
            { "value": "store3", "label": "宝胜杭州西湖店" },
            { "value": "store4", "label": "宝胜上海静安店" }
        ]
        
        sdui_config_in = schemas.SDUIConfigCreate(
            code="data/stores",
            name="门店列表数据",
            config_type="data",
            content={"content": stores_data}
        )
        stores_config = crud.sdui_config.create(db, obj_in=sdui_config_in)
        logger.info("初始化门店列表数据配置")
    
    # 检查是否已存在最近订单数据配置
    orders_config = crud.sdui_config.get_by_code(db, code="data/recent-orders")
    if not orders_config:
        # 创建最近订单数据配置
        orders_data = [
            {
                "orderNo": "DD2024030100001",
                "status": "待处理",
                "store": "宝胜金华通道中心仓",
                "createTime": "2024-03-01 10:23:45",
                "amount": 4150.00
            },
            {
                "orderNo": "DD2024030100002",
                "status": "处理中",
                "store": "宝胜金华通道北仓",
                "createTime": "2024-03-01 09:15:22",
                "amount": 3280.50
            },
            {
                "orderNo": "DD2024030100003",
                "status": "已完成",
                "store": "宝胜杭州西湖店",
                "createTime": "2024-02-29 15:45:10",
                "amount": 6430.00
            },
            {
                "orderNo": "DD2024030100004",
                "status": "已完成",
                "store": "宝胜上海静安店",
                "createTime": "2024-02-28 14:22:33",
                "amount": 5120.75
            }
        ]
        
        sdui_config_in = schemas.SDUIConfigCreate(
            code="data/recent-orders",
            name="最近订单数据",
            config_type="data",
            content={"content": orders_data}
        )
        orders_config = crud.sdui_config.create(db, obj_in=sdui_config_in)
        logger.info("初始化最近订单数据配置") 