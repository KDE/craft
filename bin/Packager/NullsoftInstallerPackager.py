#
# copyright (c) 2010 Patrick Spendrin <ps_ml@gmx.de>
# copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
#
from winreg import * # pylint: disable=F0401

import utils
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
        self.isInstalled = self.__isInstalled()
        if not self.isInstalled:
            utils.die( "could not find installed nsis package, "
                       "you can install it using emerge nsis or"
                       "download and install it from "
                       "http://sourceforge.net/projects/nsis/" )

    def __isInstalled( self ):
        """ check if nsis (Nullsoft scriptable install system) is installed somewhere """
        # pylint: disable=E0602
        # if pylint is done on linux, we don't have those toys
        if os.path.exists(os.path.join(self.rootdir, "dev-utils", "makensis.exe")):
            self.nsisInstallPath = os.path.join(self.rootdir, "dev-utils")
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

    def generateNSISInstaller( self ):
        """ runs makensis to generate the installer itself """
        if self.package.endswith( "-package" ):
            shortPackage = self.package[ : -8 ]
        else:
            shortPackage = self.package
        if not "setupname" in self.defines or not self.defines[ "setupname" ]:
            self.defines[ "setupname" ] = "%s-%s-setup-%s.exe" % ( shortPackage, os.getenv("EMERGE_ARCHITECTURE"), self.buildTarget )
        if not "srcdir" in self.defines or not self.defines[ "srcdir" ]:
            self.defines[ "srcdir" ] = self.imageDir()
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
        if not self.scriptname:
            self.scriptname = os.path.join( os.path.dirname( __file__ ), "NullsoftInstaller.nsi" )
        self.defines[ "architecture" ] = os.getenv("EMERGE_ARCHITECTURE")

        # make absolute path for output file
        if not os.path.isabs( self.defines[ "setupname" ] ):
            dstpath = self.packageDestinationDir()
            self.defines[ "setupname" ] = os.path.join( dstpath, self.defines[ "setupname" ] )

        definestring = ""
        for key in self.defines:
            definestring += " /D" + key + "=\"" + self.defines[ key ] + "\""

        utils.new_line()
        utils.debug( "generating installer %s" % self.defines[ "setupname" ] )
        if self.isInstalled:
            if not utils.systemWithoutShell( "\"%s\" %s %s" % ( os.path.join(
                    self.nsisInstallPath, 'makensis.exe' ), definestring,
                    self.scriptname ), cwd = os.path.abspath( self.packageDir() ) ):
                utils.die("Error in makensis execution")

    def createPackage( self ):
        """ create a package """
        print("packaging using the NullsoftInstallerPackager")

        self.internalCreatePackage()
        self.preArchive()
        self.generateNSISInstaller()
        utils.createDigestFile( self.defines[ "setupname" ])
        return True
