"""
输入验证工具
提供各种输入数据的验证函数
"""

import re
from typing import Optional


def validate_username(username: str) -> tuple[bool, str]:
    """
    验证用户名
    规则：3-20个字符，只能包含字母、数字、下划线
    """
    if not username:
        return False, "用户名不能为空"

    if len(username) < 3:
        return False, "用户名至少需要3个字符"

    if len(username) > 20:
        return False, "用户名不能超过20个字符"

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "用户名只能包含字母、数字和下划线"

    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    验证密码
    规则：6-50个字符
    """
    if not password:
        return False, "密码不能为空"

    if len(password) < 6:
        return False, "密码至少需要6个字符"

    if len(password) > 50:
        return False, "密码不能超过50个字符"

    return True, ""


def validate_nickname(nickname: str) -> tuple[bool, str]:
    """
    验证昵称
    规则：1-30个字符，不能包含特殊字符
    """
    if not nickname:
        return False, "昵称不能为空"

    if len(nickname) > 30:
        return False, "昵称不能超过30个字符"

    # 移除空白字符后检查
    stripped = nickname.strip()
    if len(stripped) == 0:
        return False, "昵称不能只包含空格"

    return True, ""


def validate_channel_name(name: str) -> tuple[bool, str]:
    """
    验证频道名称
    规则：1-50个字符
    """
    if not name:
        return False, "频道名称不能为空"

    if len(name) > 50:
        return False, "频道名称不能超过50个字符"

    stripped = name.strip()
    if len(stripped) == 0:
        return False, "频道名称不能只包含空格"

    return True, ""


def validate_channel_id(channel_id: str) -> tuple[bool, str]:
    """
    验证频道ID
    规则：3-30个字符，只能包含字母、数字、下划线、连字符
    """
    if not channel_id:
        return True, ""  # 频道ID可以为空（自动生成）

    if len(channel_id) < 3:
        return False, "频道ID至少需要3个字符"

    if len(channel_id) > 30:
        return False, "频道ID不能超过30个字符"

    if not re.match(r'^[a-zA-Z0-9_-]+$', channel_id):
        return False, "频道ID只能包含字母、数字、下划线和连字符"

    return True, ""


def validate_message_content(content: Optional[str]) -> tuple[bool, str]:
    """
    验证消息内容
    规则：最多5000个字符
    """
    if content is None:
        return True, ""

    if len(content) > 5000:
        return False, "消息内容不能超过5000个字符"

    return True, ""


def sanitize_input(text: str) -> str:
    """
    清理输入文本
    移除潜在的危险字符
    """
    if not text:
        return ""

    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)

    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """
    验证文件扩展名
    """
    if not filename:
        return False

    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    return f'.{ext}' in allowed_extensions or ext in [e.lstrip('.') for e in allowed_extensions]
