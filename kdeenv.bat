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

rem use local python installation if present
rem when in kderoot/emerge
if exist %~dp0python (
    set PYTHONPATH=%~dp0python
)

rem in case we are in kderoot 
if exist %~dp0emerge\python (
    set PYTHONPATH=%~dp0emerge\python
)

rem call kdesettings.bat 
rem in case we are in kderoot/emerge 
if exist %~dp0..\etc\kdesettings.bat (
call %~dp0..\etc\kdesettings.bat %BUILDTYPE%
)

rem in case we are in kderoot 
if exist %~dp0etc\kdesettings.bat (
call %~dp0etc\kdesettings.bat %BUILDTYPE%
)

rem handle drive substitution
rem
rem check for unversioned kdesettings.bat,
rem in that case drive substition already took place
if NOT "%EMERGE_SETTINGS_VERSION%" == "" (
    if !EMERGE_USE_SHORT_PATH! == 1 (
        set ROOT_SET=FALSE
        set SVN_SET=FALSE
        set DOWNLOAD_SET=FALSE
        set GIT_SET=FALSE
        rem Check if drives are already set up correctly
        FOR /F "tokens=1,2,3* delims= " %%i in ('subst') DO (
            if /I "%%i" == "!EMERGE_ROOT_DRIVE!\:" (
                if /I "%%k" == "!KDEROOT!" (
                    set ROOT_SET=TRUE
                )
            )
            if /I "%%i" == "!EMERGE_SVN_DRIVE!\:" (
                if /I "%%k" == "!KDESVNDIR!" (
                    set SVN_SET=TRUE
                )
            )
            if /I "%%i" == "!EMERGE_DOWNLOAD_DRIVE!\:" (
                if /I "%%k" == "!DOWNLOADDIR!" (
                    set DOWNLOAD_SET=TRUE
                )
            )
            if /I "%%i" == "!EMERGE_GIT_DRIVE!\:" (
                if /I "%%k" == "!KDEGITDIR!" (
                    set GIT_SET=TRUE
                )
            )
        )
        if NOT "!ROOT_SET!"=="TRUE" (
            if exist !EMERGE_ROOT_DRIVE!\NUL subst !EMERGE_ROOT_DRIVE! /D
            subst !EMERGE_ROOT_DRIVE! !KDEROOT!
        )
        if NOT "!DOWNLOAD_SET!"=="TRUE" (
            if not exist !DOWNLOADDIR!\NUL mkdir !DOWNLOADDIR!
            if exist !EMERGE_DOWNLOAD_DRIVE!\NUL subst !EMERGE_DOWNLOAD_DRIVE! /D
            subst !EMERGE_DOWNLOAD_DRIVE! !DOWNLOADDIR!
        )
        if NOT "!SVN_SET!"=="TRUE" (
            if not exist !KDESVNDIR!\NUL mkdir !KDESVNDIR!
            if exist !EMERGE_SVN_DRIVE!\NUL subst !EMERGE_SVN_DRIVE! /D
            subst !EMERGE_SVN_DRIVE! !KDESVNDIR!
        )
        if NOT "!GIT_SET!" == "TRUE" (
            if not exist !KDEGITDIR!\NUL mkdir !KDEGITDIR!
            if exist !EMERGE_GIT_DRIVE!\NUL subst !EMERGE_GIT_DRIVE! /D
            subst !EMERGE_GIT_DRIVE! !KDEGITDIR!
         )
        set KDEROOT=!EMERGE_ROOT_DRIVE!\
        set KDESVNDIR=!EMERGE_SVN_DRIVE!\
        set DOWNLOADDIR=!EMERGE_DOWNLOAD_DRIVE!\
        set KDEGITDIR=!EMERGE_GIT_DRIVE!\
        !EMERGE_ROOT_DRIVE!
    )
)

rem print pathes 
if NOT "%EMERGE_SETTINGS_VERSION%" == "" (
    echo KDEROOT     : %KDEROOT%
    echo KDECOMPILER : %KDECOMPILER%
    echo KDESVNDIR   : %KDESVNDIR%
    echo KDEGITDIR   : %KDEGITDIR%
    echo PYTHONPATH  : %PYTHONPATH%
    echo DOWNLOADDIR : %DOWNLOADDIR%
)

rem handle multiple merge roots
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

rem for python
if NOT "!PYTHONPATH!" == "" ( 
   set PATH=!PYTHONPATH!;!PATH!
)

if "%EMERGE_USE_CCACHE%" == "True" (
    echo EMERGE_USE_CCACHE is active to use it "set EMERGE_MAKE_PROGRAM=jom /E" or "set EMERGE_MAKE_PROGRAM=mingw32-make -e"
    set CCACHE_DIR=%KDEROOT%\build\CCACHE
    set CXX=ccache g++
    set CC=ccache gcc
)

if "%KDECOMPILER%" == "mingw" ( 
    call :path-mingw
) else (
    if "%KDECOMPILER%" == "mingw4" ( 
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

