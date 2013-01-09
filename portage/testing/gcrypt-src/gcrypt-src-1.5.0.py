import info
import platform
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['1.5.0']:
            self.targets[ ver ] = 'ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'libgcrypt-' + ver

        self.patchToApply['1.5.0'] = [('libgcrypt-1.5.0-20110831.diff', 1), ('libgcrypt-1.5.0-cmake.diff', 1)]
        self.targetDigests['1.5.0'] = 'e6508315b76eaf3d0df453f67371b106654bd4fe'
        self.defaultTarget = '1.5.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/gpg-error'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.configure.testDefine = "-DBUILD_TESTS=ON"
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
