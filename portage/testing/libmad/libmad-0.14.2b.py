import base
import os
import shutil
import utils
import info

PACKAGE_NAME         = "libmad"
PACKAGE_VER          = "0.15.1b"
PACKAGE_FULL_VER     = "0.15.1b"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "mad"

SRC_URI= """
ftp://ftp.mars.org/pub/mpeg/libmad-0.15.1b.tar.gz
"""

DEPEND = """
"""

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.15.1b'] = SRC_URI
        self.defaultTarget = '0.15.1b'
        
class subclass( base.baseclass ):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "libmad-" + PACKAGE_VER
        #self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        base.baseclass.unpack( self ) or utils.die( "unpack failed" )
        os.chdir( self.workdir )
        shutil.copyfile( os.path.join( self.packagedir, "CMakeLists.txt" ), os.path.join( self.workdir,self.instsrcdir, "CMakeLists.txt" ) )
        shutil.copyfile( os.path.join( self.packagedir, "FindKDEWIN32.cmake" ), os.path.join( self.workdir,self.instsrcdir, "FindKDEWIN32.cmake" ) )
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
