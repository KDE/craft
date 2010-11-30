import utils
import os
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.0.1'] = 'ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-2.0.1.tar.bz2'
        self.targetInstSrc['2.0.1'] = 'libassuan-2.0.1'
        self.targetDigests['2.0.1'] = 'b7e9dbd41769cc20b1fb7db9f2ecdf276ffc352c'
        self.patchToApply['2.0.1'] = [ ('assuan-381-head.diff', 0), ('libassuan-2.0.1-20101029.diff', 1) ]
        self.shortDescription = "an IPC library used by some of the other GnuPG related packages"
        self.defaultTarget = '2.0.1'

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
