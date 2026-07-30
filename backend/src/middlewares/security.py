"""
安全中间件
添加安全相关的HTTP头和请求限制
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    安全HTTP头中间件
    添加常见的安全响应头
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # 添加安全头
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 不添加 HSTS，因为开发环境使用 HTTP
        # 生产环境应该添加: Strict-Transport-Security

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    请求频率限制中间件
    基于IP地址限制请求频率
    """

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # 获取客户端IP
        client_ip = request.client.host if request.client else "unknown"

        # 清理过期的请求记录
        current_time = time.time()
        self.requests[client_ip] = [
            t for t in self.requests[client_ip]
            if current_time - t < 60
        ]

        # 检查请求频率
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return Response(
                content='{"detail": "请求过于频繁，请稍后再试"}',
                status_code=429,
                media_type="application/json"
            )

        # 记录请求
        self.requests[client_ip].append(current_time)

        # 处理请求
        response = await call_next(request)

        # 添加速率限制头
        remaining = self.requests_per_minute - len(self.requests[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))

        return response
