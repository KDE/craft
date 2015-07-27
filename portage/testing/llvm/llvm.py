# -*- coding: utf-8 -*-
from BuildSystem import CMakeBuildSystem
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "http://llvm.org/git/llvm.git"
        releaseVersion = "3.6.2"
        self.targets[releaseVersion] = "http://llvm.org/releases/" + releaseVersion + "/llvm-" + releaseVersion + ".src.tar.xz"
        self.targetInstSrc[releaseVersion] = "llvm-" + releaseVersion + ".src"
        self.targetDigests[releaseVersion] = '7a00257eb2bc9431e4c77c3a36b033072c54bc7e'
        self.defaultTarget = releaseVersion

    def setBuildOptions(self):
        info.infoclass.setBuildOptions(self)

        self.options.configure.defines = '-DLLVM_TARGETS_TO_BUILD="X86"'

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        # this program needs python 2.7
        self.subinfo.options.configure.defines += " -DPYTHON_EXECUTABLE=%s/python.exe" % emergeSettings.get("Paths","PYTHON27","").replace("\\","/")

    def configure(self):
        if not ("Paths","Python27") in emergeSettings:
            utils.die("Please make sure Paths/Python27 is set in your kdesettings.ini")
        if compiler.isMinGW() and not self.buildType() == "Release":
            utils.die("You should build clang only in Release mode as it will use up to 10gb disk space if build as RelWithDebInfo, see emerge --buildtype Release")
        return CMakeBuildSystem.configure(self)
