import logging
import json
import os
from pathlib import Path
from sqlalchemy.orm import Session
from app import crud
from app.schemas.sdui_config import SDUIConfigCreate

logger = logging.getLogger(__name__)

# 配置文件路径
DEFAULT_CONFIGS_PATH = Path(__file__).parent.parent.parent / "sdui_configs.json"

def migrate_default_configs(db: Session) -> None:
    """将默认的SDUI配置从JSON文件迁移到数据库"""
    
    logger.info("开始迁移默认SDUI配置到数据库...")
    
    # 检查配置文件是否存在
    if not os.path.exists(DEFAULT_CONFIGS_PATH):
        logger.warning(f"配置文件不存在: {DEFAULT_CONFIGS_PATH}")
        return
    
    try:
        # 从JSON文件加载配置
        with open(DEFAULT_CONFIGS_PATH, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        # 迁移每个配置
        for config in configs:
            # 检查配置是否已存在
            existing = crud.sdui_config.get_by_code(db, code=config["code"])
            
            if not existing:
                # 创建新配置
                sdui_config_in = SDUIConfigCreate(
                    code=config["code"],
                    name=config["name"],
                    config_type="page",  # 默认为页面类型
                    content=config["config_data"],
                    description=config.get("description", "")
                )
                
                try:
                    new_config = crud.sdui_config.create(db, obj_in=sdui_config_in)
                    logger.info(f"成功创建配置: {new_config.code}")
                except Exception as e:
                    logger.error(f"创建配置 {config['code']} 失败: {str(e)}")
            else:
                logger.info(f"配置 {config['code']} 已存在，跳过")
        
        logger.info("默认SDUI配置迁移完成")
    except Exception as e:
        logger.error(f"迁移过程发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    # 如果直接运行此脚本，则创建数据库会话并执行迁移
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        migrate_default_configs(db)
    finally:
        db.close() 