from app.db.session import SessionLocal
from app.models.sdui_config import SDUIConfig
import json

def update_structure_configs():
    """更新所有结构配置，确保包含商品流通菜单"""
    db = SessionLocal()
    try:
        # 正确的菜单结构
        correct_navigation_items = [
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
        
        # 获取所有结构配置
        configs = db.query(SDUIConfig).filter(SDUIConfig.config_type == 'structure').all()
        print(f"Found {len(configs)} structure configs")
        
        for config in configs:
            print(f"Processing config: {config.code}")
            print(f"Before update: {json.dumps(config.content['navigation']['items'], indent=2, ensure_ascii=False)}")
            
            # 检查内容是否为字典
            if not isinstance(config.content, dict):
                print(f"Config content is not a dictionary for {config.code}! Type: {type(config.content)}")
                continue
                
            # 确保有正确的 logo 路径
            if 'navigation' in config.content and 'logo' in config.content['navigation']:
                config.content['navigation']['logo'] = '/static/logos/logo.png'
                print(f"Updated logo for {config.code}")
            
            # 更新菜单项
            if 'navigation' in config.content and 'items' in config.content['navigation']:
                config.content['navigation']['items'] = correct_navigation_items
                print(f"Updated navigation items for {config.code}")
                print(f"After update: {json.dumps(config.content['navigation']['items'], indent=2, ensure_ascii=False)}")
        
        # 提交所有修改
        db.commit()
        print(f"Successfully updated {len(configs)} structure configurations")
        
        # 验证更新
        for config in configs:
            db.refresh(config)
            print(f"Verification for {config.code}: {json.dumps(config.content['navigation']['items'][1]['key'], ensure_ascii=False)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    update_structure_configs() 