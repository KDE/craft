import shutil
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.7.7']:
            self.targets[ver] = 'ftp://xmlsoft.org/libxml2/libxml2-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libxml2-' + ver
        self.patchToApply['2.7.7'] = ("libxml2-2.7.7-20101103.diff", 1)
        self.targetDigests['2.7.7'] = '8592824a2788574a172cbddcdc72f734ff87abe3'
        
        self.defaultTarget = '2.7.7'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-sources/zlib-src'] = 'default'
        self.hardDependencies['win32libs-sources/win_iconv-src'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = False

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'libxml2'
        self.subinfo.options.configure.defines = "-DBUILD_tests=OFF"
            
            
    def createPackage( self ): 
        libName="libxml2" 
        self.stripLibs( libName )
        # auto-create both import libs with the help of pexports	 
        self.createImportLibs( libName )
        return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
    
