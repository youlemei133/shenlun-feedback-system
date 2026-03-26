@echo off
chcp 65001 >nul
echo ========================================
echo   申论判官反馈系统 - 启动脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python 环境正常

echo.
echo [2/3] 检查依赖包...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo ❌ 错误：依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖包安装完成

echo.
echo [3/3] 启动服务...
echo.
echo ========================================
echo   服务已启动！
echo   主页面：http://localhost:5000
echo   管理后台：http://localhost:5000/admin
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

cd backend
python app.py

pause
