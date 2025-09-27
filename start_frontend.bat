@echo off
echo 正在停止可能存在的服务器...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
echo 在 frontend/build 目录启动服务器...
cd /d "%~dp0frontend\build"
echo 当前目录: %CD%
echo 文件列表:
dir
echo.
echo 启动Python HTTP服务器...
python -m http.server 3000