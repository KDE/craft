import shutil
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['4.1.6']:
            self.targets[ver] = 'http://downloads.sourceforge.net/sourceforge/giflib/giflib-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'giflib-' + ver
        self.patchToApply['4.1.6'] = ("giflib-4.1.6-20100327.diff", 1)
        
        self.defaultTarget = '4.1.6'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-sources/zlib-src'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'giflib'
        self.subinfo.options.configure.defines = "-DBUILD_utils=OFF"
        self.subinfo.options.package.withCompiler = None
            
            
    def createPackage( self ): 
        libName="giflib4" 
        self.stripLibs( libName )
        # auto-create both import libs with the help of pexports	 
        self.createImportLibs( libName )
        return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
    