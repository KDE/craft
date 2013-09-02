import info
import platform
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['1.5.0', '1.5.3']:
            self.targets[ ver ] = 'ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'libgcrypt-' + ver

        self.patchToApply['1.5.0'] = [('libgcrypt-1.5.0-20110831.diff', 1), 
                                      ('libgcrypt-1.5.0-cmake.diff', 1),
                                      ('libgcrypt-win64.diff', 1)]
        self.patchToApply['1.5.3'] = [('libgcrypt-1.5.0-20110831.diff', 1), 
                                      ('libgcrypt-1.5.3-cmake.diff', 1),
                                      ('libgcrypt-win64.diff', 1)]
        self.targetDigests['1.5.0'] = '3e776d44375dc1a710560b98ae8437d5da6e32cf'
        self.targetDigests['1.5.3'] = '2c6553cc17f2a1616d512d6870fe95edf6b0e26e'

        self.shortDescription = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = '1.5.3'

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
