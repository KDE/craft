# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()
        

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/llvm'] = 'default'
        self.dependencies['dev-util/libcxx'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DLIBCXXABI_ENABLE_SHARED=OFF '


    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        if self.buildType().startswith("Rel"):
            # forcing build in Release mode, RelWithDebInfo would take lots of disk space and memory during link
            options += ' -DCMAKE_BUILD_TYPE=Release'
        return options