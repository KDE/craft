# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.svnTargets['gitHEAD'] = "git://github.com/martine/ninja.git"        
        for ver in ["1.1.0","1.2.0","1.3.0","1.3.1","1.3.2","1.3.3","1.3.4", "1.4.0"]:
            self.targets[ ver ] = "https://github.com/martine/ninja/archive/v%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = "ninja-%s" % ver
        self.targetDigests['1.2.0'] = '9ce01fdf7815f0fda4e477d7fedcd47a3d0afb51'
        self.patchToApply[ "1.1.0" ] = [("0001-if-windows-and-not-msvc-set-platform-to-mingw.patch",1)]
        self.targetDigests['1.3.4'] = 'e6ac7d49b2b5913956ad6740c8612981183808af'
        self.targetDigests['1.4.0'] = '3ab2fcb71e9f70c19cda2d63983cdfe0f971d04f'
        self.patchToApply['1.4.0'] = [("0001-Fix-compilation-on-VS2013.patch", 1),
                                      ("0002-Fix-up-platform_helper-for-MSVC-with-Python-2.6.8-th.patch", 1),
                                      ("0003-fixed-platform_helper.py-msvc_needs_fs-test.patch", 1)]
        self.defaultTarget = '1.4.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.destinationPath = "dev-utils"
        CMakePackageBase.__init__( self )
        
    def configure(self):
        return True
        
    def make(self):
        self.enterSourceDir()
        command = "python bootstrap.py"
        if compiler.isMinGW() and self.subinfo.buildTarget not in ("1.1.0", "1.2.0"):
            command += " --platform=mingw"
        print(command)
        return self.system( command, "make" )
        
    def install(self):
        utils.copyFile(os.path.join(self.sourceDir(),"ninja.exe"),os.path.join(self.imageDir(),"bin","ninja.exe"))
        return True
        
if __name__ == '__main__':
    Package().execute()
