"""
WebSocket 路由模块
处理实时消息推送
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ..config.database import get_db
from ..models.user import User
from ..models.channel import UserChannel
from ..services.auth_service import decode_token
from ..websocket_manager import ws_manager
import json

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/{channel_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    channel_id: int,
    token: str = None
):
    """
    WebSocket 端点
    用户通过此连接加入频道房间，接收实时消息

    连接方式：ws://localhost:8000/ws/{channel_id}?token=xxx
    """
    # 验证 token
    if not token:
        await websocket.close(code=4001, reason="缺少认证token")
        return

    payload = decode_token(token)
    if not payload:
        await websocket.close(code=4001, reason="无效的token")
        return

    username = payload.get("sub")
    if not username:
        await websocket.close(code=4001, reason="无效的token内容")
        return

    # 获取数据库会话
    db = next(get_db())
    try:
        # 查找用户
        user = db.query(User).filter(User.username == username).first()
        if not user:
            await websocket.close(code=4001, reason="用户不存在")
            return

        # 检查用户是否加入了该频道
        user_channel = db.query(UserChannel).filter(
            UserChannel.user_id == user.id,
            UserChannel.channel_id == channel_id
        ).first()
        if not user_channel:
            await websocket.close(code=4003, reason="未加入该频道")
            return

        # 连接到频道房间
        await ws_manager.connect(websocket, user.id, channel_id)

        # 通知房间内其他用户有新人加入
        await ws_manager.broadcast_to_channel(channel_id, {
            "type": "user_joined",
            "user_id": user.id,
            "nickname": user.nickname,
            "avatar": user.avatar
        }, exclude_websocket=websocket)

        # 监听消息
        try:
            while True:
                data = await websocket.receive_text()
                # 客户端发送的心跳消息
                if data == "ping":
                    await websocket.send_text("pong")
        except WebSocketDisconnect:
            # 用户断开连接
            await ws_manager.disconnect(websocket)
            # 通知房间内其他用户有人离开
            await ws_manager.broadcast_to_channel(channel_id, {
                "type": "user_left",
                "user_id": user.id,
                "nickname": user.nickname
            })
    finally:
        db.close()
