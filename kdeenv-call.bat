@echo off

for /F "tokens=* USEBACKQ" %%F in (`powershell -ExecutionPolicy RemoteSigned %~dp0kdeenv.ps1 --get Paths Python`) do (
    set _PYTHONPATH=%%F
)
set PATH=%_PYTHONPATH%;%PATH%
set _PYTHONPATH=

rem Simulate a Unix eval here...
set rand=%random%
set filename="%temp%\kdeenv_%random%.cmd"
python %~dp0bin\CraftSetupHelper.py --setup --mode cmd > %filename%
call %filename%

del %filename%