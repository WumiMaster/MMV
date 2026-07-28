"""
管理员路由模块
处理用户管理相关的请求（CRUD）
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from ..config.database import get_db
from ..models.user import User, UserRole
from ..services.auth_service import hash_password
from ..middlewares.auth import get_current_admin
import os
import uuid

router = APIRouter(prefix="/api/admin", tags=["管理员"])

# 上传文件目录
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==================== 请求/响应数据结构 ====================

class CreateUserRequest(BaseModel):
    """创建用户请求"""
    username: str
    password: str
    nickname: str


class UpdateUserRequest(BaseModel):
    """更新用户请求"""
    nickname: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    nickname: str
    avatar: Optional[str]
    role: str

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """用户列表响应"""
    users: List[UserResponse]
    total: int
    page: int
    page_size: int


# ==================== 路由处理 ====================

@router.get("/users", response_model=UserListResponse)
async def get_users(
    page: int = 1,
    page_size: int = 20,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取用户列表（分页）
    需要管理员权限
    """
    # 计算偏移量
    offset = (page - 1) * page_size

    # 查询总数
    total = db.query(User).count()

    # 查询用户列表
    users = db.query(User).order_by(User.id).offset(offset).limit(page_size).all()

    return UserListResponse(
        users=users,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/users", response_model=UserResponse)
async def create_user(
    request: CreateUserRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    创建新用户
    需要管理员权限
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
        role=UserRole.USER  # 管理员创建的默认为普通用户
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UpdateUserRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    更新用户信息
    需要管理员权限
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 更新字段
    if request.nickname is not None:
        user.nickname = request.nickname
    if request.password is not None:
        user.hashed_password = hash_password(request.password)
    if request.role is not None:
        if request.role not in ["user", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的角色值，只能是 user 或 admin"
            )
        user.role = UserRole(request.role)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    删除用户
    需要管理员权限
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 不允许删除自己
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除当前登录的管理员账号"
        )

    db.delete(user)
    db.commit()

    return {"message": "用户已删除"}


@router.post("/users/{user_id}/avatar")
async def upload_user_avatar(
    user_id: int,
    file: UploadFile = File(...),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    为指定用户上传头像
    需要管理员权限
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持 JPG、PNG、GIF、WebP 格式的图片"
        )

    # 验证文件大小（最大 5MB）
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
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
    user.avatar = avatar_url
    db.commit()

    return {"avatar": avatar_url}
