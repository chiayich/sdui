from app.db.session import SessionLocal
from app.models.sdui_config import SDUIConfig

def update_home_config():
    """更新首页配置中的菜单结构"""
    db = SessionLocal()
    try:
        # 查询首页配置
        home_config = db.query(SDUIConfig).filter(SDUIConfig.code == 'home').first()
        if not home_config:
            print("首页配置不存在")
            return
        
        # 更新菜单结构
        if 'layout' in home_config.content and 'sider' in home_config.content['layout'] and 'menu' in home_config.content['layout']['sider']:
            menu = home_config.content['layout']['sider']['menu']
            
            # 更新商品流通菜单
            flow_menu = next((item for item in menu if item.get('key') == 'flow'), None)
            if flow_menu:
                # 添加路由到子菜单
                for child in flow_menu.get('children', []):
                    if 'key' in child:
                        route = f"/flow/{child['key']}"
                        child['route'] = route
                        print(f"更新商品流通子菜单路由: {child['title']} -> {route}")
            
            # 更新系统管理菜单
            system_menu = next((item for item in menu if item.get('key') == 'system'), None)
            if system_menu:
                system_menu['title'] = '系统管理'
                system_menu['children'] = [
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
                print("更新系统管理菜单结构")
            
            # 提交更改
            db.commit()
            print("首页配置更新成功")
        else:
            print("首页配置结构不匹配")
    
    finally:
        db.close()

if __name__ == "__main__":
    update_home_config() 