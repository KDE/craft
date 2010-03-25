import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['win32libs-sources/zlib-src'] = 'default'

    def setTargets( self ):
        self.targets['2.0.1'] = 'http://downloads.sourceforge.net/sourceforge/expat/expat-2.0.1.tar.gz'
     
        
        self.targetInstSrc['2.0.1'] = "expat-2.0.1"
       

        self.defaultTarget = '2.0.1'

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
        
    def createPackage( self ):
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libexpat-1" )
        return KDEWinPackager.createPackage( self )

           
if __name__ == '__main__':
     Package().execute()
