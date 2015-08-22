# -*- coding: utf-8 -*-
import info
import compiler
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['3.2.5']:
            self.targets[ver] = 'http://bitbucket.org/eigen/eigen/get/%s.tar.bz2' % ver
            self.archiveNames[ver] = "eigen-%s.tar.bz2" % ver
        self.targetInstSrc['3.2.5'] = 'eigen-eigen-bdd17ee3b1b3'
        self.targetDigests['3.2.5'] = 'aa4667f0b134f5688c5dff5f03335d9a19aa9b3d'

        self.shortDescription = 'C++ template library for linear algebra'
        self.defaultTarget = '3.2.5'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        if compiler.isMSVC():
            self.subinfo.options.configure.defines = "-DBUILD_TESTS=OFF"
