@echo off
setlocal
set "SCRIPT=%~dp0bootstrap.ps1"
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" %*
endlocal
