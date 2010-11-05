import shutil
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.4.4','1.2.43']:
            self.targets[ver] = 'http://downloads.sourceforge.net/libpng/libpng-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libpng-' + ver
        self.patchToApply['1.4.4'] = ("libpng-1.4.4-20100517.diff", 1)
        self.targetDigests['1.4.4'] = '245490b22086a6aff8964b7d32383a17814d8ebf'
        
        self.description = 'A library to display png images'
        self.defaultTarget = '1.4.4'
        

    def setDependencies( self ):
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DPNG_TESTS=OFF -DPNG_STATIC=OFF -DPNG_NO_STDIO=OFF"
        self.subinfo.options.package.packageName = 'libpng'

    def createPackage( self ): 
        if(self.subinfo.buildTarget.startswith('1.2')):
           libName="libpng12" 
        else:
           libName="libpng14" 
        self.stripLibs( libName )
        # auto-create both import libs with the help of pexports	 
        self.createImportLibs( libName )
        return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
    
