@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   MiniMax Music 3 - 巴洛克音乐工房
echo   Baroque Web Workbench (port 7861)
echo ============================================
.venv\Scripts\python.exe app\server.py
pause
