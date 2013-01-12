# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.svnTargets['gitHEAD'] = "git://github.com/martine/ninja.git"        
        self.patchToApply['gitHEAD'] = [("0001-if-windows-and-not-msvc-set-platform-to-mingw.patch",1)]
        for ver in ["1.1.0"]:
            self.svnTargets[ ver ] = "git://github.com/martine/ninja.git||v%s" % ver
            self.patchToApply[ ver ] = [("0001-if-windows-and-not-msvc-set-platform-to-mingw.patch",1)]
        self.defaultTarget = '1.1.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
    def configure(self):
        return True
        
    def make(self):
        self.enterSourceDir()
        command = "python bootstrap.py"
        return self.system( command, "make" )
        
    def install(self):
        utils.copyFile(os.path.join(self.sourceDir(),"ninja.exe"),os.path.join(self.imageDir(),"bin","ninja.exe"))
        return True
        
if __name__ == '__main__':
    Package().execute()
