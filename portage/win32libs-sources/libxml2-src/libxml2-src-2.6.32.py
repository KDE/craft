import os
from shells import MSysShell
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['dev-util/pexports'] = 'default'

    def setTargets( self ):
        self.targets[ '2.7.7' ] = "ftp://xmlsoft.org/libxml2/libxml2-2.7.7.tar.gz"
        self.targetInstSrc[ '2.7.7' ] = "libxml2-2.7.7"
        #self.patchToApply['2.7.7']=('pthreads.diff',1)
        self.defaultTarget = '2.7.7'

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.KDEWinPackager import *;

class Package( PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        self.subinfo.options.configure.defines =" --disable-static --enable-shared LDFLAGS=\"-L%s -lz\""%(MSysShell().toNativePath(os.path.join( os.environ.get( "KDEROOT" ) , "lib" )))
        
    def createPackage( self ):
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "xml2" )
        return KDEWinPackager.createPackage( self )

           
if __name__ == '__main__':
     Package().execute()
