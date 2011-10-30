@echo off
cd %~dp0
SET KDEROOT=%~dp0

SET PATH=%KDEROOT%\bin;%PATH%
SET HOME=%KDEROOT%\home
SET KDEHOME=%HOME%

SET APPLICATION=

IF NOT "%1" == "" (
    SET APPLICATION=%1
    SHIFT
)

IF EXIST %KDEROOT%\firstrun GOTO :INSTALL
IF NOT EXIST %KDEROOT%\home GOTO :INSTALL

:RUN

IF "%APPLICATION%" == "" (
    CALL bin\amarok.exe
) ELSE (
    CALL %APPLICATION% %1 %2 %3 %4 %5 %6 %7 %8 %9
)

GOTO :EOF


:INSTALL
echo install
IF NOT EXIST %KDEROOT%\home MKDIR %KDEROOT%\home
IF NOT EXIST %KDEROOT%\firstrun DEL firstrun



echo *******************************************************************************
echo package: %0
echo *******************************************************************************

SET quitnow=False
::for %%i in ( kioslave.exe kded4.exe ) DO (
::    tasklist /NH /FI "IMAGENAME eq %%i" | find "%%i" > "Nul" && (
::        echo error: found %%i running. please kill this process!
::        SET quitnow=True
::    )
::)

if %quitnow% equ True (
    echo error: one or more programs are running that shouldn't run.
    echo        please close them before restarting this script
    goto :eof
)

if not `"bin\update-mime-database.exe --help"` equ "" (
    bin\update-mime-database "%CD%\share\mime"
) else (
    echo error: update-mime-database wasn't found.
    echo        please check for correct installation
)

if not `"bin\kbuildsycoca4.exe --help"` equ "" (
    bin\kbuildsycoca4 --noincremental
) else (
    echo error: kbuildsycoca4 wasn't found.
    echo        please check for correct installation
)

echo HM

GOTO :RUN