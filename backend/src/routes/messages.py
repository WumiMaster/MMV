"""
消息路由模块
处理消息发送、获取历史消息、图片上传
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
import os
import uuid
from ..config.database import get_db
from ..models.user import User
from ..models.channel import Channel, SubChannel, UserChannel
from ..models.message import Message
from ..middlewares.auth import get_current_user
from ..websocket_manager import ws_manager

router = APIRouter(prefix="/api", tags=["消息"])


# ==================== 配置 ====================

# 图片上传目录
UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 图片大小限制（10MB）
MAX_IMAGE_SIZE = 10 * 1024 * 1024

# 允许的图片类型
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]


# ==================== 请求/响应数据结构 ====================

class SendMessageRequest(BaseModel):
    """发送消息请求"""
    sub_channel_id: int
    content: Optional[str] = None  # 文字内容（可为空）
    image_url: Optional[str] = None  # 图片地址（可为空）


class MessageUserResponse(BaseModel):
    """消息用户信息"""
    id: int
    username: str
    nickname: str
    avatar: Optional[str]


class MessageResponse(BaseModel):
    """消息响应"""
    id: int
    sub_channel_id: int
    user: MessageUserResponse
    content: Optional[str]
    image_url: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    """消息列表响应"""
    messages: List[MessageResponse]
    total: int
    has_more: bool


# ==================== 消息接口 ====================

@router.post("/messages", response_model=MessageResponse)
async def send_message(
    request: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    发送消息到文字子频道
    """
    # 验证内容不为空
    if not request.content and not request.image_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="消息内容和图片不能同时为空"
        )

    # 查找子频道
    sub_channel = db.query(SubChannel).filter(SubChannel.id == request.sub_channel_id).first()
    if not sub_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="子频道不存在"
        )

    # 验证是文字子频道
    if sub_channel.type != "text":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能向文字子频道发送消息"
        )

    # 检查用户是否加入了该频道
    user_channel = db.query(UserChannel).filter(
        UserChannel.user_id == current_user.id,
        UserChannel.channel_id == sub_channel.channel_id
    ).first()
    if not user_channel:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="你尚未加入该频道"
        )

    # 创建消息
    message = Message(
        sub_channel_id=request.sub_channel_id,
        user_id=current_user.id,
        content=request.content,
        image_url=request.image_url
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    # 构建响应
    message_response = MessageResponse(
        id=message.id,
        sub_channel_id=message.sub_channel_id,
        user=MessageUserResponse(
            id=current_user.id,
            username=current_user.username,
            nickname=current_user.nickname,
            avatar=current_user.avatar
        ),
        content=message.content,
        image_url=message.image_url,
        created_at=message.created_at.replace(tzinfo=timezone.utc).isoformat() if message.created_at else datetime.now(timezone.utc).isoformat()
    )

    # 通过 WebSocket 广播消息到频道
    channel_id = sub_channel.channel_id
    await ws_manager.broadcast_to_channel(channel_id, {
        "type": "new_message",
        "message": {
            "id": message.id,
            "sub_channel_id": message.sub_channel_id,
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "nickname": current_user.nickname,
                "avatar": current_user.avatar
            },
            "content": message.content,
            "image_url": message.image_url,
            "created_at": message.created_at.isoformat() if message.created_at else None
        }
    })

    return message_response


@router.get("/messages/{sub_channel_id}", response_model=MessageListResponse)
async def get_messages(
    sub_channel_id: int,
    page: int = 1,
    page_size: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取子频道的历史消息（分页）
    最新的消息在前
    """
    # 查找子频道
    sub_channel = db.query(SubChannel).filter(SubChannel.id == sub_channel_id).first()
    if not sub_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="子频道不存在"
        )

    # 检查用户是否加入了该频道
    user_channel = db.query(UserChannel).filter(
        UserChannel.user_id == current_user.id,
        UserChannel.channel_id == sub_channel.channel_id
    ).first()
    if not user_channel:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="你尚未加入该频道"
        )

    # 查询消息总数
    total = db.query(Message).filter(Message.sub_channel_id == sub_channel_id).count()

    # 分页查询（最新的在前）
    offset = (page - 1) * page_size
    messages = db.query(Message).filter(
        Message.sub_channel_id == sub_channel_id
    ).order_by(desc(Message.created_at)).offset(offset).limit(page_size).all()

    # 构建响应
    message_list = []
    for msg in messages:
        user = msg.user
        message_list.append(MessageResponse(
            id=msg.id,
            sub_channel_id=msg.sub_channel_id,
            user=MessageUserResponse(
                id=user.id,
                username=user.username,
                nickname=user.nickname,
                avatar=user.avatar
            ),
            content=msg.content,
            image_url=msg.image_url,
            created_at=str(msg.created_at)
        ))

    return MessageListResponse(
        messages=message_list,
        total=total,
        has_more=(offset + page_size) < total
    )


@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传图片
    返回图片URL用于发送消息
    """
    # 验证文件类型
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持 JPG、PNG、GIF、WebP 格式的图片"
        )

    # 验证文件大小
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="图片大小不能超过 10MB"
        )

    # 生成唯一文件名
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # 保存文件
    with open(filepath, "wb") as f:
        f.write(contents)

    # 返回图片URL
    image_url = f"/uploads/images/{filename}"
    return {"image_url": image_url}
