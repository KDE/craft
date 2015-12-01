# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]http://llvm.org/git/llvm.git|release_37"
        releaseVersion = "3.7.0"
        self.targets[releaseVersion] = "http://llvm.org/releases/" + releaseVersion + "/llvm-" + releaseVersion + ".src.tar.xz"
        self.targetInstSrc[releaseVersion] = "llvm-" + releaseVersion + ".src"
        self.targetDigests['3.7.0'] = '0355c2fe01a8d17c3315069e6f2ef80c281e7dad'
        self.defaultTarget = releaseVersion

        if compiler.isMSVC2015():
            self.defaultTarget = 'gitHEAD'
        else:
            self.defaultTarget = releaseVersion

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DLLVM_TARGETS_TO_BUILD="CppBackend;X86"'

    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        if self.buildType().startswith("Rel"):
            # forcing build in Release mode, RelWithDebInfo would take lots of disk space (around 10 G) and memory during link
            options += ' -DCMAKE_BUILD_TYPE=Release'
        return options

    def configure(self):
        return CMakeBuildSystem.configure(self)
