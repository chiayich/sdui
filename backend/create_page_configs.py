from app.db.session import SessionLocal
from app.models.sdui_config import SDUIConfig
from app.crud.crud_sdui_config import sdui_config
from app.schemas.sdui_config import SDUIConfigCreate
import json

def create_page_configs():
    """创建所有页面的SDUI配置"""
    db = SessionLocal()
    try:
        # 创建商品流通工作台页面
        create_or_update_config(
            db, 
            "workbench", 
            "商品流通工作台", 
            get_flow_workbench_config()
        )

        # 创建集货页面
        create_or_update_config(
            db, 
            "collection", 
            "集货", 
            get_collection_config()
        )

        # 创建流通指令页面
        create_or_update_config(
            db, 
            "instruction", 
            "流通指令", 
            get_instruction_config()
        )

        # 创建仿真评估页面
        create_or_update_config(
            db, 
            "simulation", 
            "仿真评估", 
            get_simulation_config()
        )

        # 创建门店概览页面
        create_or_update_config(
            db, 
            "overview", 
            "门店概览", 
            get_overview_config()
        )

        # 创建用户管理页面
        create_or_update_config(
            db, 
            "system.user", 
            "用户管理", 
            get_user_management_config()
        )

        # 创建角色管理页面
        create_or_update_config(
            db, 
            "system.role", 
            "角色管理", 
            get_role_management_config()
        )

        # 创建权限管理页面
        create_or_update_config(
            db, 
            "system.permission", 
            "权限管理", 
            get_permission_management_config()
        )

        # 创建组织管理页面
        create_or_update_config(
            db, 
            "system.organization", 
            "组织管理", 
            get_organization_management_config()
        )

        print("所有页面配置创建/更新完成")
    finally:
        db.close()

def create_or_update_config(db, code, name, content):
    """创建或更新配置"""
    existing = sdui_config.get_by_code(db, code=code)
    if existing:
        existing.content = content
        existing.name = name
        db.commit()
        print(f"更新页面配置: {code}")
    else:
        config_in = SDUIConfigCreate(
            code=code,
            name=name,
            config_type="page",
            content=content
        )
        sdui_config.create(db, obj_in=config_in)
        print(f"创建页面配置: {code}")

def get_flow_workbench_config():
    """获取商品流通工作台配置"""
    return {
        "type": "page",
        "id": "flowWorkbenchPage",
        "title": "商品流通工作台",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "商品流通工作台",
                    "content": {
                        "type": "text",
                        "content": "商品流通工作台页面内容"
                    }
                }
            ]
        }
    }

def get_collection_config():
    """获取集货配置"""
    return {
        "type": "page",
        "id": "collectionPage",
        "title": "集货",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "集货",
                    "content": {
                        "type": "text",
                        "content": "集货页面内容"
                    }
                }
            ]
        }
    }

def get_instruction_config():
    """获取流通指令配置"""
    return {
        "type": "page",
        "id": "instructionPage",
        "title": "流通指令",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "流通指令",
                    "content": {
                        "type": "text",
                        "content": "流通指令页面内容"
                    }
                }
            ]
        }
    }

def get_simulation_config():
    """获取仿真评估配置"""
    return {
        "type": "page",
        "id": "simulationPage",
        "title": "仿真评估",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "仿真评估",
                    "content": {
                        "type": "text",
                        "content": "仿真评估页面内容"
                    }
                }
            ]
        }
    }

def get_overview_config():
    """获取门店概览配置"""
    return {
        "type": "page",
        "id": "overviewPage",
        "title": "门店概览",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "门店概览",
                    "content": {
                        "type": "text",
                        "content": "门店概览页面内容"
                    }
                }
            ]
        }
    }

def get_user_management_config():
    """获取用户管理配置"""
    return {
        "type": "page",
        "id": "userManagementPage",
        "title": "用户管理",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "用户列表",
                    "extra": [
                        {
                            "type": "button",
                            "text": "新建用户",
                            "permission": "user:add",
                            "props": {
                                "type": "primary"
                            },
                            "events": {
                                "click": "handleAddUser"
                            }
                        }
                    ],
                    "content": {
                        "type": "table",
                        "id": "userTable",
                        "dataSource": "api://users",
                        "pagination": True,
                        "columns": [
                            {
                                "title": "用户名",
                                "dataIndex": "username"
                            },
                            {
                                "title": "邮箱",
                                "dataIndex": "email"
                            },
                            {
                                "title": "角色",
                                "dataIndex": "roles",
                                "render": {
                                    "type": "tag",
                                    "fieldName": "name"
                                }
                            },
                            {
                                "title": "状态",
                                "dataIndex": "is_active",
                                "render": {
                                    "type": "tag",
                                    "options": [
                                        {
                                            "value": True,
                                            "label": "启用",
                                            "color": "success"
                                        },
                                        {
                                            "value": False,
                                            "label": "禁用",
                                            "color": "danger"
                                        }
                                    ]
                                }
                            },
                            {
                                "title": "操作",
                                "actions": [
                                    {
                                        "type": "button",
                                        "text": "编辑",
                                        "permission": "user:edit",
                                        "props": {
                                            "type": "primary",
                                            "size": "small"
                                        },
                                        "events": {
                                            "click": "handleEditUser"
                                        }
                                    },
                                    {
                                        "type": "button",
                                        "text": "删除",
                                        "permission": "user:delete",
                                        "props": {
                                            "type": "danger",
                                            "size": "small"
                                        },
                                        "events": {
                                            "click": "handleDeleteUser"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }

def get_role_management_config():
    """获取角色管理配置"""
    return {
        "type": "page",
        "id": "roleManagementPage",
        "title": "角色权限管理",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "角色列表",
                    "extra": [
                        {
                            "type": "button",
                            "text": "新建角色",
                            "permission": "role:add",
                            "props": {
                                "type": "primary"
                            },
                            "events": {
                                "click": "handleAddRole"
                            }
                        }
                    ],
                    "content": {
                        "type": "table",
                        "id": "roleTable",
                        "dataSource": "api://roles",
                        "pagination": True,
                        "columns": [
                            {
                                "title": "角色名称",
                                "dataIndex": "name"
                            },
                            {
                                "title": "描述",
                                "dataIndex": "description"
                            },
                            {
                                "title": "创建时间",
                                "dataIndex": "created_at",
                                "format": "datetime"
                            },
                            {
                                "title": "状态",
                                "dataIndex": "is_active",
                                "render": {
                                    "type": "tag",
                                    "options": [
                                        {
                                            "value": True,
                                            "label": "启用",
                                            "color": "success"
                                        },
                                        {
                                            "value": False,
                                            "label": "禁用",
                                            "color": "danger"
                                        }
                                    ]
                                }
                            },
                            {
                                "title": "操作",
                                "actions": [
                                    {
                                        "type": "button",
                                        "text": "编辑",
                                        "permission": "role:edit",
                                        "props": {
                                            "type": "primary",
                                            "size": "small"
                                        },
                                        "events": {
                                            "click": "handleEditRole"
                                        }
                                    },
                                    {
                                        "type": "button",
                                        "text": "权限设置",
                                        "permission": "role:permission",
                                        "props": {
                                            "type": "info",
                                            "size": "small"
                                        },
                                        "events": {
                                            "click": "handleRolePermission"
                                        }
                                    },
                                    {
                                        "type": "button",
                                        "text": "数据权限",
                                        "permission": "role:permission",
                                        "props": {
                                            "type": "warning",
                                            "size": "small"
                                        },
                                        "events": {
                                            "click": "handleRoleDataPermission"
                                        }
                                    },
                                    {
                                        "type": "button",
                                        "text": "删除",
                                        "permission": "role:delete",
                                        "props": {
                                            "type": "danger",
                                            "size": "small"
                                        },
                                        "disabled": "{{record.is_system}}",
                                        "events": {
                                            "click": "handleDeleteRole"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }

def get_permission_management_config():
    """获取权限管理配置"""
    return {
        "type": "page",
        "id": "permissionManagementPage",
        "title": "权限管理",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "权限列表",
                    "content": {
                        "type": "table",
                        "id": "permissionTable",
                        "dataSource": "api://permissions",
                        "pagination": True,
                        "columns": [
                            {
                                "title": "权限编码",
                                "dataIndex": "code"
                            },
                            {
                                "title": "权限名称",
                                "dataIndex": "name"
                            },
                            {
                                "title": "描述",
                                "dataIndex": "description"
                            }
                        ]
                    }
                }
            ]
        }
    }

def get_organization_management_config():
    """获取组织管理配置"""
    return {
        "type": "page",
        "id": "organizationManagementPage",
        "title": "组织管理",
        "layout": {
            "type": "container",
            "children": [
                {
                    "type": "card",
                    "title": "组织结构",
                    "extra": [
                        {
                            "type": "button",
                            "text": "新建组织",
                            "permission": "org:add",
                            "props": {
                                "type": "primary"
                            },
                            "events": {
                                "click": "handleAddOrg"
                            }
                        }
                    ],
                    "content": {
                        "type": "tree",
                        "id": "orgTree",
                        "dataSource": "api://organizations/tree",
                        "fieldNames": {
                            "title": "name",
                            "key": "id",
                            "children": "children"
                        },
                        "actions": [
                            {
                                "type": "button",
                                "text": "编辑",
                                "permission": "org:edit",
                                "props": {
                                    "type": "primary",
                                    "size": "small"
                                },
                                "events": {
                                    "click": "handleEditOrg"
                                }
                            },
                            {
                                "type": "button",
                                "text": "删除",
                                "permission": "org:delete",
                                "props": {
                                    "type": "danger",
                                    "size": "small"
                                },
                                "disabled": "{{node.isRoot}}",
                                "events": {
                                    "click": "handleDeleteOrg"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }

if __name__ == "__main__":
    create_page_configs() 