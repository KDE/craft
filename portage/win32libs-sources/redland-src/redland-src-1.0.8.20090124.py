import info
import emergePlatform

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '1.0.8'
        self.targets[ ver ] = 'http://download.librdf.org/source/redland-1.0.8.tar.gz'
        self.targetInstSrc[ ver ] = 'redland-1.0.8'
        self.patchToApply[ ver ] = ( 'redland-1.0.8-20100719.diff', 1 )
        self.targetDigests['1.0.8'] = '9501b95a2b668067e2dcb0ab3bdb59e0376144de'
        self.defaultTarget = ver

    def setDependencies( self ):
        self.dependencies['win32libs-bin/sqlite'] = 'default'
        self.dependencies['win32libs-bin/libcurl'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'
        self.dependencies['win32libs-bin/libxslt'] = 'default'
        self.dependencies['win32libs-bin/openssl'] = 'default'
        self.dependencies['win32libs-bin/pcre'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-sources/wcecompat-src'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = False

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.package.packageName = 'redland'
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
