from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional, Dict, Any

router = APIRouter()

@router.get("/templates", response_model=List[dict])
async def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    template_type: Optional[str] = None
):
    """获取UI模板列表"""
    # 临时模拟数据
    return [
        {"id": "template1", "name": "主页模板", "type": "home", "version": "1.0.0"},
        {"id": "template2", "name": "详情页模板", "type": "detail", "version": "1.0.0"}
    ]

@router.get("/templates/{template_id}", response_model=dict)
async def get_template_by_id(
    template_id: str = Path(..., description="UI模板ID")
):
    """根据ID获取UI模板"""
    # 临时模拟数据
    if template_id == "template1":
        return {"id": "template1", "name": "主页模板", "type": "home", "version": "1.0.0"}
    raise HTTPException(status_code=404, detail="Template not found")

@router.post("/templates", response_model=dict, status_code=201)
async def create_template(
    template: dict
):
    """创建UI模板"""
    # 临时模拟数据
    return {"id": "template3", "name": template.get("name"), "type": template.get("type"), "version": "1.0.0"}

@router.put("/templates/{template_id}", response_model=dict)
async def update_template(
    template_id: str,
    template_update: dict
):
    """更新UI模板"""
    # 临时模拟数据
    if template_id == "template1":
        return {"id": "template1", "name": template_update.get("name"), "type": "home", "version": "1.0.0"}
    raise HTTPException(status_code=404, detail="Template not found")

@router.delete("/templates/{template_id}", status_code=204)
async def delete_template(
    template_id: str
):
    """删除UI模板"""
    # 临时模拟逻辑
    if template_id not in ["template1", "template2"]:
        raise HTTPException(status_code=404, detail="Template not found")
    return None

@router.get("/screens/{screen_id}", response_model=Dict[str, Any])
async def get_ui_config(
    screen_id: str,
    platform: Optional[str] = Query(None, description="客户端平台，如ios, android, web"),
    theme: Optional[str] = Query(None, description="UI主题"),
    locale: Optional[str] = Query(None, description="本地化设置")
):
    """获取屏幕UI配置"""
    # 临时模拟数据
    if screen_id == "home":
        return {
            "version": "1.0.0",
            "screen": {
                "id": "home",
                "title": "Home Screen",
                "components": [
                    {
                        "type": "container",
                        "id": "main-container",
                        "style": {"padding": 16},
                        "children": [
                            {
                                "type": "text",
                                "id": "welcome-text",
                                "content": "Welcome to SDUI",
                                "style": {"fontSize": 24, "fontWeight": "bold"}
                            },
                            {
                                "type": "button",
                                "id": "action-button",
                                "label": "Click Me",
                                "style": {"marginTop": 16},
                                "action": {"type": "navigate", "target": "detail"}
                            }
                        ]
                    }
                ]
            }
        }
    raise HTTPException(status_code=404, detail="Screen configuration not found") 