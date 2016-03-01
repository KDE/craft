#
# copyright (c) 2010 Patrick Spendrin <ps_ml@gmx.de>
# copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
#

import os

if os.name == 'nt':
    from winreg import * # pylint: disable=F0401

import EmergeDebug
import EmergeHash
import utils
import shutil
from Packager.CollectionPackagerBase import *


class NSIPackagerLists( PackagerLists ):
    """ dummy name for PackagerLists """

class NullsoftInstallerPackager( CollectionPackagerBase ):
    """
Packager for Nullsoft scriptable install system

This Packager generates a nsis installer (an executable which contains all files)
from the image directories of emerge. This way you can be sure to have a clean
installer.

In your package, you can add regexp whitelists and blacklists (see example files
for the fileformat). The files for both white- and blacklists, must be given already
in the constructor.

You can override the .nsi default script and you will get the following defines
given into the nsis generator via commandline if you do not override the attributes
of the same name in the dictionary self.defines:
setupname:      PACKAGENAME-setup-BUILDTARGET.exe
                PACKAGENAME is the name of the package, if the package ends with "-package",
                that part is removed
srcdir:         is set to the image directory, where all files from the image directories
                of all dependencies are gathered. You shouldn't normally have to set this.
company:        sets the company name used for the registry key of the installer. Default
                value is "KDE".
productname:    contains the capitalized PACKAGENAME and the buildTarget of the current package
executable:     executable is defined empty by default, but it is used to add a link into the
                start menu.
You can add your own defines into self.defines as well.

The output directory is determined by the environment variable EMERGE_PKGDSTDIR.
if EMERGE_NOCLEAN is given (e.g. because you call emerge --update --package Packagename), the
file collection process is skipped, and only the installer is generated.
"""
    def __init__( self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__( self, whitelists, blacklists )
        self.nsisInstallPath = None
        self._isInstalled = False

    def isInstalled(self):
        if not self._isInstalled:
            self._isInstalled = self.__isInstalled()
            if not self._isInstalled:
                EmergeDebug.die("could not find installed nsis package, "
                           "you can install it using emerge nsis or"
                           "download and install it from "
                           "http://sourceforge.net/projects/nsis/")

    def __isInstalled( self ):
        """ check if nsis (Nullsoft scriptable install system) is installed somewhere """
        if os.name != 'nt':
            return False

        # pylint: disable=E0602
        # if pylint is done on linux, we don't have those toys
        if os.path.exists(os.path.join(self.rootdir, "dev-utils", "makensis.exe")):
            self.nsisInstallPath = os.path.join(self.rootdir, "dev-utils")
            return True
        elif os.path.exists(os.path.join(self.rootdir, "dev-utils", "nsis", "makensis.exe")):
            self.nsisInstallPath = os.path.join(self.rootdir, "dev-utils", "nsis")
            return True
        try:
            key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\NSIS\Unicode', 0, KEY_READ )
            [_,self.nsisInstallPath,_] = EnumValue( key, 0 )#????
        except WindowsError:
            try:
                key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\NSIS', 0, KEY_READ )
                [ self.nsisInstallPath, dummyType ] = QueryValueEx( key, "" )
            except WindowsError:
                try:
                    key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\NSIS\Unicode', 0, KEY_READ )
                    [_,self.nsisInstallPath,_] = EnumValue( key, 0 )#????
                except WindowsError:
                    try:
                        key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\NSIS', 0, KEY_READ )
                        [ self.nsisInstallPath, dummyType ] = QueryValueEx( key, "" )
                    except WindowsError:
                        return False        
        
        CloseKey(key)
        return True

    def getVCRuntimeLibrariesLocation(self):
        """ Note: For MSVC, only: Return base directory for VC runtime distributable libraries """
        return os.path.join( os.path.dirname( shutil.which( "cl.exe" ) ), "..", "redist" )

    def getVCRedistLocation(self, compiler):
        if compiler.isMSVC2015():
            if compiler.isX64():
                return os.path.join( self.getVCRuntimeLibrariesLocation(), "1033", "vcredist_x64.exe" )
            elif compiler.isX86():
                return os.path.join( self.getVCRuntimeLibrariesLocation(), "1033", "vcredist_x86.exe" )
        return None

    def generateNSISInstaller( self ):
        """ runs makensis to generate the installer itself """

        self.isInstalled()

        if not self.scriptname:
            self.scriptname = os.path.join( os.path.dirname( __file__ ), "NullsoftInstaller.nsi" )

        if self.package.endswith( "-package" ):
            shortPackage = self.package[ : -8 ]
        else:
            shortPackage = self.package

        if not "setupname" in self.defines or not self.defines[ "setupname" ]:
            self.defines[ "setupname" ] = "%s-%s-setup-%s.exe" % ( shortPackage, compiler.architecture(), self.buildTarget )
        if not "srcdir" in self.defines or not self.defines[ "srcdir" ]:
            self.defines[ "srcdir" ] = self.archiveDir()
        if not "company" in self.defines or not self.defines[ "company" ]:
            self.defines[ "company" ] = "KDE"
        if not "productname" in self.defines or not self.defines[ "productname" ]:
            self.defines[ "productname" ] = shortPackage.capitalize()
        if not "version" in self.defines or not self.defines[ "version" ]:
            self.defines[ "version" ] = self.buildTarget
        if not "executable" in self.defines or not self.defines[ "executable" ]:
            self.defines[ "executable" ] = ""
        if "license" in self.defines and self.defines[ "license" ]:
            self.defines[ "license" ] = "!insertmacro MUI_PAGE_LICENSE \"%s\"" %  self.defines[ "license" ] 
        else:
            self.defines[ "license" ] = ""
        if "icon" in self.defines and self.defines[ "icon" ]:
            self.defines[ "icon" ] = "!define MUI_ICON \"%s\"" % self.defines[ "icon" ]
        else:
            self.defines[ "icon" ] = ""
        self.defines[ "architecture" ] = compiler.architecture()
        self.defines[ "defaultinstdir" ] = "$PROGRAMFILES64" if compiler.isX64() else "$PROGRAMFILES"

        # runtime distributable files
        self.defines[ "vcredist" ] = self.getVCRedistLocation(compiler)
        if not self.defines[ "vcredist" ]:
            self.defines[ "vcredist" ] = "none"
            # for earlier versions of MSVC, simply copy the redist files to the "bin" folder of the installation
            if compiler.isMSVC():
                if compiler.isX64():
                    redistPath = os.path.join( os.path.join( self.getVCRuntimeLibrariesLocation(), "x64" ) )
                else:
                    redistPath = os.path.join( os.path.join( self.getVCRuntimeLibrariesLocation(), "x86" ) )
                for root, subdirs, files in os.walk( redistPath ):
                    for f in files:
                        shutil.copy( os.path.join( root, f ), os.path.join( self.archiveDir(), "bin" ) )
            else:
                EmergeDebug.die( "Fixme: copy MinGW runtime (listdc++.dll, etc." )

        # make absolute path for output file
        if not os.path.isabs( self.defines[ "setupname" ] ):
            dstpath = self.packageDestinationDir()
            self.defines[ "setupname" ] = os.path.join( dstpath, self.defines[ "setupname" ] )

        definestring = ""
        for key in self.defines:
            definestring += " /D" + key + "=\"" + self.defines[ key ] + "\""

        EmergeDebug.new_line()
        EmergeDebug.debug("generating installer %s" % self.defines["setupname"])

        verboseString = "/V4" if EmergeDebug.verbose() > 0 else "/V3"

        if self.isInstalled:
            makensisExe = os.path.join(self.nsisInstallPath, 'makensis.exe')
            if not utils.systemWithoutShell( "\"%s\" %s %s %s" % (makensisExe, verboseString, definestring,
                    self.scriptname ), cwd = os.path.abspath( self.packageDir() ) ):
                EmergeDebug.die("Error in makensis execution")

    def createPackage( self ):
        """ create a package """
        self.isInstalled()

        EmergeDebug.debug("packaging using the NullsoftInstallerPackager")

        self.internalCreatePackage()
        self.preArchive()
        self.generateNSISInstaller()
        EmergeHash.createDigestFiles(self.defines["setupname"])
        return True
