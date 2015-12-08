# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( packageName="llvm" )
        self.targetDigests['3.7.0'] = '0355c2fe01a8d17c3315069e6f2ef80c281e7dad'

        for ver in self.svnTargets.keys() | self.targets.keys():
            self.patchToApply[ ver ] = [("0002-use-DESTDIR-on-windows.patch", 1)]

        for ver in self.svnTargets.keys() :
            self.patchToApply[ ver ] = [("use-DESTDIR-on-windows-3.8.patch", 1)]


        if compiler.isMSVC2015():
            self.defaultTarget = 'release_37'

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
