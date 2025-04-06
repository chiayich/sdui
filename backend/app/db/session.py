from app.db.database import engine, SessionLocal, Base

# 重新导出数据库会话和基类，避免重复定义
# 这个文件保留是为了保持向后兼容性，新代码应直接导入database.py 