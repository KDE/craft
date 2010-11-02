import shutil
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.1.26']:
            self.targets[ver] = 'ftp://xmlsoft.org/libxslt/libxslt-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libxslt-' + ver
        self.patchToApply['1.1.26'] = ("libxslt-1.1.26-20101102.diff", 1)
        self.targetDigests['1.1.26'] = '69f74df8228b504a87e2b257c2d5238281c65154'
        
        self.defaultTarget = '1.1.26'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-sources/libxml2-src'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = False

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'libxslt'
            
            
    def createPackage( self ): 
        libName="libxslt" 
        self.stripLibs( libName )
        # auto-create both import libs with the help of pexports	 
        self.createImportLibs( libName )
        return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
    
