from fastapi import APIRouter, Depends, Query, Body
from typing import List, Dict, Any, Optional

from app.services.logger_service import get_logger_service, LoggerService

router = APIRouter()


@router.get("/logs", response_model=List[Dict[str, Any]])
async def get_logs(
    level: Optional[str] = Query(
        None, description="日志级别: DEBUG, INFO, WARNING, ERROR"
    ),
    source: Optional[str] = Query(None, description="日志源: app, api, ui"),
    limit: int = Query(100, ge=1, le=1000, description="每页限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    logger_service: LoggerService = Depends(get_logger_service),
):
    """
    获取系统日志

    - **level**: 过滤日志级别 (DEBUG, INFO, WARNING, ERROR)
    - **source**: 过滤日志源 (app, api, ui)
    - **limit**: 每页数量
    - **offset**: 分页偏移量
    """
    return logger_service.get_logs(
        level=level, source=source, limit=limit, offset=offset
    )


@router.post("/logs/batch")
async def batch_logs(
    logs_batch: Dict[str, List[Dict[str, Any]]] = Body(...),
    logger_service: LoggerService = Depends(get_logger_service),
):
    """
    批量记录日志

    接收前端批量发送的日志条目
    """
    logs = logs_batch.get("logs", [])
    results = []

    for log_entry in logs:
        level = log_entry.get("level", "INFO")
        message = log_entry.get("message", "")
        source = log_entry.get("source", "frontend")
        metadata = log_entry.get("metadata", {})

        # 记录日志
        result = logger_service.log(level, message, source, metadata)
        results.append(result)

    return {"status": "success", "processed": len(results)}


@router.get("/logs/sources")
async def get_log_sources():
    """获取所有可用的日志源"""
    return ["app", "api", "ui", "frontend"]


@router.get("/logs/levels")
async def get_log_levels():
    """获取所有可用的日志级别"""
    return ["DEBUG", "INFO", "WARNING", "ERROR"]
