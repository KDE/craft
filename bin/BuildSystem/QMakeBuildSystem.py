#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# definitions for the qmake build system

from BuildSystem.BuildSystemBase import *
from Blueprints.CraftPackageObject import *
from Blueprints.CraftVersion import CraftVersion


class QMakeBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "qmake")
        self._platform = None
        self._qtVer = None
        self.subinfo.options.needsShortPath |= CraftCore.compiler.isMinGW()

    @property
    def __qtBase(self):
        return CraftPackageObject.get("libs/qt5/qtbase").instance

    @property
    def qtVer(self):
        if not self._qtVer:
            self._qtVer = CraftVersion(self.__qtBase.subinfo.buildTarget if self.__qtBase.subinfo.buildTarget != "dev" else "5.9999")
        return self._qtVer

    @property
    def platform(self):
        if not self._platform:
            if OsUtils.isWin():
                if CraftCore.compiler.isMSVC():
                    if self.qtVer < CraftVersion("5.8"):
                        if CraftCore.compiler.isMSVC2017():
                            _compiler = "msvc2015"
                        else:
                            _compiler = CraftCore.compiler.abi.split("_")[0]
                    else:
                        _compiler = "msvc"
                    if CraftCore.compiler.isClang():
                        self._platform = f"win32-clang-{_compiler}"
                    else:
                        self._platform = f"win32-{_compiler}"
                elif CraftCore.compiler.isMinGW():
                    self._platform = "win32-g++"
                elif CraftCore.compiler.isIntel():
                    self._platform = "win32-icc"
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
                    compilerPart = f"g++-{CraftCore.compiler.bits}"
                self._platform = osPart + "-" + compilerPart
        return self._platform

    def configure(self, configureDefines=""):
        """inplements configure step for Qt projects"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        proFile = self.configureSourceDir()
        if self.subinfo.options.configure.projectFile:
            proFile = os.path.join(self.configureSourceDir(), self.subinfo.options.configure.projectFile)
        command = "%s -makefile %s %s" % (CraftCore.cache.findApplication("qmake"), proFile, self.configureOptions(configureDefines))

        return utils.system(command)

    def make(self):
        """implements the make step for Qt projects"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        options = self.makeOptions(self.subinfo.options.make.args)
        command = ' '.join([self.makeProgram, options])
        return utils.system(command)

    def install(self, options=None):
        """implements the make step for Qt projects"""
        if not options:
            options = self.makeOptions(self.subinfo.options.install.args)
        if not BuildSystemBase.install(self):
            return False
        if not self.subinfo.options.useShadowBuild:
            cwd = self.sourceDir()
        else:
            cwd = self.buildDir()
        return utils.system(f"{self.makeProgram} {options}", cwd=cwd)

    def runTest(self):
        """running qmake based unittests"""
        return True

    def configureOptions(self, defines=""):
        """returns default configure options"""
        defines += BuildSystemBase.configureOptions(self, defines)

        buildReleaseAndDebug = self.__qtBase.subinfo.options.dynamic.buildReleaseAndDebug
        if self.buildType() == "Release" or self.buildType() == "RelWithDebInfo":
            defines += ' "CONFIG -= debug"' if not buildReleaseAndDebug else ' "CONFIG += debug"'
            defines += ' "CONFIG += release"'
        elif self.buildType() == "Debug":
            defines += ' "CONFIG += debug"'
            defines += ' "CONFIG -= release"' if not buildReleaseAndDebug else ' "CONFIG += release"'

        return defines

    def ccacheOptions(self):
        return ' "QMAKE_CC=ccache gcc" "QMAKE_CXX=ccache g++" "CONFIG -= precompile_header" '

    def clangOptions(self):
        if OsUtils.isUnix():
            return ' "CONFIG -= precompile_header" '
        return ''
