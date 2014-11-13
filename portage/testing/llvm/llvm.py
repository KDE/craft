# -*- coding: utf-8 -*-
from BuildSystem import CMakeBuildSystem
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "http://llvm.org/svn/llvm-project/llvm/trunk"
        self.targets[ "3.5.0" ] = "http://llvm.org/releases/3.5.0/llvm-3.5.0.src.tar.xz"
        self.targetInstSrc[ "3.5.0" ] = "llvm-3.5.0.src"
        self.targetDigests['3.5.0'] = '58d817ac2ff573386941e7735d30702fe71267d5'
        self.defaultTarget = "3.5.0"

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        # this program needs python 2.7
        self.subinfo.options.configure.defines = "-DPYTHON_EXECUTABLE=%s/python.exe" % emergeSettings.get("Paths","PYTHON27","").replace("\\","/")

    def configure(self):
        if not ("Paths","Python27") in emergeSettings:
            utils.die("Please make sure Paths/Python27 is set in your kdesettings.ini")
        return CMakeBuildSystem.configure(self)