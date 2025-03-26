import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import os
from fastapi import Depends

# 配置基础日志格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# 创建日志目录
log_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs"
)
os.makedirs(log_dir, exist_ok=True)


class LoggerService:
    """日志服务，提供统一的日志记录和查询功能"""

    def __init__(self):
        # 应用日志
        self.app_logger = logging.getLogger("sdui.app")
        # API请求日志
        self.api_logger = logging.getLogger("sdui.api")
        # UI渲染日志
        self.ui_logger = logging.getLogger("sdui.ui")

        # 设置文件处理器
        self._setup_file_handlers()

        # 内存缓存最近的日志(仅用于快速API访问)
        self.log_cache: List[Dict[str, Any]] = []
        self.max_cache_size = 1000

    def _setup_file_handlers(self):
        """设置文件日志处理器"""
        # 应用日志文件
        app_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
        app_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.app_logger.addHandler(app_handler)

        # API日志文件
        api_handler = logging.FileHandler(os.path.join(log_dir, "api.log"))
        api_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.api_logger.addHandler(api_handler)

        # UI日志文件
        ui_handler = logging.FileHandler(os.path.join(log_dir, "ui.log"))
        ui_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.ui_logger.addHandler(ui_handler)

    def log(
        self,
        level: str,
        message: str,
        source: str = "app",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """记录日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "source": source,
            "metadata": metadata or {},
        }

        # 添加到缓存
        self.log_cache.append(log_entry)
        if len(self.log_cache) > self.max_cache_size:
            self.log_cache.pop(0)

        # 根据日志级别选择相应的日志方法
        logger = getattr(self, f"{source}_logger")
        log_method = getattr(logger, level.lower())

        # 如果有元数据，将其转换为字符串
        if metadata:
            log_method(f"{message} - {json.dumps(metadata)}")
        else:
            log_method(message)

        return log_entry

    def log_api_request(
        self,
        request_id: str,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        request_data: Optional[Dict] = None,
        response_data: Optional[Dict] = None,
    ):
        """记录API请求日志"""
        metadata = {
            "request_id": request_id,
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": duration_ms,
        }

        # 可选择性地添加请求和响应数据（可能会很大，需要谨慎处理）
        if request_data:
            metadata["request_data"] = request_data
        if response_data:
            metadata["response_data"] = response_data

        # 根据状态码确定日志级别
        level = "INFO"
        if status_code >= 400:
            level = "WARNING"
        if status_code >= 500:
            level = "ERROR"

        return self.log(
            "INFO", f"API请求: {method} {path} - {status_code}", "api", metadata
        )

    def log_ui_render(
        self,
        screen_id: str,
        render_time_ms: float,
        components_count: int,
        context: Optional[Dict] = None,
    ):
        """记录UI渲染日志"""
        metadata = {
            "screen_id": screen_id,
            "render_time_ms": render_time_ms,
            "components_count": components_count,
        }

        if context:
            metadata["context"] = context

        return self.log(
            "INFO", f"UI渲染: {screen_id} - {render_time_ms}ms", "ui", metadata
        )

    def get_logs(
        self,
        level: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """获取日志"""
        # 根据条件筛选日志
        filtered_logs = self.log_cache

        if level:
            filtered_logs = [
                log for log in filtered_logs if log["level"] == level.upper()
            ]

        if source:
            filtered_logs = [log for log in filtered_logs if log["source"] == source]

        # 分页
        paginated_logs = filtered_logs[::-1][offset : offset + limit]

        return paginated_logs

    def clear_logs(self):
        """清空日志缓存（仅用于测试）"""
        self.log_cache = []


# 创建单例实例
logger_service = LoggerService()


def get_logger_service():
    """依赖注入函数"""
    return logger_service
