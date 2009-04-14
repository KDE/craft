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

call ..\etc\kdesettings.bat

set PATH=%KDEROOT%\lib;%PATH%
set PATH=%KDEROOT%\bin;%PATH%
set KDEDIRS=%KDEROOT%
set QT_PLUGIN_PATH=%KDEROOT%\plugins
set PATH=%KDEROOT%\emerge\bin;%KDEROOT%\dev-utils\bin;%PATH%
SET KDEWIN_DIR=%KDEROOT%
set XDG_DATA_DIRS=%KDEROOT%\share

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
