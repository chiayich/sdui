from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.sdui_config import SDUIConfig
from app.schemas.sdui_config import SDUIConfigCreate, SDUIConfigUpdate


class CRUDSDUIConfig(CRUDBase[SDUIConfig, SDUIConfigCreate, SDUIConfigUpdate]):
    """SDUI配置CRUD操作类"""
    
    def get_by_code(self, db: Session, *, code: str) -> Optional[SDUIConfig]:
        """通过唯一标识码获取配置"""
        return db.query(self.model).filter(self.model.code == code).first()
    
    def get_by_type(self, db: Session, *, config_type: str) -> List[SDUIConfig]:
        """获取某个类型下的所有配置"""
        return db.query(self.model).filter(self.model.config_type == config_type).all()
    
    def get_by_code_and_type(self, db: Session, *, code: str, config_type: str) -> Optional[SDUIConfig]:
        """通过代码和类型获取配置"""
        return db.query(self.model).filter(
            self.model.code == code,
            self.model.config_type == config_type
        ).first()
    
    def create_or_update(self, db: Session, *, obj_in: SDUIConfigCreate) -> SDUIConfig:
        """创建或更新配置"""
        # 检查是否已存在
        existing = self.get_by_code(db, code=obj_in.code)
        
        if existing:
            # 更新现有配置
            update_data = {
                "name": obj_in.name,
                "content": obj_in.content,
                "description": obj_in.description,
                "config_type": obj_in.config_type
            }
            return self.update(db, db_obj=existing, obj_in=update_data)
        else:
            # 创建新配置
            return self.create(db, obj_in=obj_in)
    
    def search(self, db: Session, *, query: str, config_type: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[SDUIConfig]:
        """搜索配置"""
        search_query = f"%{query}%"
        base_query = db.query(self.model).filter(
            (self.model.code.ilike(search_query)) | 
            (self.model.name.ilike(search_query)) |
            (self.model.description.ilike(search_query))
        )
        
        if config_type:
            base_query = base_query.filter(self.model.config_type == config_type)
        
        return base_query.offset(skip).limit(limit).all()


sdui_config = CRUDSDUIConfig(SDUIConfig) 