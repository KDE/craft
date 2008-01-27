@echo off
rem here you set the base directory under which the whole kde
rem system will live
set KDEROOT=e:\kderoot

rem here you set the compiler to be used:
rem mingw : use the mingw gcc compiler (recommended)
rem msvc2005: use the microsoft visual studio 2005 c-compiler
rem
set KDECOMPILER=mingw

rem here you should set the path to your python installation
rem this is needed, so that python will be found, when
rem python scripts will be executed. by setting this here,
rem you don´t have to change the environment settings of
rem windows at all
set PYTHONPATH=e:\python25

rem here you set set the path to msys if you want to compile
rem automake-based projects (only needed for some internal packages)
set MSYSDIR=e:\kderoot\msys

rem here you can set the download directory to another dir
rem if you want, so you can share the same download dir between
rem mingw and msvc
set DOWNLOADDIR=e:\kdedownload

rem here you can tell emerge in which dir you want to save the
rem svn checkout of kde sources, and you can optionally
rem set the svn.kde.org server instead of the anonsvn.kde.org
rem one, so that you can directly commit your changes from the
rem svn checkout from emerge, if you want.
set KDESVNDIR=e:\kdesvn
set KDESVNSERVER=svn://anonsvn.kde.org
set KDESVNUSERNAME=username
rem for security reasons you better log in to the kde server by hand
rem and set the username and password at first login. then svn will
rem remember the password and it does not have to be written down here
rem set KDESVNPASSWORD=password

rem if you use svn+ssh, you'll need a ssh-agent equaivalent for managing the authorization 
rem Pageant is provided by putty, get it at 
rem http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
rem and make sure plink is in your path and Pageant is configured (you need to import your key)
set SVN_SSH=plink 

rem it is not recommended anymore to use the traditional layout.
rem if you want to use emerge.py together with the kdewin-installer, you should set
rem the value of directory_layout to 'installer', if you leave it unset or set it to
rem 'traditional' you get the category sublayout
set directory_layout=installer

rem You can set type of emerge build.
rem There are standard two build types: Debug and Release
rem - both are used if no EMERGE_BUILDTYPE is set.
rem There is a third buildtype called RelWithDebInfo
rem - which is release (optimized) build but containing debugging information.
rem You can override the build type at the commandline using the '--buildtype=[BuildType]' option.
rem The build type which is set here will not override the buildtype in .py package files.
set EMERGE_BUILDTYPE=RelWithDebInfo

rem If you want to have verbose output uncomment the following option and set it to any positive integer
rem for verbose output and to 0 or disable it for normal output
set EMERGE_VERBOSE=1

rem If you want to have shorter build times, and less disk usage, enable the next option
rem for all kde svn based stuff it will not copy the svn sources again
rem problem is that you cannot make packages when this option is set
set EMERGE_NOCOPY=True

rem If you want to build all packages with buildTests, enable the next option
rem this applies only to the cmake based packages
rem set EMERGE_BUILDTESTS=True

rem The next option only applies if you want to make packages
rem it sets the output directory where your generated packages should be stored
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

