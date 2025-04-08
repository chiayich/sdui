"""
配置模块

用于管理应用的所有配置项，包括：
- 环境配置
- 数据库配置
- Redis配置
- 应用程序配置
等
"""

from .settings import Settings

# 创建全局配置实例
settings = Settings()

# 导出配置实例供其他模块使用
__all__ = ["settings"] 