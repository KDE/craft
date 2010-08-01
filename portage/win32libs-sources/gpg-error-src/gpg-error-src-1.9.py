import utils
import os
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.9'] = 'ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-1.9.tar.bz2'
        self.patchToApply['1.9'] = ('libgpg-error-1.9-20100801.diff', 1)
        self.targetInstSrc['1.9'] = 'libgpg-error-1.9'
        self.targetDigests['1.9'] = '6836579e42320b057a2372bbcd0325130fe2561e'
        self.defaultTarget = '1.9'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['gnuwin32/grep'] = 'default'
        self.hardDependencies['gnuwin32/gawk'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_TOOL=OFF -DBUILD_TESTS=ON"


if __name__ == '__main__':
    Package().execute()
