# -*- coding: utf-8 -*-
import os

import utils
import info
import compiler


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['53.1'] = 'http://download.icu-project.org/files/icu4c/53.1/icu4c-53_1-src.tgz'
        self.targetDigests['53.1'] = '7eca017fdd101e676d425caaf28ef862d3655e0f'
        self.targetInstSrc['53.1'] = "icu\\source"
        self.defaultTarget = '53.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if compiler.isMinGW():
            self.buildDependencies['dev-util/msys'] = 'default'

from Package.CMakePackageBase import *

class PackageCMake(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

    def configure(self):
        return True

    def make(self):
        self.enterSourceDir()
        if self.buildType() == "Debug":
          bt = "Debug"
        else:
          bt = "Release"
          
        utils.system("devenv \"%s\" /upgrade" % (os.path.join(self.sourceDir(), "allinone", "allinone.sln" )) )
        return utils.system("devenv \"%s\" /build %s" % (os.path.join(self.sourceDir(), "allinone", "allinone.sln" ), bt) )

    def install(self):
        utils.copyDir(os.path.join(self.sourceDir(), "..", "bin"), os.path.join(self.imageDir(), "bin"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", "bin64"), os.path.join(self.imageDir(), "bin"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", "include"), os.path.join(self.imageDir(), "include"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", "lib"), os.path.join(self.imageDir(), "lib"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", "lib64"), os.path.join(self.imageDir(), "lib"))
        return True

from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__( self ):
        AutoToolsPackageBase.__init__(self)

    def install(self):
        if not AutoToolsPackageBase.install(self):
            return False
        files = os.listdir(os.path.join( self.installDir() , "lib" ))
        for dll in files:
            if dll.endswith(".dll"):
                utils.copyFile( os.path.join( self.installDir() , "lib" ,dll) , os.path.join( self.installDir(), "bin" ,dll) )
        return True

if compiler.isMinGW():
    class Package(PackageMSys):
        def __init__( self ):
            PackageMSys.__init__( self )
else:
    class Package(PackageCMake):
        def __init__( self ):
            PackageCMake.__init__( self )

