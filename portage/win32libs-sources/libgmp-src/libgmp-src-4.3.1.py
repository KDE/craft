import os
import sys
import base
import info
import utils
import shutil

class subinfo(info.infoclass):

    def setTargets( self ):
        self.targets['4.3.1'] = "http://ftp.gnu.org/pub/gnu/gmp/gmp-4.3.1.tar.bz2"
        self.targetInstSrc['4.3.1'] = "gmp-4.3.1"
        self.shortDescription = "GNU MP library for arbitrary precision arithmetic"
        self.defaultTarget = '4.3.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/msys'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = True
        self.subinfo = subinfo()
        self.buildType = "Release"

    def execute( self ):
        base.baseclass.execute( self )
        if self.compiler <> "mingw":
            print "error: can only be build with MinGW right now."
            exit( 1 )
       
    def compile( self ):
        self.msys.msysCustomDefines = "--disable-cxx "
        return self.msysCompile()

    def install( self ):
        return self.msysInstall()
    
    def make_package( self ):
        in_lib  = os.path.join( self.imagedir, "bin", "libgmp-3.dll" )
        out_lib = os.path.join( self.imagedir, "bin", "libgmp.dll" )
        if os.path.exists( in_lib ):
          os.rename( in_lib, out_lib )
        f = os.path.join( self.imagedir, "lib", "libgmp.la" )
        if os.path.exists( f ):
          os.remove( f )
        # auto-create both import libs with the help of pexports
        self.stripLibs( "libgmp" )

        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libgmp" )

        return self.doPackaging( "libgmp", self.buildTarget, True )
        
if __name__ == '__main__':
    subclass().execute()
