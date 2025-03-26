from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict, Any

router = APIRouter()

@router.get("/components", response_model=List[dict])
async def get_components(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    component_type: Optional[str] = None
):
    """获取组件列表"""
    # 临时模拟数据
    return [
        {"id": "comp1", "type": "container", "name": "MainContainer"},
        {"id": "comp2", "type": "text", "name": "TitleText"},
        {"id": "comp3", "type": "button", "name": "ActionButton"}
    ]

@router.get("/components/{component_id}", response_model=dict)
async def get_component_by_id(
    component_id: str = Path(..., description="组件ID")
):
    """根据ID获取组件"""
    # 临时模拟数据
    components = {
        "comp1": {
            "id": "comp1", 
            "type": "container", 
            "name": "MainContainer",
            "properties": {
                "style": {"padding": 16, "backgroundColor": "#fff"},
                "layout": "column"
            }
        },
        "comp2": {
            "id": "comp2", 
            "type": "text", 
            "name": "TitleText",
            "properties": {
                "content": "Title",
                "style": {"fontSize": 24, "fontWeight": "bold", "color": "#333"}
            }
        },
        "comp3": {
            "id": "comp3", 
            "type": "button", 
            "name": "ActionButton",
            "properties": {
                "label": "Click Me",
                "style": {"padding": "8px 16px", "backgroundColor": "#2196F3", "color": "#fff"},
                "action": {"type": "navigate", "target": "detail"}
            }
        }
    }
    
    if component_id in components:
        return components[component_id]
    raise HTTPException(status_code=404, detail="Component not found")

@router.post("/components", response_model=dict, status_code=201)
async def create_component(
    component: dict
):
    """创建组件"""
    # 临时模拟数据
    return {
        "id": "comp4", 
        "type": component.get("type", "unknown"), 
        "name": component.get("name", "NewComponent"),
        "properties": component.get("properties", {})
    }

@router.put("/components/{component_id}", response_model=dict)
async def update_component(
    component_id: str,
    component_update: dict
):
    """更新组件"""
    # 临时模拟数据
    components = ["comp1", "comp2", "comp3"]
    if component_id in components:
        return {
            "id": component_id, 
            "type": component_update.get("type", "unknown"), 
            "name": component_update.get("name", "UpdatedComponent"),
            "properties": component_update.get("properties", {})
        }
    raise HTTPException(status_code=404, detail="Component not found")

@router.delete("/components/{component_id}", status_code=204)
async def delete_component(
    component_id: str
):
    """删除组件"""
    # 临时模拟逻辑
    components = ["comp1", "comp2", "comp3"]
    if component_id not in components:
        raise HTTPException(status_code=404, detail="Component not found")
    return None

@router.get("/component-types", response_model=List[dict])
async def get_component_types():
    """获取支持的组件类型"""
    # 临时模拟数据
    return [
        {
            "type": "container",
            "displayName": "容器",
            "description": "用于包含其他组件的容器",
            "allowedChildren": ["*"],
            "properties": [
                {"name": "layout", "type": "string", "enum": ["row", "column", "grid"]},
                {"name": "style", "type": "object"}
            ]
        },
        {
            "type": "text",
            "displayName": "文本",
            "description": "显示文本内容",
            "allowedChildren": [],
            "properties": [
                {"name": "content", "type": "string"},
                {"name": "style", "type": "object"}
            ]
        },
        {
            "type": "button",
            "displayName": "按钮",
            "description": "可点击的按钮",
            "allowedChildren": [],
            "properties": [
                {"name": "label", "type": "string"},
                {"name": "action", "type": "object"},
                {"name": "style", "type": "object"}
            ]
        }
    ] 