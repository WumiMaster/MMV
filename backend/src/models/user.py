"""
用户数据模型
定义用户表结构
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from ..config.database import Base
import enum


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    USER = "user"      # 普通用户
    ADMIN = "admin"    # 管理员


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名（登录用）")
    hashed_password = Column(String(128), nullable=False, comment="加密后的密码")
    nickname = Column(String(50), nullable=False, comment="对外显示昵称")
    avatar = Column(String(255), nullable=True, comment="头像文件路径")
    role = Column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
        comment="用户角色"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )
