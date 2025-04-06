from app.db.session import SessionLocal
from app.models.sdui_config import SDUIConfig

def update_logo_path():
    """更新所有结构配置中的logo路径"""
    db = SessionLocal()
    try:
        # 查询所有结构配置
        configs = db.query(SDUIConfig).filter(SDUIConfig.config_type == 'structure').all()
        updated = 0
        
        for config in configs:
            if '/logo.png' in str(config.content):
                # 更新logo路径
                config.content['navigation']['logo'] = '/static/logos/logo.png'
                updated += 1
        
        # 提交更改
        if updated > 0:
            db.commit()
            print(f'已更新 {updated} 个配置的logo路径')
        else:
            print('没有需要更新的配置')
    
    finally:
        db.close()

if __name__ == "__main__":
    update_logo_path() 