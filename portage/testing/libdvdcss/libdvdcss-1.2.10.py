import base
import os
import shutil
import utils
import info

PACKAGE_NAME         = "libdvdcss"
PACKAGE_VER          = "1.2.10"
PACKAGE_FULL_VER     = "1.2.10"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libdvdcss"

SRC_URI= """
http://download.videolan.org/pub/libdvdcss/1.2.10/libdvdcss-1.2.10.tar.bz2
"""

DEPEND = """
"""

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.2.10'] = SRC_URI
        self.defaultTarget = '1.2.10'
        
class subclass( base.baseclass ):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "libdvdcss-1.2.10"
        #self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        base.baseclass.unpack( self ) or utils.die( "unpack failed" )
        os.chdir( self.workdir )
        shutil.copyfile( os.path.join( self.packagedir, "CMakeLists.txt" ), os.path.join( self.workdir,self.instsrcdir, "CMakeLists.txt" ) )
        shutil.copyfile( os.path.join( self.packagedir, "config.h" ), os.path.join( self.workdir,self.instsrcdir, "config.h" ) )
        shutil.copyfile( os.path.join( self.packagedir, "common.h" ), os.path.join( self.workdir,self.instsrcdir, "src/common.h" ) )
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
