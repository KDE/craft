import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.3.0', '1.3.1', '1.4.3']:
            self.targets[ver] = 'ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'gpgme-' + ver
        self.patchToApply['1.3.0'] = [('gpgme-1447-HEAD.diff', 0),
                                      ('gpgme-1.3.0-cmake.diff', 1),
                                      ('gpgme-1.3.0-20101102.diff', 1),
                                      ('gpgme-1.3.0-mingw.diff', 1)]
        self.patchToApply['1.3.1'] = [('gpgme-1.3.1-20110830.diff', 1), ("gpgme-1.3.1-cmake.diff", 1)]
        self.patchToApply['1.4.3'] = [('gpgme-1.4.3-20130916.diff', 1), ("gpgme-1.4.3-cmake.diff", 1)]

        self.targets['1510'] = "download.sourceforge.net/kde-windows/gpgme-r1510.tar.bz2"
        self.targetInstSrc['1510'] = "gpgme-r1510"
        self.patchToApply['1510'] = [('gpgme-r1510-cmake.diff', 1), ('gpgme-r1510-20101205.diff', 1)]
        self.targetDigests['1510'] = 'bb67afb24dc95795ac2a369aafd7ef99438b90b6'
        self.targetDigests['1.3.0'] = '0db69082abfbbbaf86c3ab0906f5137de900da73'
        self.targetDigests['1.3.1'] = '7d19a95a2239da13764dad7f97541be884ec5a37'
        self.targetDigests['1.4.3'] = 'ffdb5e4ce85220501515af8ead86fd499525ef9a'

        self.shortDescription = "GnuPG cryptography support library (runtime)"
        self.defaultTarget = '1.4.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/gpg-error'] = 'default'
        self.dependencies['win32libs/assuan2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
