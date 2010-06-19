# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.2.1', '1.2.2', '1.2.3', '1.3']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/stable/konversation/' + ver + '/src/konversation-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'konversation-' + ver
        self.svnTargets['gitHEAD'] = 'git://git.kde.org/konversation/konversation.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
    
class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
