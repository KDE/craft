@echo off


rem ####### Python Settings #######

rem Here you set the path to your Python installation,
rem so that Python will be found, when Python scripts are be executed.
rem By setting this here, you don't have to change the global environment
rem settings of Windows. In case python is distributed with emerge the
rem following setting is not used.
if "%EMERGE_PYTHON_PATH%" == "" (
    set EMERGE_PYTHON_PATH="C:\python34"
)


