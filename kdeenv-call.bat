@echo off

rem Add Python to PATH
for /F "tokens=* USEBACKQ" %%F in (`powershell -ExecutionPolicy RemoteSigned %~dp0kdeenv.ps1 --get Paths Python`) do (
    set _PYTHONPATH=%%F
)
set PATH=%_PYTHONPATH%;%PATH%
set _PYTHONPATH=

rem Setup compiler env, etc.
rem Note: Simulating a Unix eval here to eval the output of the setup helper script
set rand=%random%
set filename="%temp%\kdeenv_%random%.cmd"
python %~dp0bin\CraftSetupHelper.py --setup --mode cmd > %filename%
call %filename%

rem Add the script's dir to PATH (for craft.bat)
set PATH=%~dp0bin;%PATH%

del %filename%