@echo off

:: �������ԱȨ��
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

echo ����װ�ɹ����밴������رձ�����
pause >nul