import shutil
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.4.1','1.2.40']:
            self.targets[ver] = 'http://downloads.sourceforge.net/libpng/libpng-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libpng-' + ver
        
        self.defaultTarget = '1.4.1'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DPNG_TESTS=OFF -DPNG_STATIC=OFF -DPNG_NO_STDIO=OFF"
        self.subinfo.options.package.packageName = 'libpng'
        self.subinfo.options.package.withCompiler = None
            
            
    def unpack( self ):
        if( not CMakePackageBase.unpack( self ) ):
          return False 
        if(self.subinfo.buildTarget in ['1.4.1']):
          return True
        # the cmake script is in libpng-src/scripts	 
        srcdir  = os.path.join( self.sourceDir(), "scripts", "CMakeLists.txt" )	 
        destdir = os.path.join( self.sourceDir(),            "CMakeLists.txt" )	 
        shutil.copy( srcdir, destdir )
        return True
        
        
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
    