"""
WebSocket 连接管理器
管理频道房间和用户连接，实现消息广播
"""

from fastapi import WebSocket
from typing import Dict, Set, List
import json


class WebSocketManager:
    """
    WebSocket 连接管理器
    管理所有用户的 WebSocket 连接，按频道房间分组
    """

    def __init__(self):
        # 房间 -> 连接集合 {channel_id: {websocket1, websocket2, ...}}
        self.rooms: Dict[int, Set[WebSocket]] = {}
        # 连接 -> 用户信息 {websocket: {"user_id": int, "channel_id": int}}
        self.connections: Dict[WebSocket, dict] = {}

    async def connect(self, websocket: WebSocket, user_id: int, channel_id: int):
        """
        用户连接到频道房间
        """
        await websocket.accept()

        # 初始化房间
        if channel_id not in self.rooms:
            self.rooms[channel_id] = set()

        # 添加连接到房间
        self.rooms[channel_id].add(websocket)
        self.connections[websocket] = {
            "user_id": user_id,
            "channel_id": channel_id
        }

        print(f"用户 {user_id} 连接到频道 {channel_id}，当前房间人数：{len(self.rooms[channel_id])}")

    async def disconnect(self, websocket: WebSocket):
        """
        用户断开连接
        """
        if websocket in self.connections:
            info = self.connections[websocket]
            user_id = info["user_id"]
            channel_id = info["channel_id"]

            # 从房间移除
            if channel_id in self.rooms:
                self.rooms[channel_id].discard(websocket)
                # 如果房间为空，删除房间
                if not self.rooms[channel_id]:
                    del self.rooms[channel_id]

            # 删除连接记录
            del self.connections[websocket]

            print(f"用户 {user_id} 断开频道 {channel_id} 连接")

    async def broadcast_to_channel(self, channel_id: int, message: dict, exclude_websocket: WebSocket = None):
        """
        向频道房间广播消息
        exclude_websocket: 排除的连接（通常是发送者自己）
        """
        if channel_id not in self.rooms:
            return

        message_json = json.dumps(message, ensure_ascii=False)
        disconnected = set()

        for websocket in self.rooms[channel_id]:
            if websocket == exclude_websocket:
                continue
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                # 发送失败，标记为断开
                disconnected.add(websocket)
                print(f"发送消息失败: {e}")

        # 清理断开的连接
        for ws in disconnected:
            await self.disconnect(ws)

    async def send_to_user(self, user_id: int, message: dict):
        """
        向特定用户发送消息
        """
        message_json = json.dumps(message, ensure_ascii=False)
        for websocket, info in self.connections.items():
            if info["user_id"] == user_id:
                try:
                    await websocket.send_text(message_json)
                except Exception:
                    pass

    def get_room_users(self, channel_id: int) -> list:
        """
        获取房间内的用户ID列表
        """
        if channel_id not in self.rooms:
            return []

        user_ids = []
        for websocket in self.rooms[channel_id]:
            if websocket in self.connections:
                user_ids.append(self.connections[websocket]["user_id"])
        return user_ids

    def get_user_websocket(self, user_id: int) -> WebSocket:
        """
        获取用户的 WebSocket 连接
        """
        for websocket, info in self.connections.items():
            if info["user_id"] == user_id:
                return websocket
        return None


class VoiceChannelManager:
    """
    语音频道管理器
    管理语音房间和用户的音频状态
    """

    def __init__(self):
        # 语音房间 {sub_channel_id: {user_id: {"is_muted": bool, "is_deafened": bool}}}
        self.voice_rooms: Dict[int, Dict[int, dict]] = {}
        # 语音 WebSocket 连接 {sub_channel_id: {user_id: websocket}}
        self.voice_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def join_voice_room(self, sub_channel_id: int, user_id: int, user_info: dict, websocket: WebSocket = None):
        """
        用户加入语音房间
        """
        if sub_channel_id not in self.voice_rooms:
            self.voice_rooms[sub_channel_id] = {}
        if sub_channel_id not in self.voice_connections:
            self.voice_connections[sub_channel_id] = {}

        self.voice_rooms[sub_channel_id][user_id] = {
            "user_id": user_id,
            "nickname": user_info.get("nickname", ""),
            "avatar": user_info.get("avatar"),
            "is_muted": False,  # 闭麦
            "is_deafened": False,  # 本地静音
            "is_speaking": False  # 是否正在说话
        }

        # 保存 WebSocket 连接
        if websocket:
            self.voice_connections[sub_channel_id][user_id] = websocket

        print(f"用户 {user_id} 加入语音房间 {sub_channel_id}")

        # 返回房间内其他用户列表（用于建立 P2P 连接）
        return self.get_room_peers(sub_channel_id, user_id)

    async def leave_voice_room(self, sub_channel_id: int, user_id: int):
        """
        用户离开语音房间
        """
        if sub_channel_id in self.voice_rooms:
            if user_id in self.voice_rooms[sub_channel_id]:
                del self.voice_rooms[sub_channel_id][user_id]
                print(f"用户 {user_id} 离开语音房间 {sub_channel_id}")

                # 如果房间为空，删除房间
                if not self.voice_rooms[sub_channel_id]:
                    del self.voice_rooms[sub_channel_id]

        # 移除 WebSocket 连接
        if sub_channel_id in self.voice_connections:
            if user_id in self.voice_connections[sub_channel_id]:
                del self.voice_connections[sub_channel_id][user_id]
                if not self.voice_connections[sub_channel_id]:
                    del self.voice_connections[sub_channel_id]

    async def broadcast_to_voice_room(self, sub_channel_id: int, message: dict, exclude_user_id: int = None):
        """
        向语音房间内的所有用户广播消息
        """
        if sub_channel_id not in self.voice_connections:
            return

        message_json = json.dumps(message, ensure_ascii=False)
        disconnected_users = []

        for user_id, websocket in self.voice_connections[sub_channel_id].items():
            if user_id == exclude_user_id:
                continue
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                disconnected_users.append(user_id)
                print(f"发送语音消息失败: {e}")

        # 清理断开的连接
        for user_id in disconnected_users:
            await self.leave_voice_room(sub_channel_id, user_id)

    def get_room_peers(self, sub_channel_id: int, exclude_user_id: int = None) -> List[dict]:
        """
        获取房间内的其他用户列表
        """
        if sub_channel_id not in self.voice_rooms:
            return []

        peers = []
        for user_id, info in self.voice_rooms[sub_channel_id].items():
            if user_id != exclude_user_id:
                peers.append(info)
        return peers

    def get_voice_room_users(self, sub_channel_id: int) -> List[dict]:
        """
        获取语音房间内的所有用户
        """
        if sub_channel_id not in self.voice_rooms:
            return []
        return list(self.voice_rooms[sub_channel_id].values())

    def update_user_status(self, sub_channel_id: int, user_id: int, status: dict):
        """
        更新用户的音频状态
        """
        if sub_channel_id in self.voice_rooms:
            if user_id in self.voice_rooms[sub_channel_id]:
                self.voice_rooms[sub_channel_id][user_id].update(status)

    def is_user_in_voice(self, sub_channel_id: int, user_id: int) -> bool:
        """
        检查用户是否在语音房间中
        """
        return (sub_channel_id in self.voice_rooms and
                user_id in self.voice_rooms[sub_channel_id])


# 全局实例
ws_manager = WebSocketManager()
voice_manager = VoiceChannelManager()
