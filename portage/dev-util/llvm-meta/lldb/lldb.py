# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues(  )

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['dev-util/llvm'] = 'default'
        self.dependencies['dev-util/clang'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines ="-DLLDB_PATH_TO_LLVM_BUILD=\"%s\"" % portage.getPackageInstance('dev-util', 'llvm').buildDir().replace("\\", "/")
        self.subinfo.options.configure.defines +=" -DLLDB_PATH_TO_CLANG_BUILD=\"%s\"" % portage.getPackageInstance('dev-util', 'clang').buildDir().replace("\\", "/")



    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        if self.buildType().startswith("Rel"):
            # forcing build in Release mode, RelWithDebInfo would take lots of disk space (around 10 G) and memory during link
            options += ' -DCMAKE_BUILD_TYPE=Release'
        return options
