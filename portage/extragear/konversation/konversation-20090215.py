# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.2.1'] = 'ftp://ftp.kde.org/pub/kde/stable/konversation/1.2.1/src/konversation-1.2.1.tar.bz2'
        self.targetInstSrc['1.2.1'] = 'konversation-1.2.1'
        self.targets['1.2.3'] = 'ftp://ftp.kde.org/pub/kde/stable/konversation/1.2.3/src/konversation-1.2.3.tar.bz2'
        self.targetInstSrc['1.2.1'] = 'konversation-1.2.3'
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/konversation/konversation.git'
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
