from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# 使用 settings 中的配置构建数据库 URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

print(f"Connecting to database: {SQLALCHEMY_DATABASE_URL}")

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # 启用SQL语句日志
    pool_pre_ping=True  # 启用连接池预检
)

# 添加引擎事件监听器
@event.listens_for(engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    print("New database connection established")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    print("Database connection checked out from pool")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    print("Database connection checked in to pool")

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话的依赖函数
def get_db():
    db = SessionLocal()
    try:
        print("Creating new database session")
        yield db
    except Exception as e:
        print(f"Error in database session: {e}")
        raise
    finally:
        print("Closing database session")
        db.close()

# 创建所有表
def init_db():
    try:
        # 检查数据库连接
        with engine.connect() as connection:
            print("Successfully connected to database")
            # 检查table_data表是否存在
            result = connection.execute(text(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'table_data')"
            ))
            exists = result.scalar()
            if not exists:
                print("Table 'table_data' does not exist, creating tables...")
                Base.metadata.create_all(bind=engine)
                print("Database tables created successfully")
            else:
                print("Table 'table_data' already exists")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise 