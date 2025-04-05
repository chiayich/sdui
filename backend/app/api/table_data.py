from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
import traceback

from app.database import get_db
from app.models.table_data import TableData
from app.schemas.table_data import TableDataCreate, TableDataUpdate, TableDataResponse, TableDataList

# 创建路由器，打印路由信息
router = APIRouter(prefix="/table-data")
print("\nTable Data Router paths:")
for route in router.routes:
    print(f"- {route.methods} {route.path}")

@router.post("/search", response_model=TableDataList)
async def get_table_data(
    page: int = 1,
    page_size: int = 10,
    name: Optional[str] = None,
    status: Optional[str] = None,
    create_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取表格数据列表"""
    try:
        print(f"\nReceived search request:")
        print(f"- Page: {page}")
        print(f"- Page Size: {page_size}")
        print(f"- Name Filter: {name}")
        print(f"- Status Filter: {status}")
        print(f"- Create Date Filter: {create_date}")
        
        query = db.query(TableData)
        
        # 应用筛选条件
        if name:
            query = query.filter(TableData.name.ilike(f"%{name}%"))
            print(f"Applied name filter: {name}")
        if status:
            query = query.filter(TableData.status == status)
            print(f"Applied status filter: {status}")
        if create_date:
            try:
                date = datetime.strptime(create_date, "%Y-%m-%d")
                query = query.filter(
                    TableData.create_date >= date,
                    TableData.create_date < date + timedelta(days=1)
                )
                print(f"Applied date filter: {create_date}")
            except ValueError as e:
                print(f"Date parsing error: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Invalid date format: {create_date}")
        
        # 计算总数
        total = query.count()
        print(f"Total matching records: {total}")
        
        # 分页
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        print(f"Retrieved {len(items)} items for current page")
        
        result = {
            "items": items,
            "total": total
        }
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_table_data: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=TableDataResponse)
async def create_table_data(request: Request, data: TableDataCreate, db: Session = Depends(get_db)):
    """创建新的表格数据"""
    try:
        # 验证必填字段
        if not data.name or not data.name.strip():
            raise HTTPException(status_code=400, detail="Name is required")
        if not data.status or not data.status.strip():
            raise HTTPException(status_code=400, detail="Status is required")
            
        # 创建数据库对象
        db_item = TableData(
            name=data.name.strip(),
            status=data.status.strip(),
            description=data.description.strip() if data.description else None
        )
        
        # 添加到数据库
        try:
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
        except Exception as db_error:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
            
        # 转换为响应模型
        return TableDataResponse(
            id=db_item.id,
            name=db_item.name,
            status=db_item.status,
            description=db_item.description,
            create_date=db_item.create_date,
            update_date=db_item.update_date
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{item_id}", response_model=TableDataResponse)
async def update_table_data(item_id: int, data: TableDataUpdate, db: Session = Depends(get_db)):
    try:
        print(f"Received update request for item {item_id}:", data.dict())  # 添加调试日志
        db_item = db.query(TableData).filter(TableData.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        
        db.commit()
        db.refresh(db_item)
        print(f"Successfully updated item {item_id}")  # 添加调试日志
        return db_item
    except Exception as e:
        db.rollback()
        print(f"Error updating item {item_id}:", str(e))  # 添加调试日志
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{item_id}")
async def delete_table_data(item_id: int, db: Session = Depends(get_db)):
    try:
        print(f"Received delete request for item {item_id}")  # 添加调试日志
        db_item = db.query(TableData).filter(TableData.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        db.delete(db_item)
        db.commit()
        print(f"Successfully deleted item {item_id}")  # 添加调试日志
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        print(f"Error deleting item {item_id}:", str(e))  # 添加调试日志
        raise HTTPException(status_code=400, detail=str(e)) 