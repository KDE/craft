@echo off

rem Here you set the base directory under which the whole KDE
rem subsystem will live.
set KDEROOT=c:\kderoot

rem Here you set the compiler to be used.
rem * mingw4   - use the mingw gcc compiler (recommended)
rem * mingw    - use the mingw gcc compiler (gcc Version 3.4.5 - 
rem               please only use this option if you are exactly 
rem               sure about the consequences)
rem * msvc2008 - use the Microsoft Visual C++ 2008 compiler
rem * msvc2010 - use the Microsoft Visual C++ 2010 compiler (not completly tested) 
set KDECOMPILER=mingw4

rem Here you can set the architecure for which packages are build. 
rem Currently x86 (32bit), x64 (64) and arm (wince) are supported
rem 
rem               x86  x64  arm-wince
rem  mingw4        x    x       x[1] 
rem  mingw         x   ---     ---
rem  msvc2005      x   ---     ---  
rem  msvc2008      x   ---     ---
rem 
rem [1] by dev-utils/cegcc-arm-wince package
rem 
set EMERGE_ARCHITECTURE=x86
rem set EMERGE_ARCHITECTURE=x64

rem substitute pathes by drives (set to 1 to activate)
set EMERGE_USE_SHORT_PATH=0
set EMERGE_ROOT_DRIVE=r:
set EMERGE_SVN_DRIVE=s:
set EMERGE_DOWNLOAD_DRIVE=t:

rem The following variables are used for cross-compiling to Windows Mobile / WinCE
rem when uncommented, the proper toolchain is set up for the specified target OS and architecture.
rem EMERGE_TARGET_PLATFORM currently supports :
rem * WM50 - Windows Mobile 5.0 PocketPC (based on WinCE 5.01)
rem * WM60 - Windows Mobile 6.0 Professional (based on WinCE 5.02)
rem * WM65 - Windows Mobile 6.5 Professional (based on WinCE 5.02)
rem EMERGE_TARGET_ARCHITECTURE currently supports :
rem * ARMV4I (all platforms)
rem set EMERGE_TARGET_PLATFORM=WM60
rem set EMERGE_TARGET_ARCHITECTURE=ARMV4I

rem Here you set the path to your Python installation,
rem so that Python will be found, when Python scripts are be executed.
rem By setting this here, you don't have to change the global environment
rem settings of Windows. In case python is distributed with emerge the 
rem following setting is not used. 
set PYTHONPATH="%PROGRAM_FILES%\python26"

rem Here you set the path to msys if you want to compile
rem automake-based projects (only needed for some internal packages).
set MSYSDIR=%KDEROOT%\msys

rem Here you can adjust the path to your Visual Studio installation if needed
rem This is used to set up the build environment automatically
if %KDECOMPILER% == msvc2008 set VSDIR=%PROGRAM_FILES%\Microsoft Visual Studio 9
if %KDECOMPILER% == msvc2010 set VSDIR=%PROGRAM_FILES%\Microsoft Visual Studio 10

rem Here you can adjust the path to the Windows Mobile SDK installation
rem This is used to set up the cross-compilation environment automatically
if "%EMERGE_TARGET_PLATFORM%" == "WM50" set TARGET_SDKDIR=%PROGRAM_FILES%\Windows Mobile 5.0 SDK R2\PocketPC
if "%EMERGE_TARGET_PLATFORM%" == "WM60" set TARGET_SDKDIR=%PROGRAM_FILES%\Windows Mobile 6 Professional SDK\PocketPC
if "%EMERGE_TARGET_PLATFORM%" == "WM65" set TARGET_SDKDIR=%PROGRAM_FILES%\Windows Mobile 6 Professional SDK\PocketPC

rem Here you can set a specific platform SDK to use with the Visual Studio toolchain
rem Normally this is not needed as a default platform SDK is set by the build environment script
rem set PSDKDIR=%PROGRAM_FILES%\Microsoft SDKs\Windows\v6.0A

rem Here you can set the path to your Microsoft DirectX SDK installation
rem This is not needed if you use MinGW or won't use the directx backend for Phonon
rem set MSDXSDKDIR=%PROGRAM_FILES%\Microsoft DirectX SDK (August 2009)


rem proxy settings - in case a proxy is required uncomment the following variables 
rem set EMERGE_PROXY_HOST=
rem set EMERGE_PROXY_PORT=8080
rem set EMERGE_PROXY_USERNAME=
rem set EMERGE_PROXY_PASSWORD=

rem Here you can set if emerge should not try to download files in passive mode
rem set EMERGE_NO_PASSIVE_FTP=True

rem Here you change the download directory.
rem If you want, so you can share the same download directory between
rem mingw and msvc.
set DOWNLOADDIR=%KDEROOT%\download

rem Here you can tell the emerge tool in which dir you want to save the
rem SVN checkout of KDE source code. If you have SVN account registered 
rem within the KDE project, you can also set KDESVNUSERNAME and change 
rem KDESVNSERVER from svn://anonsvn.kde.org to https://svn.kde.org or 
rem svn+ssh://username@svn.kde.org, so that you can directly commit 
rem your changes from the emerge's SVN checkout. In case you use svn+ssh, 
rem also run 'plink username@svn.kde.org' after executing kdeenv.bat once
rem to accept the fingerprint of the server or svn will hang forever when
rem trying to download from the server.
set KDESVNDIR=%KDEROOT%\svn
set KDESVNSERVER=svn://anonsvn.kde.org
set KDESVNUSERNAME=username

rem Non kde svn repository checkouts will be placed below %DOWNLOADDIR%/svn-src/<package>
rem By default the emerge svn module supports only single branch svn checkouts.
rem With this option emerge assumes that the svn repository have the svn standard layout 
rem and will create related subdirectories for trunk, branches and tags below the above 
rem mentioned root directory. 
rem set EMERGE_SVN_STDLAYOUT=1

rem Here you can tell the emerge tool password for the SVN access
rem if you have SVN account registered within the KDE project.
rem For security reasons you should better log in to the KDE server by hand
rem using the command line Subversion 'svn' command: enter the username
rem and password at the first login, e.g. when you checkout the emerge
rem directory. The Subversion client will then remember the password so it
rem does not have to be written down here.
rem set KDESVNPASSWORD=password

rem If you use svn+ssh, you will need a ssh-agent equaivalent for managing
rem the authorization. Pageant is provided by the Putty project, get it at 
rem http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
rem and make sure that plink is in your PATH and Pageant is configured
rem (you need to import your key)
set SVN_SSH=plink 

rem With this option set to 1 emerge checks out each git repository branch into a 
rem separate subdirectory (see git clone --mirror at git clone  --shared --local).
rem Without this option changing the branch will overwrite previous checkouts.
rem Note: Changing the value invalidates available checkouts of related packages 
rem and requires a remove of the complete source dir.
rem set EMERGE_GIT_MULTIBRANCH=1

rem Setting up variables for git, not needed by emerge but preventing trouble with corrupted git pushes
set GIT_SSH=plink
set HOME=%USERPROFILE%
rem set GIT_AUTHOR_NAME=authorname
rem set GIT_AUTHOR_EMAIL=email
rem set GIT_COMMITTER_NAME=username
rem set GIT_COMMITTER_EMAIL=email

rem Here you can set type of the emerge build. 
rem There are two standard build types: Debug and Release.
rem Both are used if no EMERGE_BUILDTYPE is set.
rem There is a third extra buildtype called RelWithDebInfo, which is
rem release (optimized) build but containing debugging information.
rem You can override the build type at the commandline using
rem the '--buildtype=[BuildType]' option. The build type which is set here
rem will not override the buildtype in .py package files.
if "%1" == "debug" (
set EMERGE_BUILDTYPE=Debug
)
if "%1" == "relwithdebinfo" (
set EMERGE_BUILDTYPE=RelWithDebInfo
)
if "%1" == "release" (
set EMERGE_BUILDTYPE=Release
)
if "%1" == "" (
set EMERGE_BUILDTYPE=RelWithDebInfo
)

rem override specific emerge options 
rem currently only a subset of options (from bin\options.py) are setable by 
rem this environment variable because of a not full implemented option parser. 
rem  Options:
rem    * cmake.useIDE=1
rem    * cmake.openIDE=1
rem and see bin\options.py:Options::readFromEnv() for the current state
rem set EMERGE_OPTIONS=

rem If you want to have verbose output, uncomment the following option
rem and set it to positive integer for verbose output and to 0
rem or disable it for normal output. Currently the highest verbosity level
rem is 3 (equal to 'emerge -v -v -v'). level 0 equals 'emerge -q'
set EMERGE_VERBOSE=1

rem Enable this option if you want to have shorter build times, and less
rem disk usage. It will then avoid copying source code files of the KDE
rem svn repository. To disable, set EMERGE_NOCOPY=False.
set EMERGE_NOCOPY=True

rem Enable the following option to not remove a package before installing it.
rem This is insecure because the package might miss important files which will persist
rem in an older version.
rem set EMERGE_NOREMOVE=True

rem By default emerge will merge all package into KDEROOT. By setting the following 
rem option to true, the package will be installed into a subdir of KDEROOT. 
rem The directory is named like the lower cased build type 
rem When using this option you can run emerge/kdeenv.bat with the build mode type 
rem parameter (release, releasedebug or debug) to have different shells for each 
rem build type. 
rem set EMERGE_MERGE_ROOT_WITH_BUILD_TYPE=True

rem If you want to build all packages with buildTests option, enable
rem this option. Applies only to the cmake based packages.
rem set EMERGE_BUILDTESTS=True

rem This option only applies if you want to make packages. It sets
rem the output directory where your generated packages should be stored.
rem set EMERGE_PKGDSTDIR=%KDEROOT%\tmp

rem This option can be used to override the default make program
rem change the value to the path of the executable you want to use instead.
rem set EMERGE_MAKE_PROGRAM=%KDEROOT%\dev-utils\bin\jom.exe

rem This option can be used to set the default category for packages with the same name
rem that are contained in multiple categories; This is especially useful if you want
rem to build e.g. from the 4.3 branch: simply set the variable to kde-4.3 then
rem for all other packages this option doesn't have any effect
rem set EMERGE_DEFAULTCATEGORY=kde-4.3

rem This option can be used to set a directory where build logs are saved
rem instead of being printed to the console. Logging information is appended to
rem existing logs.
rem set EMERGE_LOG_DIR=%KDEROOT%\buildlogs

rem This option can be used to integrate packages from other portage directories
rem or override the default packages. The default directory can be overridden by
rem not including it in this list. If you do not set this option emerge will take
rem the current portage directory instead.
rem set EMERGE_PORTAGE_ROOT=C:\test\portage;%KDEROOT%\emerge\portage

rem This option can be used to build only source packages and don't use binary packages
rem it is needed for mingw-w32, mingw-w64 and wince builds, but works everywhere
rem set EMERGE_SOURCEONLY=True
rem No editing should be necessary below this line (in an ideal world)
rem ##################################################################

rem handle drive substitution
if %EMERGE_USE_SHORT_PATH% == 1 (
    subst %EMERGE_ROOT_DRIVE% /D
    subst %EMERGE_SVN_DRIVE% /D
    subst %EMERGE_DOWNLOAD_DRIVE% /D

    mkdir %DOWNLOADDIR% 2>NUL
    mkdir %KDESVNDIR% 2>NUL
    
    subst %EMERGE_ROOT_DRIVE% %KDEROOT%
    subst %EMERGE_SVN_DRIVE% %KDESVNDIR%
    subst %EMERGE_DOWNLOAD_DRIVE% %DOWNLOADDIR%
    set KDEROOT=%EMERGE_ROOT_DRIVE%\
    set KDESVNDIR=%EMERGE_SVN_DRIVE%\
    set DOWNLOADDIR=%EMERGE_DOWNLOAD_DRIVE%\
    %EMERGE_ROOT_DRIVE%
)

rem use local python installation if present
if exist %KDEROOT%\emerge\python (
    set PYTHONPATH=%KDEROOT%\emerge\python
) else (
    if %PYTHONPATH% == "" ( 
       echo Couldn't find local python installation - please set PYTHONPATH in %KDEROOT%\etc\kdesettings.bat ! 
    )
)

if NOT %PYTHONPATH% == "" ( 
    set PATH=%PYTHONPATH%;%PATH%
)

echo kdesettings.bat executed
echo KDEROOT     : %KDEROOT%
echo KDECOMPILER : %KDECOMPILER%
echo KDESVNDIR   : %KDESVNDIR%
echo PYTHONPATH  : %PYTHONPATH%
echo DOWNLOADDIR : %DOWNLOADDIR%

