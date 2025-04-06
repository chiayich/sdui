from app.db.session import SessionLocal
import json
from sqlalchemy import text

def update_structure_direct():
    """使用直接SQL更新所有结构配置"""
    db = SessionLocal()
    try:
        # 正确的菜单结构
        correct_navigation_items = [
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
        
        # 为structure创建完整配置
        structure_content = {
            "navigation": {
                "type": "sider",
                "logo": "/static/logos/logo.png",
                "title": "SDUI系统",
                "items": correct_navigation_items
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
        
        # 使用直接SQL更新结构配置
        structure_json = json.dumps(structure_content)
        update_sql = text("""
            UPDATE sdui_configs 
            SET content = :content 
            WHERE config_type = 'structure' AND code = :code
        """)
        
        # 更新 'structure'
        result = db.execute(update_sql, {"content": structure_json, "code": "structure"})
        print(f"Updated 'structure', affected rows: {result.rowcount}")
        
        # 更新 'system-structure'
        result = db.execute(update_sql, {"content": structure_json, "code": "system-structure"})
        print(f"Updated 'system-structure', affected rows: {result.rowcount}")
        
        # 提交事务
        db.commit()
        
        # 验证通过ORM方式
        from app.models.sdui_config import SDUIConfig
        
        # 验证 'structure'
        config = db.query(SDUIConfig).filter(SDUIConfig.code == 'structure').first()
        if config:
            print(f"Verification for 'structure' navigation items:")
            print(f"- First item: {config.content['navigation']['items'][0]['key']}")
            print(f"- Second item: {config.content['navigation']['items'][1]['key']}")
        
        # 验证 'system-structure'
        config = db.query(SDUIConfig).filter(SDUIConfig.code == 'system-structure').first()
        if config:
            print(f"Verification for 'system-structure' navigation items:")
            print(f"- First item: {config.content['navigation']['items'][0]['key']}")
            print(f"- Second item: {config.content['navigation']['items'][1]['key']}")
        
    finally:
        db.close()

if __name__ == "__main__":
    update_structure_direct() 