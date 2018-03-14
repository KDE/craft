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

    def __onlyBuildDefines(self, buildOnlyTargets):
        """This method returns a list of cmake defines to exclude targets from build"""
        defines = ""
        topLevelCMakeList = os.path.join(self.sourceDir(), "CMakeLists.txt")
        if os.path.exists(topLevelCMakeList):
            with open(topLevelCMakeList, 'r') as f:
                lines = f.read().splitlines()
            for line in lines:
                if line.find("macro_optional_add_subdirectory") > -1:
                    a = line.split("(")
                    a = a[1].split(")")
                    subdir = a[0].strip()
                    if not subdir in buildOnlyTargets:
                        defines += " -DBUILD_%s=OFF" % subdir
        # print defines
        return defines

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = "-DBUILD_TESTING={testing} ".format(testing="ON" if self.buildTests else "OFF")
        options += BuildSystemBase.configureOptions(self)

        options += f" -DCMAKE_INSTALL_PREFIX=\"{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}\""

        if (not self.buildType() == None):
            options += " -DCMAKE_BUILD_TYPE=%s" % self.buildType()

        if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative():
            options += " -DCMAKE_TOOLCHAIN_FILE=%s" % os.path.join(CraftStandardDirs.craftRoot(), "craft", "bin",
                                                                   "toolchains",
                                                                   "Toolchain-cross-mingw32-linux-%s.cmake" % CraftCore.compiler.architecture)

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            options += " -DKDE_L10N_AUTO_TRANSLATIONS=ON"

        if OsUtils.isWin():
            options += " -DKDE_INSTALL_USE_QT_SYS_PATHS=ON"
            # people use InstallRequiredSystemLibraries.cmake wrong and unconditionally install the
            # msvc crt...
            options += " -DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=ON"

        if OsUtils.isMac():
            options += f" -DKDE_INSTALL_BUNDLEDIR=\"{OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/Applications/KDE\" -DAPPLE_SUPPRESS_X11_WARNING=ON"

        if self.subinfo.options.buildTools:
            options += " " + self.subinfo.options.configure.toolsDefine + " "
        if self.subinfo.options.buildStatic and self.subinfo.options.configure.staticArgs:
            options += " " + self.subinfo.options.configure.staticArgs + " "
        if self.subinfo.options.configure.onlyBuildTargets:
            options += self.__onlyBuildDefines(self.subinfo.options.configure.onlyBuildTargets)
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

        env = os.environ
        env["DESTDIR"] = self.installDir()
        command = [self.makeProgram, self.makeOptions(self.subinfo.options.install.args)]
        return (utils.system(" ".join(command), env=env) and
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

    def postInstall(self):
        return PostInstallRoutines.updateSharedMimeInfo(self)
