import base
import os
import shutil
import utils
import info

PACKAGE_NAME         = "libofx"
PACKAGE_VER          = "0.9.1"
PACKAGE_FULL_VER     = "0.9.1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "ofx"

SRC_URI= """
http://downloads.sourceforge.net/project/libofx/libofx/0.9.1/libofx-0.9.1.tar.gz
"""
#http://sourceforge.net/projects/libofx/files/libofx/0.9.1/libofx-0.9.1.tar.gz/download

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.9.1'] = SRC_URI
        self.defaultTarget = '0.9.1'
        
    def setDependencies( self ):
        self.hardDependencies['testing/libopensp'] = 'default'
        self.hardDependencies['win32libs-bin/iconv'] = 'default'

class subclass( base.baseclass ):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "libofx-0.9.1"
        #self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        base.baseclass.unpack( self ) or utils.die( "unpack failed" )
        os.chdir( self.workdir )
        shutil.copyfile( os.path.join( self.packagedir, "CMakeLists.txt" ), os.path.join( self.workdir,self.instsrcdir, "CMakeLists.txt" ) )
        shutil.copyfile( os.path.join( self.packagedir, "FindOpenSP.cmake" ), os.path.join( self.workdir,self.instsrcdir, "FindOpenSP.cmake" ) )
        shutil.copyfile(os.path.join( self.packagedir, "config.h"), os.path.join( self.workdir,self.instsrcdir, "config.h" ) )
        if self.buildTarget == '0.9.1':
            self.system( "cd %s && patch -p0 < %s" % ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir, "ofx-msvc.diff" ) ) )
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
