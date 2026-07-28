"""
认证路由模块
处理登录、注册、获取当前用户信息等请求
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..config.database import get_db
from ..models.user import User, UserRole
from ..services.auth_service import (
    hash_password,
    authenticate_user,
    create_access_token
)
from ..middlewares.auth import get_current_user, get_current_admin
import os
import uuid
import shutil

router = APIRouter(prefix="/api/auth", tags=["认证"])

# 上传文件目录
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==================== 请求/响应数据结构 ====================

class RegisterRequest(BaseModel):
    """注册请求"""
    username: str
    password: str
    nickname: str


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"
    id: int
    role: str
    username: str
    nickname: str
    avatar: Optional[str] = None


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    nickname: str
    avatar: Optional[str]
    role: str

    class Config:
        from_attributes = True


# ==================== 路由处理 ====================

@router.post("/register", response_model=UserResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    用户注册接口
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 创建新用户
    new_user = User(
        username=request.username,
        hashed_password=hash_password(request.password),
        nickname=request.nickname,
        role=UserRole.USER  # 默认为普通用户
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录接口
    返回 JWT Token 和用户信息
    """
    user = authenticate_user(db, request.username, request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 生成 Token
    access_token = create_access_token(data={"sub": user.username})

    return TokenResponse(
        access_token=access_token,
        id=user.id,
        role=user.role.value,
        username=user.username,
        nickname=user.nickname,
        avatar=user.avatar
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户信息
    """
    return current_user


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传用户头像
    """
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持 JPG、PNG、GIF、WebP 格式的图片"
        )

    # 验证文件大小（最大 5MB）
    file_size = 0
    contents = await file.read()
    file_size = len(contents)
    if file_size > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小不能超过 5MB"
        )

    # 生成唯一文件名
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # 保存文件
    with open(filepath, "wb") as f:
        f.write(contents)

    # 更新用户头像路径
    avatar_url = f"/uploads/avatars/{filename}"
    current_user.avatar = avatar_url
    db.commit()

    return {"avatar": avatar_url}


class UpdateProfileRequest(BaseModel):
    """更新个人资料请求"""
    nickname: Optional[str] = None


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户个人资料
    """
    if request.nickname is not None:
        current_user.nickname = request.nickname

    db.commit()
    db.refresh(current_user)

    return current_user
