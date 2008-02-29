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

set PATH=%KDEROOT%\emerge\bin;%PATH%
SET KDEWIN_DIR=%KDEROOT%
set XDG_DATA_DIRS=%KDEROOT%\share
if %KDECOMPILER% == mingw ( 
    call :path-mingw
) else ( 
    call :path-msvc 
)

if %directory_layout% == installer ( 
    call :path-installer
) else (
    call :path-traditional
)
cmd /e:on /K "cd %KDEROOT%"
goto :eof

:: installer layout: only one installation directory - which serves as installation root for all packages
:: its subfolder bin contains all the executables and should contain all dynamic libraries
:: putting the lib directory into the path shouldn't be needed, it is included though for convenience
:path-installer
    set PATH=%KDEROOT%\lib;%PATH%
    set PATH=%KDEROOT%\bin;%PATH%
    set KDEDIRS=%KDEROOT%
    goto :eof

:: traditional layout: depending on the categories, there exist subfolders in %KDEROOT%: gnuwin32 for the gnuwin32 packages, qt
:: for qt headers, libraries and of course
:path-traditional
    set PATH=%KDEROOT%\gnuwin32\bin;%PATH%
    set PATH=%KDEROOT%\subversion\bin;%PATH%
    set PATH=%KDEROOT%\qt\bin;%PATH%
    set PATH=%KDEROOT%\cmake\bin;%PATH%
    set PATH=%KDEROOT%\kdewin32\bin;%PATH%
    set PATH=%KDEROOT%\win32libs\bin;%PATH%
    set PATH=%KDEROOT%\kde\bin;%PATH%
    set PATH=%KDEROOT%\dbus\bin;%PATH%
    set PATH=%KDEROOT%\mc;%PATH%
    set PATH=%KDEROOT%\perl\bin;%PATH%
    set PATH=%KDEROOT%\strigi\bin;%PATH%
    set PATH=%KDEROOT%\kde\lib;%PATH%
    set PATH=%KDEROOT%\qt\lib;%PATH%
    set KDEDIRS=%KDEROOT%\emerge
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