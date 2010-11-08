# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.2.0'] = 'http://www.cypherpunks.ca/otr/libotr-3.2.0.tar.gz'
        self.targetInstSrc['3.2.0'] = 'libotr-3.2.0'
        self.patchToApply['3.2.0'] = ('libotr-3.2.0-20091017.diff', 1)
        self.defaultTarget = '3.2.0'

    def setDependencies( self ):
        self.hardDependencies['testing/libgcrypt-src'] = 'default'
        self.hardDependencies['virtual/bin-base'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.buildInSource = True

if __name__ == '__main__':
    Package().execute()
