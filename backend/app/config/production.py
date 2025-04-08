"""生产环境配置"""

# 生产环境特定的配置覆盖
production_settings = {
    "DEBUG": False,
    "ENV": "production",
    "CORS_ORIGINS": [
        "https://example.com",
        "https://www.example.com",
    ],
    "DB_HOST": "db.example.com",  # 生产环境数据库地址
    "DB_PORT": 5432,
    "DB_USER": "prod_user",
    "DB_PASSWORD": "",  # 通过环境变量设置
    "DB_NAME": "sdui_prod",
    "SQLALCHEMY_ECHO": False,
    "REDIS_HOST": "redis.example.com",  # 生产环境Redis地址
    "REDIS_PORT": 6379,
    "REDIS_PASSWORD": "",  # 通过环境变量设置
    "USE_REDIS_CACHE": True,
    "REDIS_CACHE_TTL": 3600,
} 