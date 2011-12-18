import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'
        for version in [ '7.9', '8.00', '8.02', '8.10' ,'8.12' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'pcre', version,packagetypes=['src',] )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'pcre', version, '.tar.bz2.sha1',packagetypes=['src',] )


        self.shortDescription = "Perl-Compatible Regular Expressions"
        self.defaultTarget = '8.12'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        self.dependencies[ 'win32libs-bin/libbzip2' ] = 'default'
        self.dependencies[ 'win32libs-bin/zlib' ] = 'default'

        if emergePlatform.isCrossCompilingEnabled():
            self.buildDependencies['win32libs-sources/wcecompat-src'] = 'default'

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
