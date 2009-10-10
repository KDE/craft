# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.2'] = 'ftp://ftp.kde.org/pub/kde/stable/konversation/1.2/src/konversation-1.2.tar.bz2'
        self.targetInstSrc['1.2'] = 'konversation-1.2'
        self.svnTargets['svnHEAD'] = 'trunk/extragear/network/konversation'
        self.defaultTarget = 'svnHEAD'
    
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
