#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# definitions for the qmake build system

from Blueprints.CraftPackageObject import *
from Blueprints.CraftVersion import CraftVersion
from BuildSystem.BuildSystemBase import *


class QMakeBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "qmake")
        self._platform = None

    @property
    def __qtBase(self):
        return CraftPackageObject.get("libs/qt5/qtbase").instance

    @property
    def platform(self):
        if not self._platform:
            if OsUtils.isWin():
                if CraftCore.compiler.isMSVC():
                    _compiler = "msvc"
                    if CraftCore.compiler.isClang():
                        self._platform = f"win32-clang-{_compiler}"
                    else:
                        self._platform = f"win32-{_compiler}"
                elif CraftCore.compiler.isMinGW():
                    self._platform = "win32-g++"
                else:
                    CraftCore.log.critical(f"QMakeBuildSystem: unsupported compiler platform {CraftCore.compiler}")
            elif OsUtils.isUnix():
                if OsUtils.isMac():
                    osPart = "macx"
                elif OsUtils.isFreeBSD():
                    osPart = "freebsd"
                else:
                    osPart = "linux"

                if CraftCore.compiler.isClang():
                    compilerPart = "clang"
                else:
                    compilerPart = f"g++"
                self._platform = osPart + "-" + compilerPart
        return self._platform

    def configure(self, configureDefines=""):
        """inplements configure step for Qt projects"""
        self.enterBuildDir()

        proFile = self.configureSourceDir()
        if self.subinfo.options.configure.projectFile:
            proFile = os.path.join(self.configureSourceDir(), self.subinfo.options.configure.projectFile)
        return utils.system(Arguments(["qmake", "-makefile", proFile, self.configureOptions(configureDefines)]))

    def make(self):
        """implements the make step for Qt projects"""
        self.enterBuildDir()
        return utils.system(Arguments([self.makeProgram, self.makeOptions(self.subinfo.options.make.args)]))

    def install(self, options=None):
        """implements the make step for Qt projects"""
        if not BuildSystemBase.install(self):
            return False
        return utils.system(
            Arguments(
                [
                    self.makeProgram,
                    options,
                    self.makeOptions(self.subinfo.options.install.args),
                ]
            ),
            cwd=self.buildDir(),
        )

    def runTest(self):
        """running qmake based unittests"""
        return True

    def configureOptions(self, defines=""):
        """returns default configure options"""
        buildReleaseAndDebug = self.__qtBase.subinfo.options.dynamic.buildReleaseAndDebug
        if self.buildType() == "Release" or self.buildType() == "RelWithDebInfo":
            defines += ' "CONFIG -= debug"' if not buildReleaseAndDebug else ' "CONFIG += debug"'
            defines += ' "CONFIG += release"'
        elif self.buildType() == "Debug":
            defines += ' "CONFIG += debug"'
            defines += ' "CONFIG -= release"' if not buildReleaseAndDebug else ' "CONFIG += release"'

        return BuildSystemBase.configureOptions(self, defines)

    def ccacheOptions(self):
        return f' "QMAKE_CC=ccache {os.environ["CC"]}" "QMAKE_CXX=ccache {os.environ["CXX"]}" "CONFIG -= precompile_header" '

    def clangOptions(self):
        if OsUtils.isUnix():
            return ' "CONFIG -= precompile_header" '
        return ""
