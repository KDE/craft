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

:nextarg
if "%1" == "" goto :endargs


shift
goto :endargs

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


if not exist %~dp0..\etc\kdesettings.ini (
    echo "Please prepare a %~dp0..\etc\kdesettings.ini"
    goto :eof
)

rem handle drive substitution
rem
FOR /F "tokens=1 delims=" %%A in ('powershell %~dp0kdeenv.ps1 --get Paths PYTHONPATH') do SET _PYTHONPATH=%%A
set PATH=!_PYTHONPATH!;!PATH!
set _PYTHONPATH=""

FOR /F "tokens=1 delims=" %%A in ('python %~dp0bin\emerge_setup_helper.py --getenv --mode bat') do (
    SET Z=%%A
    SET !Z!
)



rem print pathes 

python "%~dp0bin\emerge_setup_helper.py" --print-banner


rem ####### Visual Studio Settings #######
rem Here you can adjust the path to your Visual Studio or Intel Composer installation if needed
rem This is used to set up the build environment automatically
if %KDECOMPILER% == msvc2010 set VSDIR=%VS100COMNTOOLS%
if %KDECOMPILER% == msvc2012 set VSDIR=%VS110COMNTOOLS%
if %KDECOMPILER% == msvc2013 set VSDIR=%VS120COMNTOOLS%
if %KDECOMPILER% == intel set INTELDIR=%PROGRAM_FILES%\Intel\Composer XE




if "%KDECOMPILER%" == "intel" (
    call :path-intel
) else (
    call :path-msvc 
)


%comspec% /e:on /K "cd /D %KDEROOT%"
goto :eof

:path-msvc
    rem MSVC extra setup
    if defined VSDIR (
        if "%EMERGE_ARCHITECTURE%" == "x86" (
            call "!VSDIR!\..\..\VC\vcvarsall.bat" x86
        ) else (
            call "!VSDIR!\..\..\VC\vcvarsall.bat" amd64
        )        
    )

:path-intel
    if defined INTELDIR (
        if "%EMERGE_ARCHITECTURE%" == "x86" (
            call "!INTELDIR!\bin\compilervars.bat" ia32 %INTEL_VSSHELL%
        ) else (
            if "%EMERGE_ARCHITECTURE%" == "x64" (
                call "!INTELDIR!\bin\compilervars.bat" intel64 %INTEL_VSSHELL%
            )
        )
    )


