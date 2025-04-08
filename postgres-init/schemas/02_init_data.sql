-- 创建管理员用户
INSERT INTO sdui_schema.users (username, email, hashed_password, is_active, is_superuser)
VALUES (
    'admin',
    'admin@example.com',
    '$2b$12$P8poAx9UXxmXGSAfmtpd/OybfBXFVnBaxLF5M8AYE7dvLD.q65I2i',  -- 密码: admin123
    TRUE,
    TRUE
);

-- 插入系统结构配置
INSERT INTO sdui_schema.sdui_configs (code, name, category, version, config_data, description, is_active)
VALUES 
('structure', '系统结构', 'structure', 1, '{
    "type": "layout",
    "props": {
        "navigation": {
            "items": [
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
                            "title": "流通指令"
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
                    "title": "系统管理",
                    "children": [
                        {
                            "key": "user",
                            "title": "用户管理"
                        },
                        {
                            "key": "role",
                            "title": "角色管理"
                        },
                        {
                            "key": "permission",
                            "title": "权限管理"
                        },
                        {
                            "key": "organization",
                            "title": "组织管理"
                        }
                    ]
                }
            ]
        }
    }
}', '系统导航结构配置', TRUE);

-- 插入系统管理页面配置
INSERT INTO sdui_schema.sdui_configs (code, name, category, version, config_data, description, is_active)
VALUES 
('system', '系统管理主页', 'system', 1, '{
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
}', '系统管理主页UI配置', TRUE);

-- 插入首页配置
INSERT INTO sdui_schema.sdui_configs (code, name, category, version, config_data, description, is_active)
VALUES 
('home', '首页', 'page', 1, '{
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
                    }
                ]
            }
        }
    ]
}', '商品流通首页UI配置', TRUE);

-- 创建根组织
INSERT INTO sdui_schema.organization_nodes (name, code, node_type, path, level)
VALUES ('根组织', 'root', 'company', '/root', 1)
ON CONFLICT (code) DO NOTHING;

-- 创建系统管理员角色
INSERT INTO sdui_schema.roles (name, description, is_system_role)
VALUES (
    '系统管理员',
    '具有所有系统权限的角色',
    TRUE
)
ON CONFLICT (name) DO NOTHING;

-- 创建基础权限
INSERT INTO sdui_schema.permissions (name, code, description)
VALUES 
    ('用户管理', 'user:manage', '管理用户的权限'),
    ('角色管理', 'role:manage', '管理角色的权限'),
    ('组织管理', 'org:manage', '管理组织的权限'),
    ('SDUI配置管理', 'sdui:manage', '管理SDUI配置的权限')
ON CONFLICT (code) DO NOTHING;

-- 为系统管理员角色分配所有权限
INSERT INTO sdui_schema.role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM sdui_schema.roles r
CROSS JOIN sdui_schema.permissions p
WHERE r.name = '系统管理员'
ON CONFLICT DO NOTHING;

-- 为管理员用户分配系统管理员角色
INSERT INTO sdui_schema.user_roles (user_id, role_id)
SELECT u.id, r.id
FROM sdui_schema.users u
CROSS JOIN sdui_schema.roles r
WHERE u.username = 'admin'
AND r.name = '系统管理员'
ON CONFLICT DO NOTHING;

-- 插入基础组件配置
INSERT INTO sdui_schema.sdui_configs (code, name, category, version, config_data, description, is_active)
VALUES 
    ('button_primary', '主按钮', 'component', 1, '{
        "type": "button",
        "props": {
            "variant": "primary"
        },
        "style": {
            "backgroundColor": "#1890ff",
            "color": "#ffffff",
            "borderRadius": "4px",
            "padding": "8px 16px"
        }
    }', '主要按钮组件配置', TRUE),
    
    ('card_default', '默认卡片', 'component', 1, '{
        "type": "card",
        "style": {
            "borderRadius": "8px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
            "padding": "16px",
            "margin": "8px"
        }
    }', '默认卡片组件配置', TRUE);

-- 插入布局结构配置
INSERT INTO sdui_schema.sdui_configs (code, name, category, version, config_data, description, is_active)
VALUES 
    ('layout_dashboard', '仪表盘布局', 'structure', 1, '{
        "type": "layout",
        "props": {
            "header": {
                "height": "64px",
                "fixed": true
            },
            "sidebar": {
                "width": "200px",
                "collapsible": true
            },
            "content": {
                "padding": "24px"
            }
        }
    }', '仪表盘页面布局结构', TRUE);

-- 创建组件关系
INSERT INTO sdui_schema.sdui_config_relations (parent_id, child_id, relation_type, position)
SELECT 
    p.id as parent_id,
    c.id as child_id,
    'contains',
    ROW_NUMBER() OVER (PARTITION BY p.id ORDER BY c.id)
FROM sdui_schema.sdui_configs p
JOIN sdui_schema.sdui_configs c ON c.category = 'component'
WHERE p.code = 'home_page'
AND c.code IN ('button_primary', 'card_default');

-- 页面配置
INSERT INTO sdui_schema.sdui_configs (code, name, category, version, config_data, description, is_active) 
VALUES 
('workbench', '商品流通工作台', 'page', 1, '{
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
}', '商品流通工作台页面配置', TRUE),
('collection', '集货', 'page', 1, '{
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
}', '集货页面配置', TRUE),
('instruction', '流通指令', 'page', 1, '{
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
}', '流通指令页面配置', TRUE)
ON CONFLICT (code) DO UPDATE 
SET config_data = EXCLUDED.config_data; 