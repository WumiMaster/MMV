"""
数据库种子脚本
用于初始化数据库并创建默认管理员账号和测试数据

使用方式：
  cd backend
  python seed.py
"""

import sys
import os

# 确保能导入 src 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.database import engine, SessionLocal, Base
from src.models.user import User, UserRole
from src.models.channel import Channel, SubChannel, UserChannel
from src.services.auth_service import hash_password


def seed():
    """初始化数据库并创建默认数据"""

    # 创建所有数据表
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成。")

    db = SessionLocal()
    try:
        # 检查是否已存在管理员
        existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if existing_admin:
            print(f"管理员账号已存在：{existing_admin.username}")
            print("跳过创建。如需重新创建，请先删除 data.db 文件。")
            return

        # 创建默认管理员
        admin = User(
            username="admin",
            hashed_password=hash_password("admin123"),
            nickname="超级管理员",
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        # 创建测试用户
        test_user = User(
            username="testuser",
            hashed_password=hash_password("test123"),
            nickname="测试用户",
            role=UserRole.USER
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        # 创建测试频道
        test_channel = Channel(
            name="测试频道",
            channel_id="test001",
            description="这是一个测试频道",
            message_retention_days=30,
            creator_id=admin.id
        )
        db.add(test_channel)
        db.commit()
        db.refresh(test_channel)

        # 创建文字子频道
        text_channel = SubChannel(
            channel_id=test_channel.id,
            name="综合讨论",
            type="text",
            sort_order=1
        )
        db.add(text_channel)

        # 创建语音子频道（阶段3才会用到）
        voice_channel = SubChannel(
            channel_id=test_channel.id,
            name="语音聊天室",
            type="voice",
            sort_order=2
        )
        db.add(voice_channel)
        db.commit()

        # 将管理员和测试用户加入频道
        admin_member = UserChannel(user_id=admin.id, channel_id=test_channel.id)
        test_member = UserChannel(user_id=test_user.id, channel_id=test_channel.id)
        db.add(admin_member)
        db.add(test_member)
        db.commit()

        print("=" * 40)
        print("默认数据创建成功！")
        print("=" * 40)
        print("\n管理员账号：")
        print(f"  用户名：admin")
        print(f"  密  码：admin123")
        print(f"  昵  称：超级管理员")
        print("\n测试用户账号：")
        print(f"  用户名：testuser")
        print(f"  密  码：test123")
        print(f"  昵  称：测试用户")
        print("\n测试频道：")
        print(f"  频道ID：test001")
        print(f"  频道名：测试频道")
        print(f"  子频道：综合讨论（文字）、语音聊天室（语音）")
        print("=" * 40)
        print("请登录后及时修改密码！")

    except Exception as e:
        db.rollback()
        print(f"创建失败：{e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
