@echo off
chcp 65001 >nul
title 🍌 Nano Banana Studio
echo.
echo  🍌  启动 Nano Banana Studio...
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    where python3 >nul 2>&1
    if %errorlevel% neq 0 (
        echo  ❌  未找到 Python，请先安装 Python 3：
        echo      https://www.python.org/downloads/
        pause
        exit /b 1
    )
    python3 server.py
) else (
    python server.py
)

pause
