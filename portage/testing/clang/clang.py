# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "http://llvm.org/svn/llvm-project/cfe/trunk"
        self.targets[ "3.5.0" ] = "http://llvm.org/releases/3.5.0/cfe-3.5.0.src.tar.xz"
        self.targetInstSrc[ "3.5.0" ] = "cfe-3.5.0.src"
        self.targetDigests['3.5.0'] = '834cee2ed8dc6638a486d8d886b6dce3db675ffa'
        self.defaultTarget = "3.5.0"

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['testing/llvm'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

