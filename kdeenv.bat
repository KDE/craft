@echo off
rem    this file sets some environment variables that are needed
rem    for finding programs and libraries etc.
rem    by Holger Schroeder <schroder@kde.org>
rem    by Patrick Spendrin <ps_ml@gmx.de>

rem    you should copy kdesettings-example.bat to ..\etc\kdesettings.bat
rem    and adapt it to your needs (see that file for more info)

rem    this file should contain all path settings - and provide thus an environment
rem    to build and run kde programs
rem    this file sources the kdesettings.bat file automatically

SETLOCAL ENABLEDELAYEDEXPANSION

:nextarg
if "%1" == "" goto :endargs
set EMERGE_ARGS=%1

shift
goto :endargs

:shiftarg
shift
goto :nextarg

:endargs


if not exist %~dp0..\etc\kdesettings.ini (
    echo "Please prepare a %~dp0..\etc\kdesettings.ini"
    goto :eof
)

rem load the python path from the kdesettings.ini
rem
FOR /F "tokens=1 delims=" %%A in ('powershell -ExecutionPolicy RemoteSigned %~dp0kdeenv.ps1 --get Paths PYTHONPATH') do SET _PYTHONPATH=%%A
set PATH=!_PYTHONPATH!;!PATH!
set _PYTHONPATH=

FOR /F "tokens=1 delims=" %%A in ('python %~dp0bin\EmergeSetupHelper.py --setup --mode bat') do (
    SET Z=%%A
    SET !Z!
)
set Z=


if "%EMERGE_ARGS%" == "" (
    %comspec% /e:on /K "cd /D %KDEROOT%"
    goto :eof
)
%comspec% /e:on /C %EMERGE_ARGS% %1 %2 %3 %4 %5 %6 %7 %8 %9

