# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.4/kdegames'
        for ver in ['90', '95']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.3.' + ver + '/src/kdegames-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdegames-4.3.' + ver
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.4.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.4.' + ver + '/src/kdegames-4.4.' + ver + '.tar.bz2'
          self.targetInstSrc['4.4.' + ver] = 'kdegames-4.4.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.4/kdebase-runtime'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
