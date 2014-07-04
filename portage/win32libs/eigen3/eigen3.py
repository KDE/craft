# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.2.1'] = 'http://bitbucket.org/eigen/eigen/get/3.2.1.tar.bz2'
        self.targetInstSrc['3.2.1'] = 'eigen-eigen-6b38706d90a9'
        self.targetDigests['3.2.1'] = '17aca570d647b25cb3d9dac54b480cfecf402ed9'

        self.shortDescription = 'C++ template library for linear algebra'
        self.defaultTarget = '3.2.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

