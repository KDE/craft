import base
import os
import utils
import shutil
from utils import die

PACKAGE_NAME         = "fontconfig"
PACKAGE_VER          = "2.4.2"
PACKAGE_FULL_VER     = "2.4.2-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libfontconfig"

SRC_URI= """
http://fontconfig.org/release/""" + PACKAGE_FULL_NAME + """.tar.gz
"""

DEPEND = """
dev-util/win32libs
testing/freetype-src
"""

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, SRC_URI )
        self.instsrcdir = PACKAGE_FULL_NAME
        self.createCombinedPackage = True

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir, "fontconfig-cmake.diff" ) )
        self.system( cmd ) or die( "patch" )

        return True

    def kdeSvnPath( self ):
        return False
    
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        # auto-create both import libs with the help of pexports
        #self.stripLibs( PACKAGE_DLL_NAME )

        # auto-create both import libs with the help of pexports
        #self.createImportLibs( PACKAGE_DLL_NAME )

        # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
