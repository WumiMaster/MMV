"""
语音频道路由模块
处理语音频道的 WebSocket 信令
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ..config.database import get_db
from ..models.user import User
from ..models.channel import SubChannel, UserChannel
from ..services.auth_service import decode_token
from ..websocket_manager import ws_manager, voice_manager
import json

router = APIRouter(tags=["语音频道"])


@router.websocket("/ws/voice/{sub_channel_id}")
async def voice_websocket_endpoint(
    websocket: WebSocket,
    sub_channel_id: int,
    token: str = None
):
    """
    语音频道 WebSocket 端点
    处理 WebRTC 信令：offer、answer、ICE candidates

    连接方式：ws://localhost:8000/ws/voice/{sub_channel_id}?token=xxx
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

        # 查找子频道
        sub_channel = db.query(SubChannel).filter(SubChannel.id == sub_channel_id).first()
        if not sub_channel:
            await websocket.close(code=4004, reason="子频道不存在")
            return

        # 检查用户是否加入了该频道
        user_channel = db.query(UserChannel).filter(
            UserChannel.user_id == user.id,
            UserChannel.channel_id == sub_channel.channel_id
        ).first()
        if not user_channel:
            await websocket.close(code=4003, reason="未加入该频道")
            return

        # 接受连接
        await websocket.accept()

        # 加入语音房间
        user_info = {
            "user_id": user.id,
            "nickname": user.nickname,
            "avatar": user.avatar
        }
        peers = await voice_manager.join_voice_room(sub_channel_id, user.id, user_info, websocket)

        # 通知房间内其他用户有新人加入（通过语音 WebSocket）
        await voice_manager.broadcast_to_voice_room(sub_channel_id, {
            "type": "voice_user_joined",
            "sub_channel_id": sub_channel_id,
            "user": user_info
        }, exclude_user_id=user.id)

        # 发送房间内的其他用户给新加入的用户
        await websocket.send_text(json.dumps({
            "type": "voice_peers",
            "peers": peers
        }, ensure_ascii=False))

        # 监听信令消息
        try:
            while True:
                data = await websocket.receive_text()

                # 处理心跳
                if data == "ping":
                    await websocket.send_text("pong")
                    continue

                # 解析信令消息
                try:
                    message = json.loads(data)
                    msg_type = message.get("type")

                    if msg_type == "offer":
                        # 转发 offer 给目标用户（通过语音 WebSocket）
                        target_user_id = message.get("target_user_id")
                        target_ws = voice_manager.voice_connections.get(sub_channel_id, {}).get(target_user_id)
                        if target_ws:
                            try:
                                await target_ws.send_text(json.dumps({
                                    "type": "offer",
                                    "offer": message.get("offer"),
                                    "from_user_id": user.id
                                }, ensure_ascii=False))
                            except Exception as e:
                                print(f"转发 offer 失败: {e}")

                    elif msg_type == "answer":
                        # 转发 answer 给目标用户（通过语音 WebSocket）
                        target_user_id = message.get("target_user_id")
                        target_ws = voice_manager.voice_connections.get(sub_channel_id, {}).get(target_user_id)
                        if target_ws:
                            try:
                                await target_ws.send_text(json.dumps({
                                    "type": "answer",
                                    "answer": message.get("answer"),
                                    "from_user_id": user.id
                                }, ensure_ascii=False))
                            except Exception as e:
                                print(f"转发 answer 失败: {e}")

                    elif msg_type == "ice_candidate":
                        # 转发 ICE candidate 给目标用户（通过语音 WebSocket）
                        target_user_id = message.get("target_user_id")
                        target_ws = voice_manager.voice_connections.get(sub_channel_id, {}).get(target_user_id)
                        if target_ws:
                            try:
                                await target_ws.send_text(json.dumps({
                                    "type": "ice_candidate",
                                    "candidate": message.get("candidate"),
                                    "from_user_id": user.id
                                }, ensure_ascii=False))
                            except Exception as e:
                                print(f"转发 ice_candidate 失败: {e}")

                    elif msg_type == "mute":
                        # 闭麦状态变更
                        voice_manager.update_user_status(sub_channel_id, user.id, {
                            "is_muted": message.get("is_muted", False)
                        })
                        # 广播给房间内其他用户（通过语音 WebSocket）
                        await voice_manager.broadcast_to_voice_room(sub_channel_id, {
                            "type": "voice_user_muted",
                            "sub_channel_id": sub_channel_id,
                            "user_id": user.id,
                            "is_muted": message.get("is_muted", False)
                        }, exclude_user_id=user.id)

                    elif msg_type == "deafen":
                        # 本地静音状态变更
                        voice_manager.update_user_status(sub_channel_id, user.id, {
                            "is_deafened": message.get("is_deafened", False)
                        })
                        # 广播给房间内其他用户（通过语音 WebSocket）
                        await voice_manager.broadcast_to_voice_room(sub_channel_id, {
                            "type": "voice_user_deafened",
                            "sub_channel_id": sub_channel_id,
                            "user_id": user.id,
                            "is_deafened": message.get("is_deafened", False)
                        }, exclude_user_id=user.id)

                    elif msg_type == "speaking":
                        # 说话状态变更
                        voice_manager.update_user_status(sub_channel_id, user.id, {
                            "is_speaking": message.get("is_speaking", False)
                        })
                        # 广播给房间内其他用户（通过语音 WebSocket）
                        await voice_manager.broadcast_to_voice_room(sub_channel_id, {
                            "type": "voice_user_speaking",
                            "sub_channel_id": sub_channel_id,
                            "user_id": user.id,
                            "is_speaking": message.get("is_speaking", False)
                        }, exclude_user_id=user.id)

                except json.JSONDecodeError:
                    print(f"无效的 JSON 消息: {data}")

        except WebSocketDisconnect:
            # 先通知房间内其他用户有人离开（通过语音 WebSocket）
            await voice_manager.broadcast_to_voice_room(sub_channel_id, {
                "type": "voice_user_left",
                "sub_channel_id": sub_channel_id,
                "user_id": user.id
            }, exclude_user_id=user.id)

            # 然后离开语音房间
            await voice_manager.leave_voice_room(sub_channel_id, user.id)

    finally:
        db.close()


@router.get("/api/voice/{sub_channel_id}/users")
async def get_voice_users(
    sub_channel_id: int,
    db: Session = Depends(get_db)
):
    """
    获取语音房间内的用户列表
    """
    users = voice_manager.get_voice_room_users(sub_channel_id)
    return {"users": users}
