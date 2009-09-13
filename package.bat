@echo off
rem     this file sets some environment variables that are needed
rem     for finding programs and libraries etc.
rem     it should be used to run the package.py script
rem     to set up an automatic build, run this file whenever you need with the packagelist as single parameter
rem     by Patrick Spendrin <ps_ml@gmx.de>


call ..\etc\kdesettings.bat


rem     adapt this file to your needs
rem     set an smtp server from which you can send emails via authentication
rem set EMERGE_SERVER_SERVER=smtp.googlemail.com:587

rem     set the email address you want to send emails from
rem set EMERGE_SERVER_SENDER=winbuild@googlemail.com

rem     set the needed password for authenticating to the server
rem set EMERGE_SERVER_PASS=

rem     set the receivers list: for multiple email addresses, use a comma as separator
rem set EMERGE_SERVER_RECEIVERS=

rem     set the upload server
rem set EMERGE_SERVER_UPLOAD_SERVER=

rem     set the directory on the server
rem set EMERGE_SERVER_UPLOAD_DIR=

 



rem    the following do not need to be changed
set PATH=%KDEROOT%\bin;%PATH%
set KDEDIRS=%KDEROOT%
set QT_PLUGIN_PATH=%KDEROOT%\plugins
set XDG_DATA_DIRS=%KDEROOT%\share

rem for emerge
set PATH=%KDEROOT%\emerge\bin;%PATH%

rem for dev-utils
set PATH=%KDEROOT%\dev-utils\bin;%PATH%

rem for non-subdir packages
set PATH=%KDEROOT%\bin;%PATH%

if %KDECOMPILER% == mingw ( 
    call :path-mingw
) else ( 
    call :path-msvc 
)

rem give over the first argument which should contain the path to the packagelist file
rem this can be adjusted on the build machine
rem the packagelist file is a simple file containing lines of the following form:
rem     packagename,target,patchlevel
rem # at the beginning of a line is a comment
rem if the default target or patchlevel should be used, keep the space empty but keep the commata
python server/package.py %1
goto :eof

:path-mingw
    set PATH=%KDEROOT%\mingw\bin;%PATH%
    goto :eof

:path-msvc
    if defined PSDKDIR ( 
        set PATH=%PSDKDIR%\bin;%PATH%
        set INCLUDE=%PSDKDIR%\Include;%INCLUDE%
        set LIB=%PSDKDIR%\Lib;%LIB%
    )
    goto :eof
