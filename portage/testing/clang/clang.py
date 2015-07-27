# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "http://llvm.org/git/clang.git"
        releaseVersion = "3.5.0"
        self.targets[releaseVersion] = "http://llvm.org/releases/" + releaseVersion + "/cfe-" + releaseVersion + ".src.tar.xz"
        self.targetInstSrc[releaseVersion] = "cfe-" + releaseVersion + ".src"
        self.targetDigests[releaseVersion] = '7a00257eb2bc9431e4c77c3a36b033072c54bc7e'

        if compiler.isMSVC2015():
            self.defaultTarget = 'gitHEAD'
        else:
            self.defaultTarget = releaseVersion

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
