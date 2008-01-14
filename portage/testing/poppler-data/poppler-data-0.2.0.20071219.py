import base
import os
import utils
from utils import die

PACKAGE_NAME         = "poppler-data"
PACKAGE_VER          = "0.2.0"
PACKAGE_FULL_VER     = "0.2.0"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "poppler-data"

SRC_URI = """http://poppler.freedesktop.org/""" + PACKAGE_FULL_NAME + """.tar.gz"""

DEPEND = """
gnuwin32/patch
"""

##http://poppler.freedesktop.org/""" + PACKAGE_FULL_NAME + """.tar.gz
##"""

class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, SRC_URI )
        self.instsrcdir = PACKAGE_FULL_NAME
        self.createCombinedPackage = True

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
            
        src = os.path.join( self.workdir, self.instsrcdir )

        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir , "poppler-data-cmake.patch" ) )
        if utils.verbose() >= 1:
            print cmd
        self.system( cmd ) or die( "patch" )

        return True
        
    def compile( self ):
        self.kdeCompile()
        return True
        
    def install( self ):
        self.kdeInstall()
        return True
        
    def make_package( self ):
        # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
