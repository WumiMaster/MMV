"""
消息数据模型
存储文字子频道中的消息
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base


class Message(Base):
    """
    消息表
    存储文字子频道中的所有消息（文字和图片）
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sub_channel_id = Column(Integer, ForeignKey("sub_channels.id", ondelete="CASCADE"), nullable=False, comment="子频道ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="发送者ID")
    content = Column(Text, nullable=True, comment="文字内容（可为空）")
    image_url = Column(String(500), nullable=True, comment="图片地址（可为空）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="发送时间")

    # 关联关系
    sub_channel = relationship("SubChannel", backref="messages")
    user = relationship("User", backref="messages", passive_deletes=True)
