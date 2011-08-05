@echo off
rem     this file sets some environment variables that are needed
rem     for finding programs and libraries etc.
rem     it should be used to run the package.py script
rem     to set up an automatic build, run this file whenever you need with the packagelist as single parameter
rem     by Patrick Spendrin <ps_ml@gmx.de>

cd %~dp0
set EMERGE_WAIT_FOR_APPLICATION=True
call %~dp0\kdeenv.bat python %~dp0\server\package.py %1
timeout /T 60