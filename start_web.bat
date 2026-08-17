@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   MiniMax Music 3 - 巴洛克音乐工房
echo   Baroque Web Workbench (port 7861)
echo ============================================
rem Windows 不支持 expandable_segments,保持默认分配器即可
.venv\Scripts\python.exe app\server.py
pause
