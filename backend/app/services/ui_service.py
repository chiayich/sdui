import json
import logging
from typing import Dict, List, Optional, Any
from fastapi import Depends, HTTPException

from ..config import settings
from app.db.database import get_db
from .redis_service import get_redis

logger = logging.getLogger(__name__)

class UIService:
    """服务器驱动UI服务，负责获取和处理UI模板"""
    
    def __init__(self, db=Depends(get_db), redis=Depends(get_redis)):
        self.db = db
        self.redis = redis
    
    async def get_ui_config(self, screen_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取UI配置，支持缓存和A/B测试
        
        Args:
            screen_id: 屏幕ID
            context: 上下文信息（用户ID、平台、语言等）
            
        Returns:
            完整的UI配置
        """
        try:
            # 尝试从缓存获取
            if settings.USE_REDIS_CACHE:
                cache_key = f"ui_config:{screen_id}:{context.get('locale', 'zh-CN')}:{context.get('platform', 'web')}"
                cached_data = await self.redis.get(cache_key)
                if cached_data:
                    logger.info(f"缓存命中: {cache_key}")
                    return json.loads(cached_data)
            
            # 缓存未命中，从数据库获取
            logger.info(f"从数据库获取UI配置: {screen_id}")
            
            # 获取模板基本信息
            template = await self.db.fetch_one(
                """
                SELECT id, screen_id, title, version, description
                FROM ui_templates
                WHERE screen_id = $1 AND is_active = TRUE
                """,
                screen_id
            )
            
            if not template:
                raise HTTPException(status_code=404, detail=f"模板不存在: {screen_id}")
            
            # 检查是否有匹配的A/B测试变体
            variant_id = await self._get_matching_variant(template["id"], context)
            
            # 获取组件树
            if settings.USE_DB_FUNCTION:
                # 使用数据库函数获取组件树
                components_json = await self.db.fetch_val(
                    "SELECT get_component_tree($1)",
                    template["id"]
                )
                components = json.loads(components_json)
            else:
                # 手动构建组件树
                components = await self._build_component_tree(template["id"])
            
            # 如果有A/B测试变体，应用变体覆盖
            if variant_id:
                await self._apply_variant_overrides(components, variant_id)
            
            # 构建响应
            response = {
                "version": template["version"],
                "screen": {
                    "id": screen_id,
                    "title": template["title"],
                    "components": components
                },
                "metadata": {
                    "platform": context.get("platform", "web"),
                    "locale": context.get("locale", "zh-CN"),
                    "has_variant": variant_id is not None
                }
            }
            
            # 存入缓存
            if settings.USE_REDIS_CACHE:
                await self.redis.set(
                    cache_key,
                    json.dumps(response),
                    ex=settings.REDIS_CACHE_TTL
                )
                logger.info(f"UI配置已缓存: {cache_key}")
            
            return response
            
        except Exception as e:
            logger.error(f"获取UI配置失败: {str(e)}", exc_info=True)
            raise
    
    async def _get_matching_variant(self, template_id: int, context: Dict[str, Any]) -> Optional[int]:
        """获取匹配的变体ID"""
        # 简单实现，可根据需要扩展匹配逻辑
        variants = await self.db.fetch_all(
            """
            SELECT id, criteria
            FROM ui_template_variants
            WHERE template_id = $1 AND is_active = TRUE
            AND (start_date IS NULL OR start_date <= NOW())
            AND (end_date IS NULL OR end_date >= NOW())
            """,
            template_id
        )
        
        if not variants:
            return None
            
        # 简单匹配逻辑，可根据需要扩展
        for variant in variants:
            criteria = variant["criteria"]
            if not criteria:  # 空条件总是匹配
                return variant["id"]
                
            # 检查平台匹配
            if "platform" in criteria and context.get("platform") != criteria["platform"]:
                continue
                
            # 检查语言匹配
            if "locale" in criteria and context.get("locale") != criteria["locale"]:
                continue
                
            # 可以添加更多匹配规则
                
            # 所有条件都匹配
            return variant["id"]
            
        return None
    
    async def _build_component_tree(self, template_id: int) -> List[Dict[str, Any]]:
        """手动构建组件树"""
        # 获取所有组件
        all_components = await self.db.fetch_all(
            """
            SELECT id, component_id, component_type, parent_id, position,
                   properties, style, events
            FROM ui_components
            WHERE template_id = $1
            ORDER BY COALESCE(parent_id, 0), position
            """,
            template_id
        )
        
        # 构建组件映射
        components_by_id = {}
        root_components = []
        
        for comp in all_components:
            component = {
                "id": comp["component_id"],
                "type": comp["component_type"],
                "properties": comp["properties"],
                "style": comp["style"],
                "events": comp["events"],
                "children": []
            }
            
            components_by_id[comp["id"]] = component
            
            if comp["parent_id"] is None:
                root_components.append(component)
            else:
                # 添加到父组件的children列表中
                parent = components_by_id.get(comp["parent_id"])
                if parent:
                    parent["children"].append(component)
        
        return root_components
    
    async def _apply_variant_overrides(self, components: List[Dict[str, Any]], variant_id: int) -> None:
        """应用变体覆盖"""
        # 获取变体的组件覆盖
        overrides = await self.db.fetch_all(
            """
            SELECT component_id, properties, style, events
            FROM ui_variant_components
            WHERE variant_id = $1
            """,
            variant_id
        )
        
        if not overrides:
            return
            
        # 创建覆盖映射
        override_map = {o["component_id"]: o for o in overrides}
        
        # 递归应用覆盖
        def apply_overrides(component_list):
            for component in component_list:
                component_id = component["id"]
                if component_id in override_map:
                    override = override_map[component_id]
                    
                    # 合并properties
                    if override["properties"]:
                        component["properties"] = {**component["properties"], **override["properties"]}
                    
                    # 合并style
                    if override["style"]:
                        component["style"] = {**component["style"], **override["style"]}
                    
                    # 合并events
                    if override["events"]:
                        component["events"] = {**component["events"], **override["events"]}
                
                # 递归处理子组件
                if component.get("children"):
                    apply_overrides(component["children"])
        
        apply_overrides(components)
    
    async def get_all_templates(self) -> List[str]:
        """获取所有可用的模板ID"""
        templates = await self.db.fetch_all(
            """
            SELECT screen_id
            FROM ui_templates
            WHERE is_active = TRUE
            ORDER BY screen_id
            """
        )
        return [t["screen_id"] for t in templates] 