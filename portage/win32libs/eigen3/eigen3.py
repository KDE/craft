# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['3.2.4']:
            self.targets[ver] = 'http://bitbucket.org/eigen/eigen/get/%s.tar.bz2' % ver
            self.archiveNames[ver] = "eigen-%s.tar.bz2" % ver
        self.targetInstSrc['3.2.4'] = 'eigen-eigen-10219c95fe65'
        self.targetDigests['3.2.4'] = '64ea809acc449adbd8fe616def7d48ff4f0776a8'

        self.shortDescription = 'C++ template library for linear algebra'
        self.defaultTarget = '3.2.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

