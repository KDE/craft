import utils
import os
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.3.0'] = 'ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-1.3.0.tar.bz2'
        self.targetInstSrc['1.3.0'] = 'gpgme-1.3.0'
        self.targetDigests['1.3.0'] = '0db69082abfbbbaf86c3ab0906f5137de900da73'
        self.patchToApply['1.3.0'] = [('gpgme-1447-HEAD.diff', 0), 
                                      ('gpgme-1.3.0-cmake.diff', 1), 
                                      ('gpgme-1.3.0-20101102.diff', 1), 
                                      ('gpgme-1.3.0-mingw.diff', 1)]
        self.defaultTarget = '1.3.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/gpg-error'] = 'default'
        self.dependencies['win32libs-bin/assuan2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
