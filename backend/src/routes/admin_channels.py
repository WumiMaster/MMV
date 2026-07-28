"""
管理员频道路由模块
处理频道和子频道的增删改查
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import uuid
from ..config.database import get_db
from ..models.user import User
from ..models.channel import Channel, SubChannel
from ..middlewares.auth import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["管理员-频道管理"])


# ==================== 请求/响应数据结构 ====================

class CreateChannelRequest(BaseModel):
    """创建频道请求"""
    name: str
    channel_id: Optional[str] = None  # 不填则自动生成
    description: Optional[str] = None
    message_retention_days: int = 30


class UpdateChannelRequest(BaseModel):
    """更新频道请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    message_retention_days: Optional[int] = None


class ChannelResponse(BaseModel):
    """频道响应"""
    id: int
    name: str
    channel_id: str
    description: Optional[str]
    message_retention_days: int
    creator_id: int
    created_at: str
    member_count: int = 0
    sub_channel_count: int = 0

    class Config:
        from_attributes = True


class ChannelListResponse(BaseModel):
    """频道列表响应"""
    channels: List[ChannelResponse]
    total: int
    page: int
    page_size: int


class CreateSubChannelRequest(BaseModel):
    """创建子频道请求"""
    name: str
    type: str  # text 或 voice
    sort_order: int = 0


class UpdateSubChannelRequest(BaseModel):
    """更新子频道请求"""
    name: Optional[str] = None
    sort_order: Optional[int] = None


class SubChannelResponse(BaseModel):
    """子频道响应"""
    id: int
    channel_id: int
    name: str
    type: str
    sort_order: int
    created_at: str

    class Config:
        from_attributes = True


# ==================== 频道管理接口 ====================

@router.post("/channels", response_model=ChannelResponse)
async def create_channel(
    request: CreateChannelRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    创建新频道
    需要管理员权限
    """
    # 生成频道ID（如果未提供）
    channel_id = request.channel_id if request.channel_id else str(uuid.uuid4())[:8]

    # 检查频道ID是否已存在
    existing = db.query(Channel).filter(Channel.channel_id == channel_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="频道ID已存在，请使用其他ID"
        )

    # 创建频道
    channel = Channel(
        name=request.name,
        channel_id=channel_id,
        description=request.description,
        message_retention_days=request.message_retention_days,
        creator_id=current_admin.id
    )
    db.add(channel)
    db.commit()
    db.refresh(channel)

    return ChannelResponse(
        id=channel.id,
        name=channel.name,
        channel_id=channel.channel_id,
        description=channel.description,
        message_retention_days=channel.message_retention_days,
        creator_id=channel.creator_id,
        created_at=str(channel.created_at),
        member_count=0,
        sub_channel_count=0
    )


@router.get("/channels", response_model=ChannelListResponse)
async def get_channels(
    page: int = 1,
    page_size: int = 20,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取频道列表（分页）
    需要管理员权限
    """
    offset = (page - 1) * page_size
    total = db.query(Channel).count()
    channels = db.query(Channel).order_by(Channel.id.desc()).offset(offset).limit(page_size).all()

    # 构建响应，包含成员数和子频道数
    channel_list = []
    for ch in channels:
        member_count = len(ch.members)
        sub_channel_count = len(ch.sub_channels)
        channel_list.append(ChannelResponse(
            id=ch.id,
            name=ch.name,
            channel_id=ch.channel_id,
            description=ch.description,
            message_retention_days=ch.message_retention_days,
            creator_id=ch.creator_id,
            created_at=str(ch.created_at),
            member_count=member_count,
            sub_channel_count=sub_channel_count
        ))

    return ChannelListResponse(
        channels=channel_list,
        total=total,
        page=page,
        page_size=page_size
    )


@router.put("/channels/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: int,
    request: UpdateChannelRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    更新频道信息
    需要管理员权限
    """
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    if request.name is not None:
        channel.name = request.name
    if request.description is not None:
        channel.description = request.description
    if request.message_retention_days is not None:
        channel.message_retention_days = request.message_retention_days

    db.commit()
    db.refresh(channel)

    member_count = len(channel.members)
    sub_channel_count = len(channel.sub_channels)

    return ChannelResponse(
        id=channel.id,
        name=channel.name,
        channel_id=channel.channel_id,
        description=channel.description,
        message_retention_days=channel.message_retention_days,
        creator_id=channel.creator_id,
        created_at=str(channel.created_at),
        member_count=member_count,
        sub_channel_count=sub_channel_count
    )


@router.delete("/channels/{channel_id}")
async def delete_channel(
    channel_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    删除频道
    需要管理员权限
    """
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    db.delete(channel)
    db.commit()

    return {"message": "频道已删除"}


# ==================== 子频道管理接口 ====================

@router.post("/channels/{channel_id}/sub-channels", response_model=SubChannelResponse)
async def create_sub_channel(
    channel_id: int,
    request: CreateSubChannelRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    创建子频道
    需要管理员权限
    """
    # 检查频道是否存在
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    # 验证类型
    if request.type not in ["text", "voice"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="子频道类型必须是 text 或 voice"
        )

    sub_channel = SubChannel(
        channel_id=channel_id,
        name=request.name,
        type=request.type,
        sort_order=request.sort_order
    )
    db.add(sub_channel)
    db.commit()
    db.refresh(sub_channel)

    return SubChannelResponse(
        id=sub_channel.id,
        channel_id=sub_channel.channel_id,
        name=sub_channel.name,
        type=sub_channel.type,
        sort_order=sub_channel.sort_order,
        created_at=str(sub_channel.created_at)
    )


@router.put("/sub-channels/{sub_channel_id}", response_model=SubChannelResponse)
async def update_sub_channel(
    sub_channel_id: int,
    request: UpdateSubChannelRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    更新子频道
    需要管理员权限
    """
    sub_channel = db.query(SubChannel).filter(SubChannel.id == sub_channel_id).first()
    if not sub_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="子频道不存在"
        )

    if request.name is not None:
        sub_channel.name = request.name
    if request.sort_order is not None:
        sub_channel.sort_order = request.sort_order

    db.commit()
    db.refresh(sub_channel)

    return SubChannelResponse(
        id=sub_channel.id,
        channel_id=sub_channel.channel_id,
        name=sub_channel.name,
        type=sub_channel.type,
        sort_order=sub_channel.sort_order,
        created_at=str(sub_channel.created_at)
    )


@router.delete("/sub-channels/{sub_channel_id}")
async def delete_sub_channel(
    sub_channel_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    删除子频道
    需要管理员权限
    """
    sub_channel = db.query(SubChannel).filter(SubChannel.id == sub_channel_id).first()
    if not sub_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="子频道不存在"
        )

    db.delete(sub_channel)
    db.commit()

    return {"message": "子频道已删除"}
