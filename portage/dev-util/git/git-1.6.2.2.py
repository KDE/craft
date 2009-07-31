# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.3'] = "http://winkde.org/pub/kde/ports/win32/repository/other/Git-1.6.3-preview20090507-2.tar.bz2"
        self.targetInstSrc['1.6.3'] = ""
        self.targetMergePath['1.6.3'] = "dev-utils/git";
        self.defaultTarget = '1.6.3'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
    
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
