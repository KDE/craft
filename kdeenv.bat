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

call ..\etc\kdesettings.bat %1

if "%1" == "debug" ( 
set SUBDIR=\debug
) 
if "%1" == "relwithdebinfo" ( 
set SUBDIR=\relwithdebinfo
)
if "%1" == "release" ( 
set SUBDIR=\release
)
if "%1" == "" (
    if "%EMERGE_MERGE_ROOT_WITH_BUILD_TYPE%" == "True" (
        set SUBDIR=\relwithdebinfo
    ) else (
        set SUBDIR=
    )
)

set PATH=%KDEROOT%%SUBDIR%\bin;%PATH%
set KDEDIRS=%KDEROOT%%SUBDIR%
set QT_PLUGIN_PATH=%KDEROOT%%SUBDIR%\plugins
set XDG_DATA_DIRS=%KDEROOT%%SUBDIR%\share

rem for emerge
set PATH=%KDEROOT%\emerge\bin;%PATH%

rem for dev-utils
set PATH=%KDEROOT%\dev-utils\bin;%PATH%

rem for old packages
set PATH=%KDEROOT%\bin;%PATH%

if %KDECOMPILER% == mingw ( 
    call :path-mingw
) else ( 
    call :path-msvc 
)

%comspec% /e:on /K "cd %KDEROOT%"
goto :eof

:path-mingw
    set PATH=%KDEROOT%\mingw\bin;%PATH%
    goto :eof

:path-msvc
    if defined PSDKDIR ( 
        goto :path-psdk
    )
    goto :eof

:path-psdk
    set PATH=%PSDKDIR%\bin;%PATH%
    set INCLUDE=%PSDKDIR%\Include;%INCLUDE%
    set LIB=%PSDKDIR%\Lib;%LIB%
    goto :eof
