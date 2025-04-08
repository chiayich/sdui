from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import logging

from ..config import settings
from ..db.session import get_db
from ..services.ui_service import UIService

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由
router = APIRouter()


# 模型定义
class UIComponent(BaseModel):
    id: str
    type: str
    properties: Dict[str, Any] = {}
    style: Dict[str, Any] = {}
    events: Dict[str, Any] = {}
    children: List[Dict[str, Any]] = []


class UITemplate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    components: List[UIComponent]


class UIResponse(BaseModel):
    template_id: str
    screen_name: str
    version: str
    components: List[UIComponent]
    metadata: Optional[Dict[str, Any]] = None


# 临时模拟数据 - 在实际应用中应从数据库获取
DEMO_TEMPLATES = {
    "home": {
        "id": "home",
        "name": "首页",
        "description": "应用首页",
        "version": "1.0.0",
        "components": [
            {
                "id": "header",
                "type": "container",
                "style": {"padding": "16px", "backgroundColor": "#f5f5f5"},
                "properties": {},
                "events": {},
                "children": [
                    {
                        "id": "title",
                        "type": "text",
                        "properties": {"content": "SDUI 演示应用"},
                        "style": {"fontSize": "24px", "fontWeight": "bold"},
                        "events": {},
                        "children": [],
                    }
                ],
            },
            {
                "id": "content",
                "type": "container",
                "style": {"padding": "16px"},
                "properties": {},
                "events": {},
                "children": [
                    {
                        "id": "welcome",
                        "type": "text",
                        "properties": {"content": "欢迎使用SDUI框架"},
                        "style": {"marginBottom": "16px"},
                        "events": {},
                        "children": [],
                    },
                    {
                        "id": "button",
                        "type": "button",
                        "properties": {"label": "查看详情"},
                        "style": {
                            "backgroundColor": "#1890ff",
                            "color": "white",
                            "padding": "8px 16px",
                        },
                        "events": {"click": {"type": "navigation", "url": "/details"}},
                        "children": [],
                    },
                ],
            },
        ],
    },
    "details": {
        "id": "details",
        "name": "详情页",
        "description": "应用详情页",
        "version": "1.0.0",
        "components": [
            {
                "id": "header",
                "type": "container",
                "style": {"padding": "16px", "backgroundColor": "#f5f5f5"},
                "properties": {},
                "events": {},
                "children": [
                    {
                        "id": "title",
                        "type": "text",
                        "properties": {"content": "详情页"},
                        "style": {"fontSize": "24px", "fontWeight": "bold"},
                        "events": {},
                        "children": [],
                    }
                ],
            },
            {
                "id": "content",
                "type": "container",
                "style": {"padding": "16px"},
                "properties": {},
                "events": {},
                "children": [
                    {
                        "id": "description",
                        "type": "text",
                        "properties": {"content": "这是一个SDUI驱动的UI示例"},
                        "style": {"marginBottom": "16px"},
                        "events": {},
                        "children": [],
                    },
                    {
                        "id": "back_button",
                        "type": "button",
                        "properties": {"label": "返回首页"},
                        "style": {
                            "backgroundColor": "#1890ff",
                            "color": "white",
                            "padding": "8px 16px",
                        },
                        "events": {"click": {"type": "navigation", "url": "/home"}},
                        "children": [],
                    },
                ],
            },
        ],
    },
}


@router.get("/templates", response_model=List[str])
async def get_available_templates():
    """获取所有可用的UI模板ID列表"""
    return list(DEMO_TEMPLATES.keys())


@router.get("/templates/{template_id}", response_model=UIResponse)
async def get_ui_template(
    template_id: str,
    platform: Optional[str] = Query("web", description="客户端平台类型"),
    version: Optional[str] = Query(None, description="请求的模板版本"),
    locale: Optional[str] = Query("zh-CN", description="本地化语言代码"),
):
    """获取指定ID的UI模板"""
    logger.info(
        f"请求UI模板: {template_id}, 平台: {platform}, 版本: {version}, 语言: {locale}"
    )

    if template_id not in DEMO_TEMPLATES:
        raise HTTPException(status_code=404, detail=f"模板 {template_id} 不存在")

    template = DEMO_TEMPLATES[template_id]

    # 在实际应用中，这里应该根据平台、版本和语言进行模板处理
    # 例如：应用特定平台的样式、翻译文本等

    response = UIResponse(
        template_id=template["id"],
        screen_name=template["name"],
        version=template["version"],
        components=[UIComponent(**comp) for comp in template["components"]],
        metadata={
            "requested_platform": platform,
            "requested_version": version,
            "locale": locale,
        },
    )

    return response


@router.get("/{screen_id}")
async def get_screen_ui(
    screen_id: str,
    platform: str = Query("web", description="客户端平台"),
    version: Optional[str] = Query(None, description="UI版本"),
    locale: str = Query("zh-CN", description="语言设置"),
):
    """获取指定屏幕的UI配置"""
    # 重定向到模板API，保持向后兼容性
    return await get_ui_template(screen_id, platform, version, locale)
