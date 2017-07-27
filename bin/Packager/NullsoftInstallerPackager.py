#
# copyright (c) 2010 Patrick Spendrin <ps_ml@gmx.de>
# copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
#

import os

if os.name == 'nt':
    from winreg import * # pylint: disable=F0401

from CraftDebug import craftDebug
import CraftHash
import utils
import shutil
import glob
from Packager.CollectionPackagerBase import *

class NullsoftInstallerPackager( CollectionPackagerBase ):
    """
Packager for Nullsoft scriptable install system

This Packager generates a nsis installer (an executable which contains all files)
from the image directories of craft. This way you can be sure to have a clean
installer.

In your package, you can add regexp whitelists and blacklists (see example files
for the fileformat). The files for both white- and blacklists, must be given already
in the constructor.

You can override the .nsi default script and you will get the following defines
given into the nsis generator via commandline if you do not override the attributes
of the same name in the dictionary self.defines:
setupname:      PACKAGENAME-setup-BUILDTARGET.exe
                PACKAGENAME is the name of the package
srcdir:         is set to the image directory, where all files from the image directories
                of all dependencies are gathered. You shouldn't normally have to set this.
company:        sets the company name used for the registry key of the installer. Default
                value is "KDE".
productname:    contains the capitalized PACKAGENAME and the buildTarget of the current package
executable:     executable is defined empty by default, but it is used to add a link into the
                start menu.
You can add your own defines into self.defines as well.

The output directory is determined by the environment variable EMERGE_PKGDSTDIR.
if EMERGE_NOCLEAN is given (e.g. because you call craft --update --package Packagename), the
file collection process is skipped, and only the installer is generated.
"""
    @InitGuard.init_once
    def __init__( self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__( self, whitelists, blacklists )
        self.nsisExe = None
        self._isInstalled = False


    def _setDefaults(self):
        self.defines.setdefault( "architecture", craftCompiler.architecture)
        self.defines.setdefault( "company", "KDE")
        self.defines.setdefault( "defaultinstdir", "$PROGRAMFILES64" if craftCompiler.isX64() else "$PROGRAMFILES")
        self.defines.setdefault( "executable",  "")
        self.defines.setdefault( "icon",  "")
        self.defines.setdefault( "license",  "")
        self.defines.setdefault( "productname",  self.package.capitalize())
        self.defines.setdefault("setupname",  self.binaryArchiveName(fileType="exe", includeRevision=True))
        self.defines.setdefault( "srcdir",  self.archiveDir())
        self.defines.setdefault( "extrashortcuts", "")
        self.defines.setdefault( "version", self.getPackageVersion()[0])
        self.defines.setdefault( "website",  self.subinfo.homepage if not self.subinfo.homepage == "" else "https://community.kde.org/Windows")
        # runtime distributable files
        self.defines.setdefault( "vcredist",  self.getVCRedistLocation())

        if not self.scriptname:
            self.scriptname = os.path.join( os.path.dirname( __file__ ), "NullsoftInstaller.nsi" )


    def isNsisInstalled(self):
        if not self._isInstalled:
            self._isInstalled = self.__isInstalled()
            if not self._isInstalled:
                craftDebug.log.critical("could not find installed nsis package, "
                           "you can install it using craft nsis or"
                           "download and install it from "
                           "http://sourceforge.net/projects/nsis/")

    def __isInstalled( self ):
        """ check if nsis (Nullsoft scriptable install system) is installed somewhere """
        if os.name != 'nt':
            return False

        # pylint: disable=E0602
        # if pylint is done on linux, we don't have those toys
        self.nsisExe = utils.utilsCache.findApplication("makensis")
        if self.nsisExe:
            return True
        try:
            key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\NSIS\Unicode', 0, KEY_READ )
            _, nsisPath, _ = EnumValue( key, 0 )#????
        except WindowsError:
            try:
                key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\NSIS', 0, KEY_READ )
                nsisPath, _ = QueryValueEx( key, "" )
            except WindowsError:
                try:
                    key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\NSIS\Unicode', 0, KEY_READ )
                    _ ,nsisPath, _ = EnumValue( key, 0 )#????
                except WindowsError:
                    try:
                        key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\NSIS', 0, KEY_READ )
                        nsisPath, _ = QueryValueEx(key, "")
                    except WindowsError:
                        return False

        CloseKey(key)
        self.nsisExe = os.path.join(nsisPath, "makensis")
        return True

    def getVCRuntimeLibrariesLocation(self):
        """ Note: For MSVC, only: Return base directory for VC runtime distributable libraries """
        if "VCToolsRedistDir" in os.environ:
            return os.environ["VCToolsRedistDir"]
        _path = os.path.join( os.path.dirname( shutil.which( "cl.exe" ) ), "..", "redist" )
        if not os.path.exists(_path):
            _path = os.path.join( os.path.dirname( shutil.which( "cl.exe" ) ), "..", "..", "redist" )
        return _path

    def getVCRedistLocation(self):
        if not craftCompiler.isMSVC():
            return "none"
        _file = None
        if craftCompiler.isMSVC():
            arch = "x86"
            if craftCompiler.isX64(): arch = "x64"
            if craftCompiler.isMSVC2015():
                _file = os.path.join( self.getVCRuntimeLibrariesLocation(), "1033", f"vcredist_{arch}.exe" )
            elif craftCompiler.isMSVC2017():
                _file = os.path.join(self.getVCRuntimeLibrariesLocation(), "..", "14.10.25008", f"vcredist_{arch}.exe")
            if not os.path.isfile(_file):
                craftDebug.new_line()
                craftDebug.log.critical("Assuming we can't find a c++ redistributable because the user hasn't got one. Must be fixed manually.")
        return _file

    def generateNSISInstaller( self ):
        """ runs makensis to generate the installer itself """

        self.isNsisInstalled()
        self._setDefaults()

        if not self.defines["icon"] == "":
            self.defines["icon"] = "!define MUI_ICON \"%s\"" % self.defines["icon"]
        if not self.defines["license"] == "":
            self.defines["license"] = "!define MUI_PAGE_LICENSE \"%s\"" % self.defines["license"]



        # make absolute path for output file
        if not os.path.isabs( self.defines[ "setupname" ] ):
            dstpath = self.packageDestinationDir()
            self.defines[ "setupname" ] = os.path.join( dstpath, self.defines[ "setupname" ] )

        definestring = ""
        for key, value in self.defines.items():
            if value is not None:
                definestring += f" /D{key}=\"{value}\""

        craftDebug.new_line()
        craftDebug.log.debug("generating installer %s" % self.defines["setupname"])

        verboseString = "/V4" if craftDebug.verbose() > 0 else "/V3"

        if self.isNsisInstalled:
            if not utils.systemWithoutShell( "\"%s\" %s %s %s" % (self.nsisExe, verboseString, definestring,
                    self.scriptname ), cwd = os.path.abspath( self.packageDir() ) ):
                craftDebug.log.critical("Error in makensis execution")

    def createPackage( self ):
        """ create a package """
        self.isNsisInstalled()

        craftDebug.log.debug("packaging using the NullsoftInstallerPackager")

        self.internalCreatePackage()
        self.preArchive()
        self.generateNSISInstaller()
        CraftHash.createDigestFiles(self.defines["setupname"])
        return True
