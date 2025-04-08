"""SDUI配置的CRUD操作实现

职责：
1. 实现配置数据的业务逻辑层
2. 封装数据库操作，提供高级查询方法
3. 处理配置的创建、读取、更新、删除等操作
4. 实现特定业务需求的查询方法

主要功能：
- get_by_code: 通过唯一标识码获取配置
- get_by_type: 获取特定类型的所有配置
- create_or_update: 创建或更新配置
- search: 支持多条件的配置搜索

使用示例：
```python
# 创建配置
config = crud.sdui_config.create(
    db=db,
    obj_in=SDUIConfigCreate(
        code="system.user",
        name="用户管理",
        category="system",
        config_data={"type": "page", ...}
    )
)

# 查询配置
config = crud.sdui_config.get_by_code(db, code="system.user")
```
"""

from typing import Any, Dict, List, Optional

from app.crud.base import CRUDBase
from app.models.sdui_config import SDUIConfig
from app.schemas.sdui_config import SDUIConfigCreate, SDUIConfigUpdate
from sqlalchemy.orm import Session


class CRUDSDUIConfig(CRUDBase[SDUIConfig, SDUIConfigCreate, SDUIConfigUpdate]):
    """SDUI配置CRUD操作类"""

    def get_by_code(self, db: Session, *, code: str) -> Optional[SDUIConfig]:
        """通过唯一标识码获取配置"""
        return db.query(self.model).filter(self.model.code == code).first()

    def get_by_category(self, db: Session, *, category: str) -> List[SDUIConfig]:
        """获取某个分类下的所有配置"""
        return db.query(self.model).filter(self.model.category == category).all()

    def get_by_code_and_category(
        self, db: Session, *, code: str, category: str
    ) -> Optional[SDUIConfig]:
        """通过代码和分类获取配置"""
        return (
            db.query(self.model)
            .filter(self.model.code == code, self.model.category == category)
            .first()
        )

    def create_or_update(self, db: Session, *, obj_in: SDUIConfigCreate) -> SDUIConfig:
        """创建或更新配置"""
        # 检查是否已存在
        existing = self.get_by_code(db, code=obj_in.code)

        if existing:
            # 更新现有配置
            update_data = {
                "name": obj_in.name,
                "config_data": obj_in.config_data,
                "description": obj_in.description,
                "category": obj_in.category,
            }
            return self.update(db, db_obj=existing, obj_in=update_data)
        else:
            # 创建新配置
            return self.create(db, obj_in=obj_in)

    def search(
        self,
        db: Session,
        *,
        query: str,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[SDUIConfig]:
        """搜索配置"""
        search_query = f"%{query}%"
        base_query = db.query(self.model).filter(
            (self.model.code.ilike(search_query))
            | (self.model.name.ilike(search_query))
            | (self.model.description.ilike(search_query))
        )

        if category:
            base_query = base_query.filter(self.model.category == category)

        return base_query.offset(skip).limit(limit).all()


sdui_config = CRUDSDUIConfig(SDUIConfig)
