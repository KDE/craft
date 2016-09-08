import os

import info

from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import CMakePackageBase
from Package.PackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ "3.2.1" ]:
            self.targets[ver] = "https://github.com/winlibs/libffi/archive/libffi-%s.tar.gz" % ver
            self.archiveNames[ver] = "libffi-libffi-%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = "libffi-libffi-%s" % ver
        self.targetDigests['3.2.1'] = (['9f8e1133c6b9f72b73943103414707a1970e2e9b1d332c3df0d35dac1d9917e5'], EmergeHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.2.1"

    def setDependencies( self ):
        if compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


class PackageCMake(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

        toolset = ""
        if compiler.isMSVC2013():
            toolset = "vc12"
        elif compiler.isMSVC2015():
            toolset = "vc14"
        self.arch = "x86"
        if compiler.isX64():
            self.arch = "x64"
        self.msvcDir = os.path.join(self.sourceDir(), "win32", "%s_%s" % (toolset, self.arch))


        if self.buildType() == "Debug":
            self.bt = "Debug"
        else:
            self.bt = "Release"

    def configure(self):
        return True

    def make(self):
        self.enterSourceDir()

        return utils.system("msbuild /m /t:Rebuild \"%s\" /p:Configuration=%s " %
                (os.path.join(self.msvcDir, "libffi-msvc.sln"), self.bt)
        )

    def install(self):
        os.makedirs(os.path.join(self.imageDir(), "lib"))
        utils.copyFile(os.path.join(self.msvcDir, self.arch, self.bt, "libffi.lib"), os.path.join(self.imageDir(), "lib", "libffi.lib"), False)
        utils.copyDir(os.path.join(self.sourceDir(), "include"), os.path.join(self.imageDir(), "include"), False)
        return True


from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__( self ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = "--enable-shared --disable-static "

if compiler.isMinGW():
    class Package(PackageMSys): pass
else:
    class Package(PackageCMake): pass

