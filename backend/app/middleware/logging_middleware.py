import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.services.logger_service import logger_service


class LoggingMiddleware(BaseHTTPMiddleware):
    """日志中间件，记录所有API请求和响应"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # 生成请求ID
        request_id = str(uuid.uuid4())

        # 记录请求开始时间
        start_time = time.time()
        
        # 记录基本请求信息，不尝试读取请求体
        logger_service.log(
            level="INFO",
            message=f"开始处理请求: {request.method} {request.url}",
            source="api",
            metadata={"request_id": request_id}
        )

        try:
            # 调用下一个中间件或路由处理器
            response = await call_next(request)
            
            # 计算请求处理时间
            duration = (time.time() - start_time) * 1000  # 毫秒

            # 记录日志
            logger_service.log_api_request(
                request_id=request_id,
                method=request.method,
                path=str(request.url),
                status_code=response.status_code,
                duration_ms=duration,
                request_data=None  # 不记录请求体，避免性能问题
            )

            return response

        except Exception as e:
            # 记录异常
            duration = (time.time() - start_time) * 1000
            logger_service.log(
                level="ERROR",
                message=f"API请求异常: {request.method} {request.url} - {str(e)}",
                source="api",
                metadata={
                    "request_id": request_id,
                    "method": request.method,
                    "path": str(request.url),
                    "duration_ms": duration,
                    "exception": str(e)
                }
            )
            # 重新抛出异常，让异常处理器处理
            raise
