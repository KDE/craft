# -*- coding: utf-8 -*-
import utils
import os
import info
import emergePlatform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['49.1.1'] = 'http://download.icu-project.org/files/icu4c/49.1.1/icu4c-49_1_1-src.tgz'
        self.targetInstSrc['49.1.1'] = "icu"
        self.targetDigests['49.1.1'] = 'f407d7e2808b76e3a6ca316aab896aef74bf6722'
        self.defaultTarget = '49.1.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def configure(self):
        return True

    def make(self):
        utils.system("devenv %s /build Release" % os.path.join(self.sourceDir(),"source","allinone","allinone.sln" ))
        return True

    def install(self):
        utils.copyDir(os.path.join(self.sourceDir(),"bin") , os.path.join(self.imageDir(),"bin"))
        utils.copyDir(os.path.join(self.sourceDir(),"include") , os.path.join(self.imageDir(),"include"))
        utils.copyDir(os.path.join(self.sourceDir(),"lib") , os.path.join(self.imageDir(),"lib"))
        return True

if __name__ == '__main__':
    Package().execute()
