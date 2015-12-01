# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]http://llvm.org/git/clang.git|release_37"
        releaseVersion = "3.7.0"
        self.targets[releaseVersion] = "http://llvm.org/releases/" + releaseVersion + "/cfe-" + releaseVersion + ".src.tar.xz"
        self.targetInstSrc[releaseVersion] = "cfe-" + releaseVersion + ".src"
        self.targetDigests['3.7.0'] = '4ff8100565528b13d99a73f807e9b426c3b3bed9'

        if compiler.isMSVC2015():
            self.defaultTarget = 'gitHEAD'
        else:
            self.defaultTarget = releaseVersion

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['testing/llvm'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        if self.buildType().startswith("Rel"):
            # forcing build in Release mode, RelWithDebInfo would take lots of disk space and memory during link
            options += ' -DCMAKE_BUILD_TYPE=Release'
        return options

    def configure(self):
        if compiler.isMinGW() and not self.buildType() == "Release":
            utils.die("You should build clang only in Release mode as it will use up to 10gb disk space if build as RelWithDebInfo, see emerge --buildtype Release")
        return CMakeBuildSystem.configure(self)
