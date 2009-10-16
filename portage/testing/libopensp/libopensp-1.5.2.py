import base
import os
import shutil
import utils
import info

PACKAGE_NAME         = "libopensp"
PACKAGE_VER          = "1.5.2"
PACKAGE_FULL_VER     = "1.5.2"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "opensp"

SRC_URI= """
http://surfnet.dl.sourceforge.net/project/openjade/opensp/1.5.2/OpenSP-1.5.2.tar.gz
"""

DEPEND = """
"""

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.5.2'] = SRC_URI
        self.defaultTarget = '1.5.2'
        
class subclass( base.baseclass ):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "OpenSP-1.5.2"
        #self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        base.baseclass.unpack( self ) or utils.die( "unpack failed" )
        os.chdir( self.workdir )
        shutil.copyfile( os.path.join( self.packagedir, "CMakeLists.txt" ), os.path.join( self.workdir,self.instsrcdir, "CMakeLists.txt" ) )
        shutil.copyfile( os.path.join( self.packagedir, "config.h"), os.path.join( self.workdir,self.instsrcdir, "include/config.h" ) )
        if( not os.path.exists( self.workdir ) ):
            os.makedirs( self.workdir )
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):

    # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
