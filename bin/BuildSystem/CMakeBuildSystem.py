#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides cmake build system"""

from BuildSystem.BuildSystemBase import *
from CraftCompiler import craftCompiler
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs


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
            if craftCompiler.isMSVC() and not (
                self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE) or craftCompiler.isIntel():
                return "NMake Makefiles"
            else:
                if craftCompiler.isMSVC2017():
                    return "Visual Studio 15 2017" + (" Win64" if craftCompiler.isX64() else "")
                elif craftCompiler.isMSVC2015():
                    return "Visual Studio 14 2015" + (" Win64" if craftCompiler.isX64() else "")
                elif craftCompiler.isMSVC2010():
                    return "Visual Studio 10"
            if craftCompiler.isMinGW():
                return "MinGW Makefiles"
        elif OsUtils.isUnix():
            return "Unix Makefiles"
        else:
            craftDebug.log.critical(f"unknown {craftCompiler} compiler")

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

    def __slnFileName(self):
        """ return solution file name """
        slnname = "%s.sln" % self.package
        if os.path.exists(os.path.join(self.buildDir(), slnname)):
            return slnname
        topLevelCMakeList = os.path.join(self.configureSourceDir(), "CMakeLists.txt")
        if os.path.exists(topLevelCMakeList):
            with open(topLevelCMakeList, 'r') as f:
                lines = f.read().splitlines()
            for line in lines:
                if line.find("project(") > -1:
                    a = line.split("(")
                    a = a[1].split(")")
                    slnname = "%s.sln" % a[0].strip()
        if os.path.exists(os.path.join(self.buildDir(), slnname)):
            return slnname
        slnname = "%s.sln" % self.subinfo.options.make.slnBaseName
        if os.path.exists(os.path.join(self.buildDir(), slnname)):
            return slnname
        return "NO_NAME_FOUND"

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)

        ## \todo why is it required to replace \\ by / ?
        options += " -DCMAKE_INSTALL_PREFIX=\"%s\"" % self.mergeDestinationDir().replace("\\", "/")

        options += " -DCMAKE_PREFIX_PATH=\"%s\"" % \
                   self.mergeDestinationDir().replace("\\", "/")

        if (not self.buildType() == None):
            options += " -DCMAKE_BUILD_TYPE=%s" % self.buildType()

        if craftCompiler.isGCC() and not craftCompiler.isNative():
            options += " -DCMAKE_TOOLCHAIN_FILE=%s" % os.path.join(CraftStandardDirs.craftRoot(), "craft", "bin",
                                                                   "toolchains",
                                                                   "Toolchain-cross-mingw32-linux-%s.cmake" % craftCompiler.architecture)

        if OsUtils.isWin():
            options += " -DKDE_INSTALL_USE_QT_SYS_PATHS=ON"

        if OsUtils.isMac():
            options += " -DKDE_INSTALL_BUNDLEDIR=\"%s/Applications/KDE\" -DAPPLE_SUPPRESS_X11_WARNING=ON" % \
                       self.mergeDestinationDir().replace("\\", "/")

        if not self.buildTests:
            options += " -DBUILD_TESTING=OFF "

        if self.subinfo.options.buildTools:
            options += " " + self.subinfo.options.configure.toolsDefine + " "
        if self.subinfo.options.buildStatic and self.subinfo.options.configure.staticArgs:
            options += " " + self.subinfo.options.configure.staticArgs + " "
        if self.subinfo.options.configure.onlyBuildTargets:
            options += self.__onlyBuildDefines(self.subinfo.options.configure.onlyBuildTargets)
        if self.subinfo.options.cmake.useCTest:
            options += " -DCMAKE_PROGRAM_PATH=\"%s\" " % \
                       (os.path.join(self.mergeDestinationDir(), "dev-utils", "svn", "bin").replace("\\", "/"))
        if craftCompiler.isIntel():
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
        craftDebug.step(command)

        with open(os.path.join(self.buildDir(), "cmake-command.bat"), "w") as fc:
            fc.write(command)

        return self.system(command, "configure", 0)

    def make(self):
        """implements the make step for cmake projects"""

        self.enterBuildDir()

        if self.subinfo.options.cmake.openIDE:
            if craftCompiler.isMSVC2010():
                command = "start vcexpress %s" % self.__slnFileName()
        elif self.subinfo.options.cmake.useIDE:
            if craftCompiler.isMSVC2015():
                command = "msbuild /maxcpucount %s /t:ALL_BUILD /p:Configuration=\"%s\"" % (
                self.__slnFileName(), self.buildType())
            elif craftCompiler.isMSVC2010():
                craftDebug.log.critical("has to be implemented");
        elif self.subinfo.options.cmake.useCTest:
            # first make clean
            self.system(self.makeProgram + " clean", "make clean")
            command = "ctest -M " + "Nightly" + " -T Start -T Update -T Configure -T Build -T Submit"
        else:
            command = ' '.join([self.makeProgram, self.makeOptions()])

        return self.system(command, "make")

    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False

        self.enterBuildDir()

        env = os.environ
        if self.subinfo.options.install.useMakeToolForInstall:
            if craftCompiler.isMSVC2015() and (self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):
                command = "msbuild INSTALL.vcxproj /p:Configuration=\"%s\"" % self.buildType()
            else:
                env["DESTDIR"] = self.installDir()
                command = f"{self.makeProgram} install"
        else:
            command = "cmake -DCMAKE_INSTALL_PREFIX=%s -P cmake_install.cmake" % self.installDir()

        if not self.system(command, "install", env=env):
            return False

        if self.subinfo.options.install.useMakeToolForInstall and not (
            self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):
            self._fixCmakeImageDir(self.installDir(), self.mergeDestinationDir())
        return True

    def unittest(self):
        """running cmake based unittests"""

        self.enterBuildDir()

        return self.system("ctest --output-on-failure")

    def ccacheOptions(self):
        out = " -DCMAKE_CXX_COMPILER=ccache -DCMAKE_CXX_COMPILER_ARG1=g++ "
        out += " -DCMAKE_C_COMPILER=ccache -DCMAKE_C_COMPILER_ARG1=gcc "
        return out

    def clangOptions(self):
        if craftCompiler.isMSVC():
            return " -DCMAKE_CXX_COMPILER=clang-cl" \
                   " -DCMAKE_C_COMPILER=clang-cl"
            return out
        else:
            return " -DCMAKE_CXX_COMPILER=/usr/bin/clang++" \
                   " -DCMAKE_C_COMPILER=/usr/bin/clang"

    def _fixCmakeImageDir(self, imagedir, rootdir):
        """
        when using DESTDIR=foo under windows, it does not _replace_
        CMAKE_INSTALL_PREFIX with it, but prepends destdir to it.
        so when we want to be able to install imagedir into KDEROOT,
        we have to move things around...
        """
        craftDebug.log.debug("fixImageDir: %s %s" % (imagedir, rootdir))
        # imagedir = e:\foo\thirdroot\tmp\dbus-0\image
        # rootdir  = e:\foo\thirdroot
        # files are installed to
        # e:\foo\thirdroot\tmp\dbus-0\image\foo\thirdroot
        _, rootpath = os.path.splitdrive(rootdir)
        # print "rp:", rootpath
        if (rootpath.startswith(os.path.sep)):
            rootpath = rootpath[1:]
        # CMAKE_INSTALL_PREFIX = X:\
        # -> files are installed to
        # x:\build\foo\dbus\image\
        # --> all fine in this case
        # print("rp:", rootpath)
        if len(rootpath) == 0:
            return

        tmp = os.path.join(imagedir, rootpath)
        if os.path.exists(tmp):
            utils.mergeTree(tmp, imagedir)
            utils.rmtree(os.path.join(tmp, rootpath.split(os.path.pathsep)[0]))
        if craftSettings.getboolean("QtSDK", "Enabled", "False"):
            qtDir = os.path.join(craftSettings.get("QtSDK", "Path"), craftSettings.get("QtSDK", "Version"),
                                 craftSettings.get("QtSDK", "Compiler"))
            # drop the drive letter and the first slash [3:]
            path = os.path.join(imagedir, qtDir[3:])
            if os.path.exists(path):
                utils.mergeTree(path, imagedir)
                utils.rmtree(os.path.join(imagedir, craftSettings.get("QtSDK", "Path")[3:]))
