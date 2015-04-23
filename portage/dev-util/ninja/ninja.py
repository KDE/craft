# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.svnTargets['gitHEAD'] = "git://github.com/martine/ninja.git"        
        for ver in ["1.5.3" ]:
            self.targets[ ver ] = "https://github.com/martine/ninja/archive/v%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = "ninja-%s" % ver
        self.targetDigests['1.5.3'] = 'b3ff794461ff5e4e1e73fe6bd11e653bbe509e63'
        self.patchToApply['1.5.3'] = ("ninja-1.5.3-20141203.diff",1)

        if compiler.isMSVC2015():
            self.defaultTarget = 'gitHEAD'
        else:
            self.defaultTarget = '1.5.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.merge.destinationPath = "dev-utils"

    def configure(self):
        return True
        
    def make(self):
        self.enterSourceDir()
        command = "python configure.py --bootstrap"
        if compiler.isMinGW() and self.subinfo.buildTarget not in ("1.1.0", "1.2.0"):
            command += " --platform=mingw"
        print(command)
        return self.system( command, "make" )
        
    def install(self):
        utils.copyFile(os.path.join(self.sourceDir(),"ninja.exe"),os.path.join(self.imageDir(),"bin","ninja.exe"))
        return True
        
