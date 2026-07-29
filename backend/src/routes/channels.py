"""
用户频道路由模块
处理用户加入/退出频道、获取频道信息等
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from ..config.database import get_db
from ..models.user import User
from ..models.channel import Channel, SubChannel, UserChannel
from ..middlewares.auth import get_current_user

router = APIRouter(prefix="/api/channels", tags=["用户频道"])


# ==================== 请求/响应数据结构 ====================

class JoinChannelRequest(BaseModel):
    """加入频道请求"""
    channel_id: str  # 频道ID（不是数据库主键）


class SubChannelResponse(BaseModel):
    """子频道响应"""
    id: int
    name: str
    type: str
    sort_order: int

    class Config:
        from_attributes = True


class ChannelDetailResponse(BaseModel):
    """频道详情响应"""
    id: int
    name: str
    channel_id: str
    description: Optional[str]
    member_count: int
    sub_channels: List[SubChannelResponse]

    class Config:
        from_attributes = True


class MyChannelResponse(BaseModel):
    """我加入的频道响应"""
    id: int
    name: str
    channel_id: str
    description: Optional[str]
    avatar: Optional[str]
    member_count: int
    sub_channel_count: int

    class Config:
        from_attributes = True


# ==================== 用户频道接口 ====================

@router.post("/join", response_model=ChannelDetailResponse)
async def join_channel(
    request: JoinChannelRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    通过频道ID加入频道
    """
    # 查找频道
    channel = db.query(Channel).filter(Channel.channel_id == request.channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在，请检查频道ID"
        )

    # 检查是否已加入
    existing = db.query(UserChannel).filter(
        UserChannel.user_id == current_user.id,
        UserChannel.channel_id == channel.id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="你已经加入了该频道"
        )

    # 加入频道
    user_channel = UserChannel(
        user_id=current_user.id,
        channel_id=channel.id
    )
    db.add(user_channel)
    db.commit()

    # 返回频道详情
    sub_channels = db.query(SubChannel).filter(
        SubChannel.channel_id == channel.id
    ).order_by(SubChannel.sort_order).all()

    return ChannelDetailResponse(
        id=channel.id,
        name=channel.name,
        channel_id=channel.channel_id,
        description=channel.description,
        member_count=len(channel.members),
        sub_channels=[SubChannelResponse(
            id=sc.id,
            name=sc.name,
            type=sc.type,
            sort_order=sc.sort_order
        ) for sc in sub_channels]
    )


@router.get("/my", response_model=List[MyChannelResponse])
async def get_my_channels(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取我加入的频道列表
    """
    # 查询用户加入的频道
    user_channels = db.query(UserChannel).filter(
        UserChannel.user_id == current_user.id
    ).all()

    channels = []
    for uc in user_channels:
        channel = uc.channel
        channels.append(MyChannelResponse(
            id=channel.id,
            name=channel.name,
            channel_id=channel.channel_id,
            description=channel.description,
            avatar=channel.avatar,
            member_count=len(channel.members),
            sub_channel_count=len(channel.sub_channels)
        ))

    return channels


@router.get("/{channel_id}", response_model=ChannelDetailResponse)
async def get_channel_detail(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取频道详情（需已加入）
    """
    # 检查是否已加入
    user_channel = db.query(UserChannel).filter(
        UserChannel.user_id == current_user.id,
        UserChannel.channel_id == channel_id
    ).first()
    if not user_channel:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="你尚未加入该频道"
        )

    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    sub_channels = db.query(SubChannel).filter(
        SubChannel.channel_id == channel.id
    ).order_by(SubChannel.sort_order).all()

    return ChannelDetailResponse(
        id=channel.id,
        name=channel.name,
        channel_id=channel.channel_id,
        description=channel.description,
        member_count=len(channel.members),
        sub_channels=[SubChannelResponse(
            id=sc.id,
            name=sc.name,
            type=sc.type,
            sort_order=sc.sort_order
        ) for sc in sub_channels]
    )


@router.delete("/{channel_id}/leave")
async def leave_channel(
    channel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    退出频道
    """
    user_channel = db.query(UserChannel).filter(
        UserChannel.user_id == current_user.id,
        UserChannel.channel_id == channel_id
    ).first()
    if not user_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="你尚未加入该频道"
        )

    db.delete(user_channel)
    db.commit()

    return {"message": "已退出频道"}
