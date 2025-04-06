-- SDUI配置初始化SQL
-- 创建SDUI配置表
CREATE TABLE IF NOT EXISTS sdui_configs (
    id UUID PRIMARY KEY,
    code VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    config_data JSONB NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    creator_id UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sdui_configs_code ON sdui_configs(code);
CREATE INDEX IF NOT EXISTS idx_sdui_configs_category ON sdui_configs(category);
CREATE INDEX IF NOT EXISTS idx_sdui_configs_name ON sdui_configs(name);

-- 插入系统管理页面配置
INSERT INTO sdui_configs (
    id, code, name, category, version, config_data, description, is_active, created_at, updated_at
) VALUES (
    gen_random_uuid(), 
    'system', 
    '系统管理主页', 
    'system', 
    1, 
    '{
        "type": "page",
        "id": "systemManagementPage",
        "title": "系统管理",
        "content": [
            {
                "type": "container",
                "children": [
                    {
                        "type": "title",
                        "level": 2,
                        "content": "系统管理"
                    },
                    {
                        "type": "row",
                        "gutter": 24,
                        "children": [
                            {
                                "type": "col",
                                "span": {
                                    "xs": 24,
                                    "sm": 12,
                                    "md": 8,
                                    "lg": 6
                                },
                                "children": [
                                    {
                                        "type": "card",
                                        "hoverable": true,
                                        "className": "system-card",
                                        "events": {
                                            "click": {
                                                "type": "navigate",
                                                "target": "/system/organization"
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
                                                        "className": "card-icon"
                                                    },
                                                    {
                                                        "type": "container",
                                                        "children": [
                                                            {
                                                                "type": "text",
                                                                "content": "组织架构管理",
                                                                "level": "h3"
                                                            },
                                                            {
                                                                "type": "text",
                                                                "content": "管理公司组织架构及部门",
                                                                "className": "text-muted"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "col",
                                "span": {
                                    "xs": 24,
                                    "sm": 12,
                                    "md": 8,
                                    "lg": 6
                                },
                                "children": [
                                    {
                                        "type": "card",
                                        "hoverable": true,
                                        "className": "system-card",
                                        "events": {
                                            "click": {
                                                "type": "navigate",
                                                "target": "/system/role"
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
                                                        "className": "card-icon"
                                                    },
                                                    {
                                                        "type": "container",
                                                        "children": [
                                                            {
                                                                "type": "text",
                                                                "content": "角色权限管理",
                                                                "level": "h3"
                                                            },
                                                            {
                                                                "type": "text",
                                                                "content": "管理系统角色及权限设置",
                                                                "className": "text-muted"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "col",
                                "span": {
                                    "xs": 24,
                                    "sm": 12,
                                    "md": 8,
                                    "lg": 6
                                },
                                "children": [
                                    {
                                        "type": "card",
                                        "hoverable": true,
                                        "className": "system-card",
                                        "events": {
                                            "click": {
                                                "type": "navigate",
                                                "target": "/system/user"
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
                                                        "className": "card-icon"
                                                    },
                                                    {
                                                        "type": "container",
                                                        "children": [
                                                            {
                                                                "type": "text",
                                                                "content": "用户管理",
                                                                "level": "h3"
                                                            },
                                                            {
                                                                "type": "text",
                                                                "content": "管理系统用户及账号权限",
                                                                "className": "text-muted"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "col",
                                "span": {
                                    "xs": 24,
                                    "sm": 12,
                                    "md": 8,
                                    "lg": 6
                                },
                                "children": [
                                    {
                                        "type": "card",
                                        "hoverable": true,
                                        "className": "system-card",
                                        "events": {
                                            "click": {
                                                "type": "navigate",
                                                "target": "/system/config"
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
                                                        "className": "card-icon"
                                                    },
                                                    {
                                                        "type": "container",
                                                        "children": [
                                                            {
                                                                "type": "text",
                                                                "content": "系统配置",
                                                                "level": "h3"
                                                            },
                                                            {
                                                                "type": "text",
                                                                "content": "管理系统基础配置项",
                                                                "className": "text-muted"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "styles": {
            ".system-card": {
                "height": "130px",
                "cursor": "pointer",
                "transition": "all 0.3s"
            },
            ".system-card:hover": {
                "transform": "translateY(-5px)",
                "boxShadow": "0 2px 12px 0 rgba(0, 0, 0, 0.1)"
            },
            ".card-icon": {
                "fontSize": "36px",
                "padding": "20px",
                "color": "#409eff"
            },
            ".text-muted": {
                "color": "#909399",
                "fontSize": "14px"
            }
        }
    }',
    '系统管理主页UI配置',
    TRUE,
    NOW(),
    NOW()
);

-- 插入组织架构管理页面配置
INSERT INTO sdui_configs (
    id, code, name, category, version, config_data, description, is_active, created_at, updated_at
) VALUES (
    gen_random_uuid(), 
    'system.organization', 
    '组织架构管理页面', 
    'system', 
    1, 
    '{
        "type": "page",
        "id": "organizationManagementPage",
        "title": "组织架构管理",
        "layout": {
            "type": "splitPane",
            "leftWidth": "30%",
            "rightWidth": "70%",
            "left": {
                "type": "card",
                "title": "组织架构树",
                "content": {
                    "type": "tree",
                    "id": "orgTree",
                    "dataSource": "api://organization/tree",
                    "props": {
                        "nodeKey": "id",
                        "labelKey": "name",
                        "defaultExpandAll": true
                    },
                    "events": {
                        "nodeClick": "handleNodeClick"
                    },
                    "actions": [
                        {
                            "type": "button",
                            "text": "添加根节点",
                            "permission": "organization:add",
                            "props": {
                                "type": "primary",
                                "size": "small"
                            },
                            "events": {
                                "click": "handleAddRoot"
                            }
                        }
                    ]
                }
            },
            "right": {
                "type": "card",
                "title": "节点详情",
                "content": {
                    "type": "dynamicContent",
                    "id": "nodeDetail",
                    "loading": "{{loading}}",
                    "emptyText": "请从左侧选择一个组织节点",
                    "content": {
                        "type": "container",
                        "visible": "{{!!selectedNode}}",
                        "children": [
                            {
                                "type": "descriptions",
                                "title": "基本信息",
                                "items": [
                                    { "label": "节点ID", "value": "{{selectedNode.id}}" },
                                    { "label": "节点名称", "value": "{{selectedNode.name}}" },
                                    { "label": "节点编码", "value": "{{selectedNode.code}}" },
                                    { "label": "节点类型", "value": "{{selectedNode.node_type}}" },
                                    { "label": "路径", "value": "{{selectedNode.path}}" }
                                ]
                            },
                            {
                                "type": "table",
                                "title": "子节点列表",
                                "visible": "{{selectedNode.children && selectedNode.children.length > 0}}",
                                "dataSource": "{{selectedNode.children}}",
                                "columns": [
                                    { "title": "名称", "dataIndex": "name" },
                                    { "title": "编码", "dataIndex": "code" },
                                    { "title": "类型", "dataIndex": "node_type" },
                                    {
                                        "title": "操作",
                                        "actions": [
                                            {
                                                "type": "button",
                                                "text": "查看",
                                                "props": { "type": "primary", "size": "small" },
                                                "events": { "click": "handleViewChild" }
                                            },
                                            {
                                                "type": "button",
                                                "text": "编辑",
                                                "permission": "organization:edit",
                                                "props": { "type": "info", "size": "small" },
                                                "events": { "click": "handleEditChild" }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "button",
                            "text": "添加子节点",
                            "permission": "organization:add",
                            "visible": "{{canAddChild}}",
                            "props": { "type": "primary", "size": "small" },
                            "events": { "click": "handleAddChild" }
                        },
                        {
                            "type": "button",
                            "text": "编辑节点",
                            "permission": "organization:edit",
                            "visible": "{{!!selectedNode}}",
                            "props": { "type": "info", "size": "small" },
                            "events": { "click": "handleEdit" }
                        },
                        {
                            "type": "button",
                            "text": "删除节点",
                            "permission": "organization:delete",
                            "visible": "{{canDelete}}",
                            "props": { "type": "danger", "size": "small" },
                            "events": { "click": "handleDelete" }
                        }
                    ]
                }
            }
        }
    }',
    '组织架构管理页面UI配置',
    TRUE,
    NOW(),
    NOW()
);

-- 插入角色权限管理页面配置
INSERT INTO sdui_configs (
    id, code, name, category, version, config_data, description, is_active, created_at, updated_at
) VALUES (
    gen_random_uuid(), 
    'system.role', 
    '角色权限管理页面', 
    'system', 
    1, 
    '{
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
                            "props": { "type": "primary" },
                            "events": { "click": "handleAddRole" }
                        }
                    ],
                    "content": {
                        "type": "table",
                        "id": "roleTable",
                        "dataSource": "api://roles",
                        "pagination": true,
                        "columns": [
                            { "title": "角色名称", "dataIndex": "name" },
                            { "title": "描述", "dataIndex": "description" },
                            { "title": "创建时间", "dataIndex": "created_at", "format": "datetime" },
                            {
                                "title": "状态",
                                "dataIndex": "is_active",
                                "render": {
                                    "type": "tag",
                                    "options": [
                                        { "value": true, "label": "启用", "color": "success" },
                                        { "value": false, "label": "禁用", "color": "danger" }
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
                                        "props": { "type": "primary", "size": "small" },
                                        "events": { "click": "handleEditRole" }
                                    },
                                    {
                                        "type": "button",
                                        "text": "权限设置",
                                        "permission": "role:permission",
                                        "props": { "type": "info", "size": "small" },
                                        "events": { "click": "handleRolePermission" }
                                    },
                                    {
                                        "type": "button",
                                        "text": "数据权限",
                                        "permission": "role:permission",
                                        "props": { "type": "warning", "size": "small" },
                                        "events": { "click": "handleRoleDataPermission" }
                                    },
                                    {
                                        "type": "button",
                                        "text": "删除",
                                        "permission": "role:delete",
                                        "props": { "type": "danger", "size": "small" },
                                        "disabled": "{{record.is_system}}",
                                        "events": { "click": "handleDeleteRole" }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }',
    '角色权限管理页面UI配置',
    TRUE,
    NOW(),
    NOW()
);

-- 插入用户管理页面配置
INSERT INTO sdui_configs (
    id, code, name, category, version, config_data, description, is_active, created_at, updated_at
) VALUES (
    gen_random_uuid(), 
    'system.user', 
    '用户管理页面', 
    'system', 
    1, 
    '{
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
                            "props": { "type": "primary" },
                            "events": { "click": "handleAddUser" }
                        }
                    ],
                    "content": {
                        "type": "table",
                        "id": "userTable",
                        "dataSource": "api://users",
                        "pagination": true,
                        "columns": [
                            { "title": "用户名", "dataIndex": "username" },
                            { "title": "姓名", "dataIndex": "full_name" },
                            { "title": "邮箱", "dataIndex": "email" },
                            { 
                                "title": "所属组织", 
                                "dataIndex": "primary_org_node.name",
                                "defaultValue": "-"
                            },
                            {
                                "title": "状态",
                                "dataIndex": "is_active",
                                "render": {
                                    "type": "tag",
                                    "options": [
                                        { "value": true, "label": "启用", "color": "success" },
                                        { "value": false, "label": "禁用", "color": "danger" }
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
                                        "props": { "type": "primary", "size": "small" },
                                        "events": { "click": "handleEditUser" }
                                    },
                                    {
                                        "type": "button",
                                        "text": "角色设置",
                                        "permission": "user:role",
                                        "props": { "type": "info", "size": "small" },
                                        "events": { "click": "handleUserRole" }
                                    },
                                    {
                                        "type": "button",
                                        "text": "删除",
                                        "permission": "user:delete",
                                        "props": { "type": "danger", "size": "small" },
                                        "events": { "click": "handleDeleteUser" }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }',
    '用户管理页面UI配置',
    TRUE,
    NOW(),
    NOW()
);

-- 插入首页配置
INSERT INTO sdui_configs (
    id, code, name, category, version, config_data, description, is_active, created_at, updated_at
) VALUES (
    gen_random_uuid(), 
    'home', 
    '首页', 
    'page', 
    1, 
    '{
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
                                "title": "商品流通工作台"
                            },
                            {
                                "key": "collection",
                                "title": "集货"
                            },
                            {
                                "key": "instruction",
                                "title": "流通指令",
                                "active": true
                            },
                            {
                                "key": "simulation",
                                "title": "仿真评估"
                            },
                            {
                                "key": "overview",
                                "title": "门店概览"
                            }
                        ]
                    },
                    {
                        "key": "system",
                        "icon": "setting",
                        "title": "系统配置"
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
                        "showTotal": true
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
    }',
    '商品流通首页UI配置',
    TRUE,
    NOW(),
    NOW()
);

-- 插入操作指南页面配置
INSERT INTO sdui_configs (
    id, code, name, category, version, config_data, description, is_active, created_at, updated_at
) VALUES (
    gen_random_uuid(), 
    'instruction', 
    '操作指南', 
    'page', 
    1, 
    '{
        "type": "page",
        "id": "instructionPage",
        "title": "操作指南",
        "content": [
            {
                "type": "container",
                "children": [
                    {
                        "type": "card",
                        "title": "SDUI系统操作指南",
                        "content": {
                            "type": "container",
                            "children": [
                                {
                                    "type": "title",
                                    "level": 2,
                                    "content": "什么是SDUI？"
                                },
                                {
                                    "type": "paragraph",
                                    "content": "服务端驱动UI（Server-Driven UI，简称SDUI）是一种前后端分离架构模式，它将UI的配置和渲染逻辑从前端移至后端。后端通过API向前端提供UI配置，前端根据这些配置动态渲染界面。这种方式使得UI变更可以在服务端完成，无需频繁更新前端应用。"
                                },
                                {
                                    "type": "title",
                                    "level": 3,
                                    "content": "主要功能"
                                },
                                {
                                    "type": "list",
                                    "listType": "ul",
                                    "items": [
                                        "动态页面：根据后端配置渲染不同页面，支持页面快速调整",
                                        "权限控制：根据用户权限显示不同的UI元素和功能",
                                        "组织管理：多级组织结构管理，支持不同组织层级的权限分配",
                                        "角色权限：基于角色的权限控制系统，精细化管理用户权限"
                                    ]
                                },
                                {
                                    "type": "title",
                                    "level": 3,
                                    "content": "操作流程"
                                },
                                {
                                    "type": "steps",
                                    "direction": "vertical",
                                    "items": [
                                        {
                                            "title": "系统登录",
                                            "description": "使用分配的账号和密码登录系统"
                                        },
                                        {
                                            "title": "系统首页",
                                            "description": "查看系统概览，选择需要进入的功能模块"
                                        },
                                        {
                                            "title": "组织管理",
                                            "description": "进入系统管理-组织架构管理，可以创建和编辑组织结构"
                                        },
                                        {
                                            "title": "角色权限",
                                            "description": "进入系统管理-角色权限管理，设置不同角色的权限范围"
                                        },
                                        {
                                            "title": "用户管理",
                                            "description": "进入系统管理-用户管理，创建用户并分配角色和所属组织"
                                        }
                                    ]
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "text": "返回首页",
                                    "props": {
                                        "type": "primary"
                                    },
                                    "events": {
                                        "click": {
                                            "type": "navigate",
                                            "target": "/"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }',
    '操作指南页面UI配置',
    TRUE,
    NOW(),
    NOW()
);

-- 插入模拟演示页面配置
INSERT INTO sdui_configs (
    id, code, name, category, version, config_data, description, is_active, created_at, updated_at
) VALUES (
    gen_random_uuid(), 
    'simulation', 
    '模拟演示', 
    'page', 
    1, 
    '{
        "type": "page",
        "id": "simulationPage",
        "title": "模拟演示",
        "content": [
            {
                "type": "container",
                "children": [
                    {
                        "type": "card",
                        "title": "SDUI组件演示",
                        "content": {
                            "type": "container",
                            "children": [
                                {
                                    "type": "title",
                                    "level": 2,
                                    "content": "动态表单示例"
                                },
                                {
                                    "type": "form",
                                    "id": "demoForm",
                                    "labelWidth": "120px",
                                    "items": [
                                        {
                                            "type": "input",
                                            "label": "用户名",
                                            "name": "username",
                                            "placeholder": "请输入用户名",
                                            "rules": [
                                                { "required": true, "message": "请输入用户名" }
                                            ]
                                        },
                                        {
                                            "type": "password",
                                            "label": "密码",
                                            "name": "password",
                                            "placeholder": "请输入密码",
                                            "rules": [
                                                { "required": true, "message": "请输入密码" },
                                                { "min": 6, "message": "密码长度不能小于6位" }
                                            ]
                                        },
                                        {
                                            "type": "select",
                                            "label": "部门",
                                            "name": "department",
                                            "placeholder": "请选择所属部门",
                                            "options": [
                                                { "label": "研发部", "value": "dev" },
                                                { "label": "市场部", "value": "marketing" },
                                                { "label": "销售部", "value": "sales" },
                                                { "label": "财务部", "value": "finance" }
                                            ]
                                        },
                                        {
                                            "type": "radio",
                                            "label": "性别",
                                            "name": "gender",
                                            "options": [
                                                { "label": "男", "value": "male" },
                                                { "label": "女", "value": "female" }
                                            ]
                                        },
                                        {
                                            "type": "checkbox",
                                            "label": "兴趣爱好",
                                            "name": "hobbies",
                                            "options": [
                                                { "label": "阅读", "value": "reading" },
                                                { "label": "运动", "value": "sports" },
                                                { "label": "旅游", "value": "travel" },
                                                { "label": "电影", "value": "movies" }
                                            ]
                                        },
                                        {
                                            "type": "datePicker",
                                            "label": "入职日期",
                                            "name": "entryDate"
                                        },
                                        {
                                            "type": "textarea",
                                            "label": "个人简介",
                                            "name": "introduction",
                                            "placeholder": "请输入个人简介",
                                            "rows": 4
                                        }
                                    ],
                                    "actions": [
                                        {
                                            "type": "button",
                                            "text": "提交",
                                            "props": {
                                                "type": "primary"
                                            },
                                            "events": {
                                                "click": "handleFormSubmit"
                                            }
                                        },
                                        {
                                            "type": "button",
                                            "text": "重置",
                                            "events": {
                                                "click": "handleFormReset"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "title",
                                    "level": 2,
                                    "content": "动态表格示例"
                                },
                                {
                                    "type": "table",
                                    "id": "demoTable",
                                    "data": [
                                        {
                                            "id": 1,
                                            "name": "张三",
                                            "age": 28,
                                            "department": "研发部",
                                            "position": "前端工程师",
                                            "status": "active"
                                        },
                                        {
                                            "id": 2,
                                            "name": "李四",
                                            "age": 32,
                                            "department": "研发部",
                                            "position": "后端工程师",
                                            "status": "active"
                                        },
                                        {
                                            "id": 3,
                                            "name": "王五",
                                            "age": 35,
                                            "department": "市场部",
                                            "position": "市场经理",
                                            "status": "inactive"
                                        },
                                        {
                                            "id": 4,
                                            "name": "赵六",
                                            "age": 25,
                                            "department": "销售部",
                                            "position": "销售代表",
                                            "status": "active"
                                        }
                                    ],
                                    "columns": [
                                        { "title": "ID", "dataIndex": "id" },
                                        { "title": "姓名", "dataIndex": "name" },
                                        { "title": "年龄", "dataIndex": "age" },
                                        { "title": "部门", "dataIndex": "department" },
                                        { "title": "职位", "dataIndex": "position" },
                                        {
                                            "title": "状态",
                                            "dataIndex": "status",
                                            "render": {
                                                "type": "tag",
                                                "options": [
                                                    { "value": "active", "label": "在职", "color": "success" },
                                                    { "value": "inactive", "label": "离职", "color": "danger" }
                                                ]
                                            }
                                        },
                                        {
                                            "title": "操作",
                                            "actions": [
                                                {
                                                    "type": "button",
                                                    "text": "编辑",
                                                    "props": { "type": "primary", "size": "small" },
                                                    "events": { "click": "handleEdit" }
                                                },
                                                {
                                                    "type": "button",
                                                    "text": "删除",
                                                    "props": { "type": "danger", "size": "small" },
                                                    "events": { "click": "handleDelete" }
                                                }
                                            ]
                                        }
                                    ],
                                    "pagination": {
                                        "pageSize": 10,
                                        "total": 4,
                                        "current": 1
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "text": "返回首页",
                                    "props": {
                                        "type": "primary"
                                    },
                                    "events": {
                                        "click": {
                                            "type": "navigate",
                                            "target": "/"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }',
    '模拟演示页面UI配置',
    TRUE,
    NOW(),
    NOW()
); 