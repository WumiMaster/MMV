@echo off
echo ================================
echo 喵喵语音 HTTPS 启动脚本
echo ================================

REM 检查证书文件
if not exist "cert.pem" (
    echo 错误：找不到 cert.pem 证书文件
    echo 请先运行 mkcert 生成证书：
    echo mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 172.31.238.60
    pause
    exit /b 1
)

if not exist "key.pem" (
    echo 错误：找不到 key.pem 证书文件
    pause
    exit /b 1
)

echo 证书文件已找到 ✓
echo.

echo [1/2] 启动后端 (HTTPS)...
start "Backend HTTPS" cmd /k "cd backend && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --ssl-keyfile ../key.pem --ssl-certfile ../cert.pem"

timeout /t 2 /nobreak > nul

echo [2/2] 启动前端 (HTTPS)...
start "Frontend HTTPS" cmd /k "cd frontend && npm run dev"

echo.
echo ================================
echo 启动完成！
echo.
echo 本机访问：https://localhost:5174
echo 手机访问：https://172.31.238.60:5174
echo.
echo 注意：首次访问手机浏览器会提示证书不信任
echo 点击"高级" -> "继续访问"即可
echo ================================
pause
