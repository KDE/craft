# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "http://llvm.org/git/clang.git"
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


    def configure(self):
        if compiler.isMinGW() and not self.buildType() == "Release":
            utils.die("You should build clang only in Release mode as it will use up to 10gb disk space if build as RelWithDebInfo, see emerge --buildtype Release")
        return CMakeBuildSystem.configure(self)