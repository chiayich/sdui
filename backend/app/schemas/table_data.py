from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class TableDataBase(BaseModel):
    name: str
    status: str
    description: Optional[str] = None

class TableDataCreate(TableDataBase):
    pass

class TableDataUpdate(TableDataBase):
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

class TableDataResponse(TableDataBase):
    id: int
    create_date: datetime
    update_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class TableDataList(BaseModel):
    items: List[TableDataResponse]
    total: int 