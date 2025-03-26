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

        # 尝试获取请求体，但不消耗它
        request_body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                request_body_bytes = await request.body()
                # 重新设置请求体，以便后续处理
                request._body = request_body_bytes
                # 仅记录小于10KB的请求体
                if len(request_body_bytes) < 10 * 1024:
                    request_body = request_body_bytes.decode()
            except Exception:
                # 如果解析失败，不记录请求体
                pass

        # 记录基本请求信息
        path = request.url.path
        method = request.method

        # 包装Response对象以捕获状态码和响应体
        response_body = []

        class ResponseCapture:
            def __init__(self, response: Response):
                self.response = response
                self.status_code = response.status_code

            async def __call__(self, scope, receive, send):
                async def send_wrapper(message):
                    if message["type"] == "http.response.body":
                        response_body.append(message.get("body", b""))
                    await send(message)

                await self.response(scope, receive, send_wrapper)

        # 调用下一个中间件或路由处理器
        try:
            response = await call_next(request)
            duration = (time.time() - start_time) * 1000  # 毫秒

            # 包装响应以捕获响应体
            wrapped_response = ResponseCapture(response)

            # 记录日志（不包括响应体，响应体通常太大）
            logger_service.log_api_request(
                request_id=request_id,
                method=method,
                path=path,
                status_code=response.status_code,
                duration_ms=duration,
                request_data={"body": request_body} if request_body else None,
            )

            return wrapped_response

        except Exception as e:
            # 记录异常
            duration = (time.time() - start_time) * 1000
            logger_service.log(
                level="ERROR",
                message=f"API请求异常: {method} {path} - {str(e)}",
                source="api",
                metadata={
                    "request_id": request_id,
                    "method": method,
                    "path": path,
                    "duration_ms": duration,
                    "exception": str(e),
                    "request_body": request_body,
                },
            )
            # 重新抛出异常，让异常处理器处理
            raise
