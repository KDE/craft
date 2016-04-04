# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.targetDigests['3.7.0'] = '0355c2fe01a8d17c3315069e6f2ef80c281e7dad'

        for ver in self.svnTargets.keys() | self.targets.keys():
            if ver in ["3.7.0", "3.7.1", "release_37"]:
                self.patchToApply[ ver ] = [("0002-use-DESTDIR-on-windows.patch", 1)]
            if ver in ["release_38"]:
                self.patchToApply[ver] = [("use-DESTDIR-on-windows-3.8.patch", 1)]


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/lld'] = 'default'
        self.buildDependencies['dev-util/clang'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DLLVM_TARGETS_TO_BUILD="X86"'
        self.subinfo.options.configure.defines += " -DLLVM_EXTERNAL_LLD_SOURCE_DIR=\"%s\"" % portage.getPackageInstance('dev-util', 'lld').sourceDir().replace("\\", "/")
        self.subinfo.options.configure.defines += " -DLLVM_EXTERNAL_CLANG_SOURCE_DIR=\"%s\"" % portage.getPackageInstance('dev-util', 'clang').sourceDir().replace("\\", "/")

    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        if self.buildType().startswith("Rel"):
            # forcing build in Release mode, RelWithDebInfo would take lots of disk space (around 10 G) and memory during link
            options += ' -DCMAKE_BUILD_TYPE=Release'
        return options
