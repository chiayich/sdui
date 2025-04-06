#!/usr/bin/env python
"""
SDUI 配置数据库迁移脚本
将hardcoded的配置迁移到数据库中
"""
import sys
import os
import logging
from pathlib import Path

# 将backend目录添加到系统路径，以便能够导入app包
sys.path.append(str(Path(__file__).parent))

from app.db.session import SessionLocal
from app.db.migrate_sdui_configs import migrate_default_configs

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("migration.log")
    ]
)

logger = logging.getLogger(__name__)

def main():
    """运行配置迁移"""
    logger.info("开始SDUI配置迁移...")
    
    # 创建数据库会话
    db = SessionLocal()
    try:
        # 执行迁移
        migrate_default_configs(db)
        db.commit()
        logger.info("SDUI配置迁移完成")
    except Exception as e:
        db.rollback()
        logger.error(f"迁移失败: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main() 