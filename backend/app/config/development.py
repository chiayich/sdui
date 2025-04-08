"""开发环境配置"""

# 开发环境特定的配置覆盖
development_settings = {
    "DEBUG": True,
    "ENV": "development",
    "DB_HOST": "localhost",
    "DB_PORT": 5432,
    "DB_USER": "huajin",
    "DB_PASSWORD": "",
    "DB_NAME": "sdui",
    "SQLALCHEMY_ECHO": True,  # 在开发环境下打印SQL语句
    "REDIS_HOST": "localhost",
    "REDIS_PORT": 6379,
} 