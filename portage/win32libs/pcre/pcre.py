import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ '7.9', '8.00', '8.02', '8.10' ,'8.12', '8.21', '8.32', '8.33' ]:
            self.targets[ ver ] = 'ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'pcre-' + ver
        self.patchToApply[ '8.10' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        self.patchToApply[ '8.12' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        self.patchToApply[ '8.21' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        self.patchToApply[ '8.32' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]
        self.patchToApply[ '8.33' ] = [ ( "pcre-8.10-20101125.diff", 1 ) ]

        self.targetDigests['8.10'] = '8b345da0f835b2caabff071b0b5bab40564652be'
        self.targetDigests['8.12'] = '2219b372bff53ee29a7e44ecf5977ad15df01cea'
        self.targetDigests['8.21'] = '52abf655d94f5208377258ffff27c7b35c53af39'
        self.targetDigests['8.32'] = 'dbd44267cf4d7c6464391003908d5a4342726700'
        self.targetDigests['8.33'] = 'c4dd6aa1ffeca7bea1bc45b214c8e862bfdacc3c'

        self.shortDescription = "Perl-Compatible Regular Expressions"
        self.defaultTarget = '8.33'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        self.dependencies[ 'win32libs/libbzip2' ] = 'default'
        self.dependencies[ 'win32libs/zlib' ] = 'default'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

        defines  = "-DBUILD_SHARED_LIBS=ON "
        defines += "-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON "
        defines += "-DPCRE_SUPPORT_UTF8=ON "
        defines += "-DPCRE_EBCDIC=OFF "
        self.subinfo.options.configure.defines = defines

if __name__ == '__main__':
    Package().execute()
