@echo off

:: 申请管理员权限
%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin

cd %~dp0

if not exist .venv\scripts\python.exe (
    python -m venv .venv 1>nul 2>nul
    if not exist .venv\scripts\python.exe (
        init\python.exe /passive /quiet TargetDir=%LocalAppData%\Programs\Python\Python3X-32 1>nul 2>nul
        %LocalAppData%\Programs\Python\Python3X-32\python -m venv .venv 1>nul 2>nul)
)

.venv\scripts\python.exe core\launch.py

echo 程序安装成功，请按任意键关闭本窗口
pause >nul