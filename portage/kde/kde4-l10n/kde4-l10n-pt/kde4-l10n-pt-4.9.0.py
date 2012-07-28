import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.9.0', '4.9.1', '4.9.2', '4.9.3', '4.9.4']:
          self.targets[ ver] = 'ftp://ftp.kde.org/pub/kde/stable/%s/src/kde-l10n/kde-l10n-pt-%s.tar.xz' % (ver , ver )
          self.targetInstSrc[ ver] = 'kde-l10n-pt-%s'  % ver

        self.defaultTarget = '4.9.0'


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
