# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()
        self.targetDigests['3.7.0'] = '2a5e0f6f9d59f9cda41dbe87c4b30f4226c5b5eb'
        
        for ver in self.svnTargets.keys() | self.targets.keys():
            self.patchToApply[ ver ] = [("fix_shortpath.patch", 1)]
        

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
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