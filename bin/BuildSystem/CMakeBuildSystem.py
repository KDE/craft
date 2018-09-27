#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides cmake build system"""

from BuildSystem.BuildSystemBase import *
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs
from Utils.PostInstallRoutines import *



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
        options = "-DBUILD_TESTING={testing} ".format(testing="ON" if self.buildTests else "OFF")
        options += BuildSystemBase.configureOptions(self)

        craftRoot = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        options += f" -DCMAKE_INSTALL_PREFIX=\"{craftRoot}\""
        options += f" -DCMAKE_PREFIX_PATH=\"{craftRoot}\""

        if (not self.buildType() == None):
            options += " -DCMAKE_BUILD_TYPE=%s" % self.buildType()

        if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative():
            options += " -DCMAKE_TOOLCHAIN_FILE=%s" % os.path.join(CraftStandardDirs.craftRoot(), "craft", "bin",
                                                                   "toolchains",
                                                                   "Toolchain-cross-mingw32-linux-%s.cmake" % CraftCore.compiler.architecture)

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            options += " -DKDE_L10N_AUTO_TRANSLATIONS=ON"

        if OsUtils.isWin():
            # people use InstallRequiredSystemLibraries.cmake wrong and unconditionally install the
            # msvc crt...
            options += " -DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=ON"

        if OsUtils.isMac():
            options += f" -DKDE_INSTALL_BUNDLEDIR=\"{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/Applications/KDE\" -DAPPLE_SUPPRESS_X11_WARNING=ON"
            if CraftCore.compiler.macUseSDK:
                # Ensure that we don't depend on SDK features only present on newer systems
                options += " -DCMAKE_OSX_DEPLOYMENT_TARGET=" + CraftCore.compiler.macOSDeploymentTarget

        if CraftCore.compiler.isWindows or CraftCore.compiler.isMacOS:
            options += " -DKDE_INSTALL_USE_QT_SYS_PATHS=ON"

        if self.subinfo.options.buildTools:
            options += " " + self.subinfo.options.configure.toolsDefine + " "
        if self.subinfo.options.buildStatic and self.subinfo.options.configure.staticArgs:
            options += " " + self.subinfo.options.configure.staticArgs + " "
        if CraftCore.compiler.isMSVC():
                options += " -DCMAKE_VS_PLATFORM_TOOLSET={0}".format(CraftCore.compiler.getMsvcPlatformToolset())
                if "WINDOWSSDKVERSION" in os.environ:
                    options += " -DCMAKE_VS_WINDOWS_TARGET_PLATFORM_VERSION={0}".format(os.environ["WINDOWSSDKVERSION"].replace("\\", ""))
        if CraftCore.compiler.isIntel():
            # this is needed because otherwise it'll detect the MSVC environment
            options += " -DCMAKE_CXX_COMPILER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                      "icl.exe").replace("\\", "/")
            options += " -DCMAKE_C_COMPILER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                    "icl.exe").replace("\\", "/")
            options += " -DCMAKE_LINKER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                "xilink.exe").replace("\\", "/")
        options += " \"%s\"" % self.configureSourceDir()
        return options

    def configure(self, defines=""):
        """implements configure step for cmake projects"""

        self.enterBuildDir()
        command = r"""cmake -G "%s" %s""" % (self.__makeFileGenerator(), self.configureOptions(defines))
        CraftCore.debug.step(command)

        with open(os.path.join(self.buildDir(), "cmake-command.bat"), "w") as fc:
            fc.write(command)

        return utils.system(command)

    def make(self):
        """implements the make step for cmake projects"""

        self.enterBuildDir()

        command = ' '.join([self.makeProgram, self.makeOptions(self.subinfo.options.make.args)])
        return utils.system(command)

    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False

        self.enterBuildDir()


        with utils.ScopedEnv({"DESTDIR" : self.installDir()}):
            command = [self.makeProgram, self.makeOptions(self.subinfo.options.install.args)]
            return (utils.system(" ".join(command)) and
                    self._fixInstallPrefix())

    def unittest(self):
        """running cmake based unittests"""

        self.enterBuildDir()

        command = ["ctest", "--output-on-failure", "--timeout", "300"]
        if CraftCore.debug.verbose() == 1:
            command += ["-V"]
        elif CraftCore.debug.verbose() > 1:
            command += ["-VV"]
        return utils.system(command)

    def ccacheOptions(self):
        out = " -DCMAKE_CXX_COMPILER=ccache -DCMAKE_CXX_COMPILER_ARG1=g++ "
        out += " -DCMAKE_C_COMPILER=ccache -DCMAKE_C_COMPILER_ARG1=gcc "
        return out

    def clangOptions(self):
        if CraftCore.compiler.isMSVC():
            return " -DCMAKE_CXX_COMPILER=clang-cl" \
                   " -DCMAKE_C_COMPILER=clang-cl"
        else:
            return " -DCMAKE_CXX_COMPILER=/usr/bin/clang++" \
                   " -DCMAKE_C_COMPILER=/usr/bin/clang"

    def internalPostQmerge(self):
        if not super().internalPostQmerge():
            return False
        return PostInstallRoutines.updateSharedMimeInfo(self)
