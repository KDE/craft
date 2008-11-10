@echo off

echo *******************************************************************************
echo package: %0
echo *******************************************************************************

set quitnow=False
::for %%i in ( kioslave.exe kded4.exe ) DO (
::    tasklist /NH /FI "IMAGENAME eq %%i" | find "%%i" > "Nul" && (
::        echo error: found %%i running. please kill this process!
::        set quitnow=True
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