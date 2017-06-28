@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
set CraftDeprecatedEntryScript="kdeenv.bat"
set PATH=%~dp0\bin;!PATH!

if "%1" == "" goto :endargs
powershell -NoProfile %~dp0\craftenv.ps1 %ComSpec% /C %*
goto :eof
:endargs
powershell -NoProfile %~dp0\craftenv.ps1 %ComSpec%
