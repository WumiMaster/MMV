"""
数据库配置模块
使用 SQLAlchemy 连接 SQLite 数据库
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接地址
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 需要此参数
)

# 启用 SQLite 外键约束支持
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 模型基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    用于 FastAPI 依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
