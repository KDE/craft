import utils
import os
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.5.0']:
            self.targets[ver] = 'ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'libgcrypt-' + ver
        self.targetDigests['1.5.0'] = '3e776d44375dc1a710560b98ae8437d5da6e32cf'
        self.patchToApply['1.5.0'] = [('libgcrypt-1.5.0-20120213.diff', 1)]

#        self.shortDescription = "GnuPG cryptography support library (runtime)"
        self.defaultTarget = '1.5.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/gpg-error'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
