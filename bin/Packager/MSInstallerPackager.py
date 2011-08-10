
import uuid
import shutil
import re
import types
import fileinput
from _winreg import * # pylint: disable=F0401
import compiler
from CollectionPackagerBase import *


class MSInstallerPackager( CollectionPackagerBase ):
    def __init__( self ):
        CollectionPackagerBase.__init__( self )

    def generateMSInstaller( self ):
        """ runs tools to generate the installer itself """
        if self.package.endswith( "-package" ):
            shortPackage = self.package[ : -8 ]
        else:
            shortPackage = self.package
        if not "setupname" in self.defines or not self.defines[ "setupname" ]:
            self.defines[ "setupname" ] = "%s-setup-%s.exe" % ( shortPackage, self.buildTarget )
        if not "srcdir" in self.defines or not self.defines[ "srcdir" ]:
            self.defines[ "srcdir" ] = self.imageDir()
        if not "company" in self.defines or not self.defines[ "company" ]:
            self.defines[ "company" ] = "KDE"
        if not "productname" in self.defines or not self.defines[ "productname" ]:
            self.defines[ "productname" ] = "%s %s" % ( shortPackage.capitalize(), self.buildTarget )
        if not "executable" in self.defines or not self.defines[ "executable" ]:
            self.defines[ "executable" ] = ""
        if not self.scriptname:
            self.scriptname = os.path.join( os.path.dirname( __file__ ), "NullsoftInstaller.nsi" )

        # make absolute path for output file
        if not os.path.isabs( self.defines[ "setupname" ] ):
            dstpath = self.packageDestinationDir()
            self.defines[ "setupname" ] = os.path.join( dstpath, self.defines[ "setupname" ] )

#        definestring = ""
#        for key in self.defines:
#            definestring += " /D" + key + "=\"" + self.defines[ key ] + "\""

        utils.new_line()
        utils.debug( "generating installer %s" % self.defines[ "setupname" ] )
#        if self.isInstalled:
#            utils.systemWithoutShell( "\"%s\" %s %s" % ( os.path.join(
#                self.nsisInstallPath, 'makensis.exe' ), definestring,
#                self.scriptname ), cwd = os.path.abspath( self.packageDir() ) )

    def createPackage( self ):
        """ create a package """
        print "packaging using the NullsoftInstallerPackager"
        
        self.internalCreatePackage()

        self.generateMSInstaller()
        return True
