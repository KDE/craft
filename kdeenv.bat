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

set BUILDTYPE=
set APPLICATION=

:nextarg
if "%1" == "" goto :endargs

if "%1" == "debug" goto :setbuildtype
if "%1" == "release" goto :setbuildtype
if "%1" == "relwithdebinfo" goto :setbuildtype

set APPLICATION=%1
shift
goto :endargs

:setbuildtype
set BUILDTYPE=%1

:shiftarg
shift
goto :nextarg

:endargs

if exist ..\etc\kdesettings.bat (
call ..\etc\kdesettings.bat %BUILDTYPE%
)

if exist etc\kdesettings.bat (
call etc\kdesettings.bat %BUILDTYPE%
)

set SUBDIR=
if "%BUILDTYPE%" == "" (
	if "%EMERGE_MERGE_ROOT_WITH_BUILD_TYPE%" == "True" (
		set SUBDIR=\%EMERGE_BUILDTYPE%
	)
) else (
	set SUBDIR=\%EMERGE_BUILDTYPE%
)

set PATH=%KDEROOT%%SUBDIR%\bin;%PATH%
set KDEDIRS=%KDEROOT%%SUBDIR%
set QT_PLUGIN_PATH=%KDEROOT%%SUBDIR%\plugins;%KDEROOT%%SUBDIR%\lib\kde4\plugins
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
    if %KDECOMPILER% == mingw4 ( 
        call :path-mingw
    ) else ( 
        call :path-msvc 
    )
)

if "%APPLICATION%" == "" (
	%comspec% /e:on /K "cd %KDEROOT%"
) else (
	start %APPLICATION% %1 %2 %3 %4 %5 %6 %7 %8 %9
)
goto :eof

:path-mingw
    if %EMERGE_ARCHITECTURE% == x64 ( 
        set PATH=%KDEROOT%\mingw64\bin;%PATH%
    ) else (
        set PATH=%KDEROOT%\mingw\bin;%PATH%
    )
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
