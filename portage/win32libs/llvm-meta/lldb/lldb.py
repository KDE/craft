# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues(  )

    def setDependencies( self ):
        self.runtimeDependencies['virtual/base'] = 'default'
        self.runtimeDependencies['win32libs/llvm'] = 'default'
        self.runtimeDependencies['win32libs/clang'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args ="-DLLDB_PATH_TO_LLVM_BUILD=\"%s\" -DLLDB_PATH_TO_LLVM_SOURCE=\"%s\"" % (CraftStandardDirs.craftRoot().replace("\\", "/"), portage.PortageInstance.getPackageInstance('win32libs', 'llvm').sourceDir().replace("\\", "/"))
        self.subinfo.options.configure.args +=" -DLLDB_PATH_TO_CLANG_BUILD=\"%s\" -DLLDB_PATH_TO_CLANG_SOURCE=\"%s\"" % (CraftStandardDirs.craftRoot().replace("\\", "/"), portage.PortageInstance.getPackageInstance('win32libs', 'clang').sourceDir().replace("\\", "/"))



    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        if self.buildType().startswith("Rel"):
            # forcing build in Release mode, RelWithDebInfo would take lots of disk space (around 10 G) and memory during link
            options += ' -DCMAKE_BUILD_TYPE=Release'
        return options
