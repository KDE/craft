import shutil
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '1.4.1'
        self.targets[ver] = 'http://downloads.sourceforge.net/libpng/libpng-' + ver + '.tar.gz'
        self.targetInstSrc[ver] = 'libpng-' + ver
        self.defaultTarget = ver

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DPNG_TESTS=OFF -DPNG_STATIC=OFF -DPNG_NO_STDIO=OFF"
        self.subinfo.options.package.packageName = 'libpng'
        self.subinfo.options.package.withCompiler = None
        if not (self.compiler() == "mingw" or self.compiler() == "mingw4"):
            print "error: can only be build with MinGW (but in the end a MinGW/MSVC combined package is created)"
            exit( 1 )

if __name__ == '__main__':
    Package().execute()
