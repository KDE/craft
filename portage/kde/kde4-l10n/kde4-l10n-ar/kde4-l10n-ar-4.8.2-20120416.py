import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.8.0', '4.8.1', '4.8.2']:
          self.targets[ ver] = 'ftp://ftp.kde.org/pub/kde/stable/%s/src/kde-l10n/kde-l10n-ar-%s.tar.bz2' % (ver , ver )
          self.targetInstSrc[ ver] = 'kde-l10n-ar-%s'  % ver

        self.defaultTarget = '4.8.2'

    def setDependencies( self ):
        self.buildDependencies['dev-util/cmake'] = 'default'
        self.buildDependencies['kde/kdelibs'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'

from Package.CMakePackageBase import *
class MainPackage( CMakePackageBase ):
            def __init__( self  ):
                self.subinfo = subinfo()
                CMakePackageBase.__init__( self )
                
if __name__ == '__main__':
    MainPackage().execute()