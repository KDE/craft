# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Hannah von Reth <vonreth@kde.org>

"""@package provides boost build system"""

from BuildSystem.BuildSystemBase import *
from CraftOS.osutils import OsUtils


class BoostBuildSystem(BuildSystemBase):
    """ cmake build support """

    def __init__(self):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self, "boost")
        self.subinfo.options.package.packSources = False

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)

        if OsUtils.isWin():
            options += " -j" + os.getenv("NUMBER_OF_PROCESSORS")
            options += " --build-dir=" + self.buildDir()
        else:
            # TODO: real value
            options += " install --prefix=%s" % self.buildDir()
            options += " -j10"

        options += (" --build-type=minimal"
                    #                " --debug-configuration"
                    " threading=multi"
                    )

        if not self.subinfo.options.buildStatic:
            options += (" link=shared"
                        " runtime-link=shared")
        else:
            options += (" link=static"
                        " runtime-link=static")
        if craftCompiler.isX64():
            options += " address-model=64 architecture=x86"
        else:
            options += " address-model=32 architecture=x86"

        if self.buildType() == "Debug":
            options += " variant=debug"
        else:
            options += " variant=release"

        options += " toolset="
        if craftCompiler.isClang():
            options += "clang"
            if craftCompiler.isGCC():
                options += " threadapi=pthread"
        elif craftCompiler.isMinGW():
            options += "gcc"
        elif craftCompiler.isMSVC():
            platform = str(craftCompiler.getMsvcPlatformToolset())
            if craftCompiler.isMSVC2017():
                options += f"msvc-{platform[:2]}.0"
            else:
                options += f"msvc-{platform[:2]}.{platform[2:]}"
        elif craftCompiler.isIntel():
            options += "intel"
            options += " -sINTEL_PATH=\"%s\"" % os.path.join(os.getenv("INTELDIR"), "bin", os.getenv("TARGET_ARCH"))
            options += " -sINTEL_BASE_MSVC_TOOLSET=vc-%s" % (
            {"vs2008": "9_0", "vs2010": "10_0", "vs2012": "11_0"}[os.getenv("INTEL_VSSHELL")])
            options += " -sINTEL_VERSION=%s" % os.getenv("PRODUCT_NAME")[-2:]
        craftUserConfig = os.path.join(CraftStandardDirs.craftRoot(), "etc", "craft-boost-config.jam")
        if os.path.exists(craftUserConfig):
            options += " --user-config=" + os.path.join(craftUserConfig)
        return options

    def configure(self, defines=""):
        return True

    def make(self):
        """implements the make step for cmake projects"""
        self.boost = CraftPackageObject.instance('win32libs/boost/boost-headers')
        self.subinfo.targetInstSrc[self.subinfo.buildTarget] = os.path.join(self.boost.sourceDir(), "libs",
                                                                            self.subinfo.targetInstSrc[
                                                                                self.subinfo.buildTarget], "build")

        self.enterSourceDir()
        cmd = "bjam"
        cmd += self.configureOptions(self.subinfo.options.configure.args)
        craftDebug.log.debug(cmd)
        return self.system(cmd)

    def install(self):
        """install the target"""
        if OsUtils.isUnix():
            if not os.path.exists(self.installDir()):
                os.makedirs(self.installDir())
            utils.copyDir(self.buildDir(), self.installDir())
            return BuildSystemBase.install(self)
        else:
            if not BuildSystemBase.install(self):
                return False

            for root, dirs, files in os.walk(self.buildDir()):
                for f in files:
                    if f.endswith(".dll"):
                        utils.copyFile(os.path.join(root, f), os.path.join(self.imageDir(), "lib", f))
                        utils.copyFile(os.path.join(root, f), os.path.join(self.imageDir(), "bin", f))
                    elif f.endswith(".a") or f.endswith(".lib"):
                        utils.copyFile(os.path.join(root, f), os.path.join(self.imageDir(), "lib", f))

            return True

    def unittest(self):
        return True
