"""
FastAPI 应用入口
配置跨域、路由、静态文件等
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from .config.database import engine, SessionLocal, Base
from .routes import auth, admin, admin_channels, channels, messages, websocket, voice
from .models.user import User
from .models.channel import Channel, SubChannel, UserChannel
from .models.message import Message
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio

load_dotenv()


# 消息清理任务
async def cleanup_old_messages():
    """定期清理超过留存天数的旧消息"""
    while True:
        try:
            db = SessionLocal()
            try:
                # 获取所有频道
                channels = db.query(Channel).all()
                for channel in channels:
                    retention_days = channel.message_retention_days or 30
                    cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

                    # 获取该频道的所有子频道
                    sub_channel_ids = [sc.id for sc in channel.sub_channels]

                    if sub_channel_ids:
                        # 删除超过留存时间的消息
                        deleted_count = db.query(Message).filter(
                            Message.sub_channel_id.in_(sub_channel_ids),
                            Message.created_at < cutoff_date
                        ).delete(synchronize_session=False)

                        if deleted_count > 0:
                            print(f"频道 '{channel.name}' 清理了 {deleted_count} 条过期消息")

                db.commit()
            finally:
                db.close()
        except Exception as e:
            print(f"消息清理任务出错: {e}")

        # 每小时执行一次
        await asyncio.sleep(3600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("启动消息清理后台任务...")
    cleanup_task = asyncio.create_task(cleanup_old_messages())

    yield

    # 关闭时
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title="喵喵语音 API",
    description="浏览器端精简版 Discord 后端服务",
    version="1.0.0",
    lifespan=lifespan
)

# 跨域配置
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5174")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173", "http://localhost:5174",
        "https://localhost:5173", "https://localhost:5174",
        "http://172.31.238.60:5174", "https://172.31.238.60:5174",
        "http://192.168.137.1:5174", "https://192.168.137.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录（头像等）
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 注册路由
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(admin_channels.router)
app.include_router(channels.router)
app.include_router(messages.router)
app.include_router(websocket.router)
app.include_router(voice.router)


@app.get("/")
async def root():
    """健康检查接口"""
    return {
        "message": "喵喵语音 API 服务运行中",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}
