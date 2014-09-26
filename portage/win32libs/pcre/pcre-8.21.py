import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ '7.9', '8.00', '8.02', '8.10' ,'8.12', '8.21', '8.32', '8.36' ]:
            self.targets[ ver ] = 'ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'pcre-' + ver
        self.patchToApply[ '8.10' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        self.patchToApply[ '8.12' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        self.patchToApply[ '8.21' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        self.patchToApply[ '8.32' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        self.patchToApply[ '8.36' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        if emergePlatform.isCrossCompilingEnabled():
            self.patchToApply[ '8.10' ].append( ( "pcre-8.02-20100518.diff", 1 ) )

        self.targetDigests['8.10'] = '8b345da0f835b2caabff071b0b5bab40564652be'
        self.targetDigests['8.12'] = '2219b372bff53ee29a7e44ecf5977ad15df01cea'
        self.targetDigests['8.21'] = '52abf655d94f5208377258ffff27c7b35c53af39'
        self.targetDigests['8.32'] = 'dbd44267cf4d7c6464391003908d5a4342726700'
        self.targetDigests['8.36'] = '9a074e9cbf3eb9f05213fd9ca5bc188644845ccc'

        self.shortDescription = "Perl-Compatible Regular Expressions"
        self.defaultTarget = '8.36'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        self.dependencies[ 'win32libs/libbzip2' ] = 'default'
        self.dependencies[ 'win32libs/zlib' ] = 'default'

        if emergePlatform.isCrossCompilingEnabled():
            self.buildDependencies['win32libs/wcecompat'] = 'default'

class Package( CMakePackageBase ):
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

if __name__ == '__main__':
    Package().execute()
