# -*- coding: utf-8 -*-
import os

import utils
import info
import compiler


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['53.1', '55.1']:
            self.targets[ver] = 'http://download.icu-project.org/files/icu4c/%s/icu4c-%s-src.tgz' % ( ver, ver.replace(".", "_"))
            self.targetInstSrc[ver] = "icu\\source"
        self.targetDigests['53.1'] = '7eca017fdd101e676d425caaf28ef862d3655e0f'
        self.targetDigests['55.1'] = '3bb301c11be0e239c653e8aa2925c53f6f4dc88d'
        self.defaultTarget = '53.1'
        if compiler.isMSVC2015():
            self.patchToApply['55.1'] = ("icu-20150414.diff", 1)
            self.defaultTarget = '55.1'
            

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

        toolsetSwitches = ""
        if compiler.isMSVC2012():
            toolsetSwitches = "/property:PlatformToolset=v110"
        elif compiler.isMSVC2013():
            toolsetSwitches = "/tv:12.0 /property:PlatformToolset=v120"
        elif compiler.isMSVC2015():
            toolsetSwitches = "/tv:14.0 /property:PlatformToolset=v140"
          
        return utils.system("msbuild /t:Rebuild \"%s\" /p:Configuration=%s %s" %
                (os.path.join(self.sourceDir(), "allinone", "allinone.sln"), bt, toolsetSwitches)
        )

    def install(self):
        utils.copyDir(os.path.join(self.sourceDir(), "..", "bin"), os.path.join(self.imageDir(), "bin"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", "bin64"), os.path.join(self.imageDir(), "bin"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", "include"), os.path.join(self.imageDir(), "include"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", "lib"), os.path.join(self.imageDir(), "lib"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", "lib64"), os.path.join(self.imageDir(), "lib"))

        if compiler.isMSVC() and self.buildType() == "Debug":
            imagedir = os.path.join( self.installDir(), "lib" )
            filelist = os.listdir( imagedir )
            for f in filelist:
                if f.endswith( "d.lib" ):
                    utils.copyFile( os.path.join( imagedir, f ), os.path.join( imagedir, f.replace( "d.lib", ".lib" ) ) )

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

