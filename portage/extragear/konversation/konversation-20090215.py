# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.2.1', '1.2.2', '1.2.3', '1.3', '1.3.1']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/stable/konversation/' + ver + '/src/konversation-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'konversation-' + ver
        self.svnTargets['gitHEAD'] = 'git://anongit.kde.org/konversation'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.dependencies['virtual/kdebase-runtime'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['virtual/kdepimlibs'] = 'default'
    
class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
