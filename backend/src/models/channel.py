"""
频道数据模型
包含频道、子频道、用户-频道关联表
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base


class Channel(Base):
    """
    频道表
    最高交流单元，由管理员创建
    """
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="频道名称")
    channel_id = Column(String(50), unique=True, index=True, nullable=False, comment="频道ID（自定义或自动生成）")
    description = Column(String(500), nullable=True, comment="频道描述")
    avatar = Column(String(255), nullable=True, comment="频道头像文件路径")
    message_retention_days = Column(Integer, default=30, comment="消息留存天数，默认30天")
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建者ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联关系
    creator = relationship("User", backref="created_channels")
    sub_channels = relationship("SubChannel", back_populates="channel", cascade="all, delete-orphan")
    members = relationship("UserChannel", back_populates="channel", cascade="all, delete-orphan")


class SubChannel(Base):
    """
    子频道表
    每个频道下可有多个文字或语音子频道
    """
    __tablename__ = "sub_channels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False, comment="所属频道ID")
    name = Column(String(100), nullable=False, comment="子频道名称")
    type = Column(String(20), nullable=False, comment="类型：text（文字）/ voice（语音）")
    sort_order = Column(Integer, default=0, comment="排序号，越小越靠前")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关联关系
    channel = relationship("Channel", back_populates="sub_channels")
    # 注意：messages 关系在 message.py 中定义，避免循环引用


class UserChannel(Base):
    """
    用户-频道关联表
    记录用户加入了哪些频道
    """
    __tablename__ = "user_channels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False, comment="频道ID")
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), comment="加入时间")

    # 关联关系
    user = relationship("User", backref="joined_channels")
    channel = relationship("Channel", back_populates="members")

    # 联合唯一约束：一个用户对一个频道只能加入一次
    __table_args__ = (
        UniqueConstraint('user_id', 'channel_id', name='uq_user_channel'),
    )
