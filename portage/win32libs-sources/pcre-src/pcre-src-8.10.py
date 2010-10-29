import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['7.9', '8.00', '8.02', '8.10']:
          self.targets[ver] = 'ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'pcre-' + ver
        self.patchToApply['8.02'] = ("pcre-8.02-20100518.diff", 1)
        self.defaultTarget = '8.10'
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-sources/libbzip2-src'] = 'default'
        self.hardDependencies['win32libs-sources/zlib-src'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

        defines  = "-DBUILD_SHARED_LIBS=ON "
        defines += "-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON "
        defines += "-DPCRE_SUPPORT_UTF8=ON "
        defines += "-DPCRE_EBCDIC=OFF "
        if self.isTargetBuild():
            defines += "-DPCRE_BUILD_TESTS=OFF "
            defines += "-DPCRE_BUILD_PCREGREP=OFF "
        self.subinfo.options.configure.defines = defines
        self.subinfo.options.package.packageName = 'pcre'

if __name__ == '__main__':
    Package().execute()
