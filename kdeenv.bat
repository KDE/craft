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

rem On win64 we have both %ProgramFiles% and %ProgramFiles(x86)%,
rem but the latter is actually used for most of the paths (e.g. for Visual Studio)
rem so we create a wrapper to use the right variable on both win32 and win64
rem 
rem NB: note that we can't use the usual if () else () there because
rem     of a bug in the batch script parser which makes the parenthesis from
rem     the variable being interpreted as the closing block parenthesis...
if defined ProgramFiles(x86) set PROGRAM_FILES=%ProgramFiles(x86)%
if not defined PROGRAM_FILES set PROGRAM_FILES=%ProgramFiles%

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

rem nb: we need delayed var expansion (!VAR!) to avoid confusing the batch script parser
rem in case the expanded vars contain parentheses (same problem as above)

set PATH=%KDEROOT%%SUBDIR%\bin;!PATH!
set KDEDIRS=%KDEROOT%%SUBDIR%
set QT_PLUGIN_PATH=%KDEROOT%%SUBDIR%\plugins;%KDEROOT%%SUBDIR%\lib\kde4\plugins
set XDG_DATA_DIRS=%KDEROOT%%SUBDIR%\share

rem for emerge
set PATH=%KDEROOT%\emerge\bin;!PATH!

rem for dev-utils
set PATH=%KDEROOT%\dev-utils\bin;!PATH!

rem for old packages
set PATH=%KDEROOT%\bin;!PATH!

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
        set PATH=%KDEROOT%\mingw64\bin;!PATH!
        goto :eof
    ) 
    if %EMERGE_ARCHITECTURE% == arm-wince ( 
        set PATH=%KDEROOT%\cegcc-arm-wince\arm-mingw32ce\bin;%KDEROOT%\cegcc-arm-wince\libexec\gcc\arm-mingw32ce\4.4.0;!PATH!
        goto :eof
    ) 
    set PATH=%KDEROOT%\mingw\bin;!PATH!
    goto :eof

:path-msvc
    rem MSVC extra setup
    if defined VSDIR (
        call "!VSDIR!\VC\vcvarsall.bat" %EMERGE_ARCHITECTURE%
    )
    if defined PSDKDIR (
        echo Using Platform SDK: !PSDKDIR!
        set PATH=!PSDKDIR!\bin;!PATH!
        set INCLUDE=!PSDKDIR!\Include;!INCLUDE!
        set LIB=!PSDKDIR!\Lib;!LIB!
    )
    
    if defined MSDXSDKDIR (
        call "!MSDXSDKDIR!\Utilities\bin\dx_setenv.cmd" %EMERGE_ARCHITECTURE%
    )

    if defined TARGET_SDKDIR (
        if exist "%TARGET_SDKDIR%" (
            echo Using Mobile SDK: !TARGET_SDKDIR!
            set TARGET_PATH=!VSDIR!\VC\ce\bin\x86_arm;!PATH!
            set TARGET_INCLUDE=!VSDIR!\VC\ce\include;!TARGET_SDKDIR!\include\%EMERGE_TARGET_ARCHITECTURE%;!TARGET_SDKDIR!\include;!VSDIR!\VC\ce\atlmfc\include
            set TARGET_LIB=!TARGET_SDKDIR!\lib\%EMERGE_TARGET_ARCHITECTURE%;!VSDIR!\VC\ce\lib\%EMERGE_TARGET_ARCHITECTURE%;!VSDIR!\VC\ce\atlmfc\lib\%EMERGE_TARGET_ARCHITECTURE%
        ) else (
            echo Couldn't find the SDK for target platform %EMERGE_TARGET_PLATFORM%-%EMERGE_TARGET_ARCHITECTURE% ^^! 
        )
    )

    goto :eof

