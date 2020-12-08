#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides cmake build system"""

from BuildSystem.BuildSystemBase import *
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs
from Utils.PostInstallRoutines import *
from Utils.Arguments import Arguments

import os


class CMakeBuildSystem(BuildSystemBase):
    """ cmake build support """

    def __init__(self):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self, "cmake")
        self.supportsNinja = True

    def __makeFileGenerator(self):
        """return cmake related make file generator"""
        if self.makeProgram == "ninja":
            return "Ninja"
        if OsUtils.isWin():
            if CraftCore.compiler.isMSVC() and not CraftCore.compiler.isIntel():
                return "NMake Makefiles"
            if CraftCore.compiler.isMinGW():
                return "MinGW Makefiles"
        elif OsUtils.isUnix():
            return "Unix Makefiles"
        else:
            CraftCore.log.critical(f"unknown {CraftCore.compiler} compiler")

    def configureOptions(self, defines=""):
        """returns default configure options"""
        craftRoot = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        options = Arguments([defines])
        options += [
                    "-DBUILD_TESTING={testing}".format(testing="ON" if self.buildTests else "OFF"),
                    BuildSystemBase.configureOptions(self),
                    f"-DCMAKE_INSTALL_PREFIX={craftRoot}",
                    f"-DCMAKE_PREFIX_PATH={craftRoot}"
                ]

        if self.buildType() is not None:
            options.append(f"-DCMAKE_BUILD_TYPE={self.buildType()}")

        #if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative():
        #    options += " -DCMAKE_TOOLCHAIN_FILE=%s" % os.path.join(CraftStandardDirs.craftRoot(), "craft", "bin", "toolchains", "Toolchain-cross-mingw32-linux-%s.cmake" % CraftCore.compiler.architecture)

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            options.append("-DKDE_L10N_AUTO_TRANSLATIONS=ON")

        if CraftCore.compiler.isWindows:
            # people use InstallRequiredSystemLibraries.cmake wrong and unconditionally install the
            # msvc crt...
            options.append("-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=ON")
        elif CraftCore.compiler.isMacOS:
            options += [f"-DKDE_INSTALL_BUNDLEDIR={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/Applications/KDE", "-DAPPLE_SUPPRESS_X11_WARNING=ON"]
        elif CraftCore.compiler.isLinux:
            # use the same lib dir on all distributions
            options += ["-DCMAKE_INSTALL_LIBDIR=lib"]

        if CraftCore.compiler.isWindows or CraftCore.compiler.isMacOS:
            options.append("-DKDE_INSTALL_USE_QT_SYS_PATHS=ON")

        if self.subinfo.options.buildTools:
            options += self.subinfo.options.configure.toolsDefine
        if self.subinfo.options.buildStatic and self.subinfo.options.configure.staticArgs:
            options += self.subinfo.options.configure.staticArgs
        if CraftCore.compiler.isIntel():
            # this is needed because otherwise it'll detect the MSVC environment
            options += " -DCMAKE_CXX_COMPILER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                      "icl.exe").replace("\\", "/")
            options += " -DCMAKE_C_COMPILER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                    "icl.exe").replace("\\", "/")
            options += " -DCMAKE_LINKER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                "xilink.exe").replace("\\", "/")
        options += ["-S", self.configureSourceDir()]
        return options

    def configure(self, defines=""):
        """implements configure step for cmake projects"""

        self.enterBuildDir()
        env = {}
        print(self.supportsCCACHE and CraftCore.cache.findApplication("ccache"), self.supportsCCACHE , CraftCore.cache.findApplication("ccache"))
        if self.supportsCCACHE and CraftCore.cache.findApplication("ccache"):
            env["PATH"] = os.pathsep.join([str(CraftCore.standardDirs.craftRoot()/ "dev-utils/ccache/bin"), os.environ["PATH"]])
        with utils.ScopedEnv(env):
            command = Arguments.formatCommand(["cmake", "-G",  self.__makeFileGenerator()], self.configureOptions(defines))
            return utils.system(command)

    def make(self):
        """implements the make step for cmake projects"""

        self.enterBuildDir()

        command = Arguments.formatCommand([self.makeProgram], self.makeOptions(self.subinfo.options.make.args))
        return utils.system(command)

    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False

        self.enterBuildDir()


        with utils.ScopedEnv({"DESTDIR" : self.installDir()}):
            command = Arguments.formatCommand([self.makeProgram], self.makeOptions(self.subinfo.options.install.args))
            return (utils.system(" ".join(command)) and
                    self._fixInstallPrefix())

    def unittest(self):
        """running cmake based unittests"""

        self.enterBuildDir()

        command = ["ctest", "--output-on-failure", "--timeout", "300", "-j", str(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count()))]
        if CraftCore.debug.verbose() == 1:
            command += ["-V"]
        elif CraftCore.debug.verbose() > 1:
            command += ["-VV"]
        return utils.system(command)

    def internalPostQmerge(self):
        if not super().internalPostQmerge():
            return False
        return PostInstallRoutines.updateSharedMimeInfo(self)
