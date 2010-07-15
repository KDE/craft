@echo off

rem This script sets the target enviroment to the actual one

set HOST_PATH=%PATH%
set HOST_INCLUDE=%INCLUDE%
set HOST_LIB=%LIB%
set PATH=%TARGET_PATH%
set INCLUDE=%TARGET_INCLUDE%
set LIB=%TARGET_LIB%
