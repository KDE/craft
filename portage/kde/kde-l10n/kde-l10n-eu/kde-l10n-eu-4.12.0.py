import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.12.0', '4.12.1', '4.12.2', '4.12.3', '4.12.4']:
          self.targets[ ver] = 'ftp://ftp.kde.org/pub/kde/stable/%s/src/kde-l10n/kde-l10n-eu-%s.tar.xz' % (ver , ver )
          self.targetInstSrc[ ver] = 'kde-l10n-eu-%s'  % ver

        self.defaultTarget = '4.12.0'


    def setDependencies( self ):
        self.buildDependencies['dev-util/cmake'] = 'default'
        self.buildDependencies['kde/kdelibs'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
