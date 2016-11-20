import os

import info

from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import CMakePackageBase
from Package.PackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ "2.49.4" ]:
            self.targets[ver] = "https://github.com/winlibs/glib/archive/glib-%s.tar.gz" % ver
            self.archiveNames[ver] = "glib-glib%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = "glib-glib-%s" % ver
            self.patchToApply[ ver ] = ("glib-glib-2.49.4-20161114.diff", 1)
        self.targetDigests['2.49.4'] = (['936e124d1d147226acd95def54cb1bea5d19dfc534532b85de6727fa68bc310f'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.49.4"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.dependencies["win32libs/libffi"] = "default"
        self.dependencies["win32libs/pcre"] = "default"
        self.dependencies["win32libs/zlib"] = "default"
        self.dependencies["win32libs/gettext"] = "default"
        if compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"

class PackageCMake(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

        self.toolset = ""
        if compiler.isMSVC2013():
            self.toolset = "vs12"
        elif compiler.isMSVC2015():
            self.toolset = "vs14"
        self.msvcDir = os.path.join(self.sourceDir(), "build", "win32", self.toolset)


        if self.buildType() == "Debug":
            self.bt = "Debug"
        else:
            self.bt = "Release"

    def configure(self):
        if not os.path.exists( os.path.join(CraftStandardDirs.craftRoot(), "lib", "libintl_a.lib")):
            utils.copyFile(os.path.join(CraftStandardDirs.craftRoot(), "lib", "libintl.lib"),
                           os.path.join(CraftStandardDirs.craftRoot(), "lib", "libintl_a.lib"))

        if not os.path.exists(os.path.join(CraftStandardDirs.craftRoot(), "lib", "zlib_a.lib")):
            utils.copyFile(os.path.join(CraftStandardDirs.craftRoot(), "lib", "zlib.lib"),
                           os.path.join(CraftStandardDirs.craftRoot(), "lib", "zlib_a.lib"))
        return True

    def make(self):
        self.enterSourceDir()
        utils.putenv("INCLUDE", "%s;%s" % (os.path.join(CraftStandardDirs.craftRoot(), "include"), os.environ["INCLUDE"]))
        utils.putenv("LIB", "%s;%s" % (os.path.join(CraftStandardDirs.craftRoot(), "lib"), os.environ["LIB"]))
        return utils.system("msbuild /m /t:Rebuild \"%s\" /p:Configuration=%s /p:useenv=true " %
                (os.path.join(self.msvcDir, "glib.sln"), self.bt)
        )

    def install(self):
        self.cleanImage()
        arch = "x86"
        if compiler.isX64():
            arch = "x64"
        utils.mergeTree(
            os.path.join(self.sourceDir(), "..", self.toolset, arch, "lib", "glib-2.0", "include"),
            os.path.join(self.sourceDir(), "..", self.toolset, arch, "include", "glib-2.0"))
        utils.copyDir(os.path.join(self.sourceDir(), "..", self.toolset, arch), self.imageDir(), False)
        return True


from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__( self ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = "--enable-shared --disable-static --with-pcre=internal"

    def install( self ):
        if not AutoToolsBuildSystem.install(self):
            return False
        utils.copyFile(os.path.join(self.buildDir(), "glib", "glibconfig.h"),
                       os.path.join(self.imageDir(), "include", "glib-2.0", "glibconfig.h"), False)
        return True

if compiler.isMinGW():
    class Package(PackageMSys): pass
else:
    class Package(PackageCMake): pass

