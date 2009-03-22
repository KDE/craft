@echo off
rem Here you set the base directory under which the whole KDE
rem subsystem will live.
set KDEROOT=c:\kderoot

rem Here you set the compiler to be used.
rem * mingw - use the mingw gcc compiler (recommended)
rem * msvc2005 - use the Microsoft Visual C++ 2005 compiler
rem * msvc2008 - use the Microsoft Visual C++ 2008 compiler
set KDECOMPILER=mingw

rem Here you set the path to your Python installation,
rem so that Python will be found, when Python scripts are be executed.
rem By setting this here, you don't have to change the global environment
rem settings of Windows.
set PYTHONPATH=%PROGRAMFILES%\python25

rem Here you set the path to msys if you want to compile
rem automake-based projects (only needed for some internal packages).
set MSYSDIR=%KDEROOT%\msys

rem Here you set the path to your platform SDK installation.
rem This path will be automatically included then.
set PSDKDIR=%PROGRAMFILES%\Microsoft Platform SDK for Windows Server 2003 R2

rem Here you set the path to your Microsoft DirectX SDK installation
rem This is not needed if you use MinGW
set MSDXSDKDIR=%PROGRAMFILES%\Microsoft DirectX SDK (June 2008)
call "%MSDXSDKDIR%\Utilities\bin\dx_setenv.cmd" x86

rem Here you set the location of the vcvarsall.bat file that adds
rem Visual C++ environment variables into the build environment.
rem if you are not building on x86 change that to something appropriate.
set VSDIR=%PROGRAMFILES%\Microsoft Visual Studio 8
call "%VSDIR%\VC\vcvarsall.bat" x86

rem Here you change the download directory.
rem If you want, so you can share the same download directory between
rem mingw and msvc.
set DOWNLOADDIR=%KDEROOT%\download

rem Here you can tell the emerge tool in which dir you want to save the
rem SVN checkout of KDE source code. If you have SVN account registered 
rem within the KDE project, you can also set KDESVNUSERNAME and change 
rem KDESVNSERVER from svn://anonsvn.kde.org to https://svn.kde.org or 
rem svn+ssh://username@svn.kde.org, so that rem you can directly commit 
rem your changes from the emerge's SVN checkout. In case you use svn+ssh, 
rem also run plink username@svn.kde.org after executing kdeenv.bat or
rem svn will hang forever
set KDESVNDIR=%KDEROOT%\svn
set KDESVNSERVER=svn://anonsvn.kde.org
set KDESVNUSERNAME=username

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

rem If you want to use emerge.py together with the kdewin-installer,
rem you should set the value of directory_layout to 'installer'. 
rem If you leave it unset or set it to 'traditional' you get the category
rem sublayout. 
rem Note: it is not recommended anymore to use the traditional layout.
set directory_layout=installer

rem Here you can set type of the emerge build. 
rem There are two standard build types: Debug and Release.
rem Both are used if no EMERGE_BUILDTYPE is set.
rem There is a third extra buildtype called RelWithDebInfo, which is
rem release (optimized) build but containing debugging information.
rem You can override the build type at the commandline using
rem the '--buildtype=[BuildType]' option. The build type which is set here
rem will not override the buildtype in .py package files.
set EMERGE_BUILDTYPE=RelWithDebInfo

rem If you want to have verbose output, uncomment the following option
rem and set it to positive integer for verbose output and to 0
rem or disable it for normal output. Currently the highest verbosity level
rem is 3 (equal to 'emerge -v -v -v'). level 0 equals 'emerge -q'
set EMERGE_VERBOSE=1

rem Enable this option if you want to have shorter build times, and less
rem disk usage. It will then avoid copying source code files of the KDE
rem svn repository. The disadvantage is that you cannot make packages when
rem this option is set. To disable, set EMERGE_NOCOPY=False.
set EMERGE_NOCOPY=True

rem If you want to build all packages with buildTests option, enable
rem this option. Applies only to the cmake based packages.
rem set EMERGE_BUILDTESTS=True

rem This option only applies if you want to make packages. It sets
rem the output directory where your generated packages should be stored.
rem set EMERGE_PKGDSTDIR=%KDEROOT%\tmp

rem No editing should be necessary below this line (in an ideal world)
rem ##################################################################

set PATH=%PYTHONPATH%;%PATH%

echo kdesettings.bat executed
echo KDEROOT     : %KDEROOT%
echo KDECOMPILER : %KDECOMPILER%
echo KDESVNDIR   : %KDESVNDIR%
echo PYTHONPATH  : %PYTHONPATH%
echo DOWNLOADDIR : %DOWNLOADDIR%

