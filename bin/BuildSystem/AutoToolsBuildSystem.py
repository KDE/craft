# -*- coding: utf-8 -*-
# definitions for the autotools build system

import glob
import os
import stat
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from shells import BashShell
from Utils.Arguments import Arguments


class AutoToolsBuildSystem(BuildSystemBase):
    def __init__(self, package: CraftPackageObject):
        BuildSystemBase.__init__(self, package, "autotools")
        self._shell = BashShell()
        self.platform = Arguments()  # hope for auto detection
        if (
            CraftCore.compiler.platform.isLinux
            and CraftCore.compiler.compiler.isGCC
            and not CraftCore.compiler.architecture.isNative
            and CraftCore.compiler.architecture.isX86_32
        ):
            self.platform = Arguments(["--host=i686-pc-linux-gnu"])
        elif CraftCore.compiler.platform.isWindows:
            if CraftCore.compiler.architecture.isX86_32:
                self.platform = Arguments(
                    [
                        "--host=i686-w64-mingw32",
                        "--build=i686-w64-mingw32",
                        "--target=i686-w64-mingw32",
                    ]
                )
            else:
                self.platform = Arguments(
                    [
                        "--host=x86_64-w64-mingw32",
                        "--build=x86_64-w64-mingw32",
                        "--target=x86_64-w64-mingw32",
                    ]
                )
        elif CraftCore.compiler.platform.isAndroid:
            if CraftCore.compiler.architecture.isArm64:
                self.platform = Arguments(["--host=aarch64-linux-android"])
            else:
                self.platform = Arguments([f"--host={CraftCore.compiler.architecture.androidArchitecture}-linux-android"])
        elif CraftCore.compiler.hostPlatform.isApple:
            if not CraftCore.compiler.platform.isNative or not CraftCore.compiler.architecture.isNative:
                targetPlatform = "darwin" if CraftCore.compiler.platform.isMacOS else "ios"
                self.platform = Arguments(
                    [
                        f"--host={CraftCore.compiler.architecture.name.lower()}-apple-darwin{os.uname().release}",
                        f"--target={CraftCore.compiler.architecture.name.lower()}-apple-{targetPlatform}",
                    ]
                )

    @property
    def makeProgram(self):
        if CraftCore.compiler.platform.isWindows:
            return "make"
        else:
            return super().makeProgram

    # make sure shell cant be overwritten
    @property
    def shell(self):
        return self._shell

    def configureDefaultDefines(self):
        """defining the default cmake cmd line"""
        return ""

    def configure(self):
        """configure the target"""
        self.enterBuildDir()

        configure = Arguments([self.sourceDir() / (self.subinfo.options.configure.projectFile or "configure")])
        self.shell.environment["CFLAGS"] = self.subinfo.options.configure.cflags + " " + self.shell.environment["CFLAGS"]
        self.shell.environment["CXXFLAGS"] = self.subinfo.options.configure.cxxflags + " " + self.shell.environment["CXXFLAGS"]
        self.shell.environment["LDFLAGS"] = self.subinfo.options.configure.ldflags + " " + self.shell.environment["LDFLAGS"]
        self.shell.environment["MAKE"] = self.makeProgram

        env = {"CLICOLOR_FORCE": None}
        if self.supportsCCACHE:
            cxx = CraftCore.standardDirs.craftRoot() / "dev-utils/ccache/bin" / Path(os.environ["CXX"]).name
            if CraftCore.compiler.platform.isWindows and not cxx.suffix:
                cxx = Path(str(cxx) + CraftCore.compiler.platform.executableSuffix)
            if cxx.exists():
                env["CXX"] = OsUtils.toMSysPath(cxx)
                env["CC"] = OsUtils.toMSysPath(cxx.parent / Path(os.environ["CC"]).name)

        with utils.ScopedEnv(env):
            autogen = self.sourceDir() / "autogen.sh"
            if self.subinfo.options.configure.bootstrap and autogen.exists():
                mode = os.stat(autogen).st_mode
                if mode & stat.S_IEXEC == 0:
                    os.chmod(autogen, mode | stat.S_IEXEC)
                self.shell.execute(self.sourceDir(), autogen)
            elif self.subinfo.options.configure.autoreconf and ((self.sourceDir() / "configure.ac").exists() or (self.sourceDir() / "configure.in").exists()):
                includesArgs = Arguments()
                if self.subinfo.options.configure.useDefaultAutoreconfIncludes:
                    includes = []
                    dataDirs = [CraftCore.standardDirs.craftRoot() / "dev-utils/cmake/share"]
                    if CraftCore.compiler.platform.isWindows:
                        # on Windows data location lies outside of the autotools prefix (msys)
                        dataDirs.append(CraftCore.standardDirs.locations.data)
                    for i in dataDirs:
                        aclocalDir = i / "aclocal"
                        if aclocalDir.is_dir():
                            includes += [f"-I{self.shell.toNativePath(aclocalDir)}"]
                    includesArgs += includes
                if not self.shell.execute(
                    self.sourceDir(),
                    "autoreconf",
                    Arguments(self.subinfo.options.configure.autoreconfArgs) + includesArgs,
                ):
                    return False

            return self.shell.execute(self.buildDir(), configure, self.configureOptions(self))

    def make(self, dummyBuildType=None):
        """Using the *make program"""
        self.enterBuildDir()
        # adding Targets later
        if not self.subinfo.options.useShadowBuild:
            if not self.shell.execute(self.buildDir(), self.makeProgram, "clean"):
                return False
        return self.shell.execute(
            self.buildDir(),
            self.makeProgram,
            self.makeOptions(self.subinfo.options.make.args),
        )

    def install(self):
        """Using *make install"""
        self.cleanImage()
        self.enterBuildDir()

        args = self.makeOptions(self.subinfo.options.install.args)

        destDir = self.shell.toNativePath(self.installDir())
        args += [f"DESTDIR={destDir}"]
        with utils.ScopedEnv({"DESTDIR": destDir}):
            if not self.shell.execute(self.buildDir(), self.makeProgram, args):
                return False

        # la files aren't relocatable and until now we lived good without them
        laFiles = glob.glob(os.path.join(self.imageDir(), "**/*.la"), recursive=True)
        for laFile in laFiles:
            if not utils.deleteFile(laFile):
                return False

        if not self._fixInstallPrefix(self.shell.toNativePath(self.installPrefix())):
            return False
        if CraftCore.compiler.compiler.isMSVC:
            # libtool produces intl.dll.lib while we expect intl.lib
            lib = glob.glob(os.path.join(self.imageDir(), "lib/**/*.dll.lib"), recursive=True)
            for src in lib:
                src = Path(src)
                dest = src.with_suffix("").with_suffix(".lib")
                if not dest.exists():
                    if not utils.moveFile(src, dest):
                        return False
        return True

    def unittest(self):
        """running unittests"""
        return self.shell.execute(self.buildDir(), self.makeProgram, self.makeOptions("check"))

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)
        prefix = self.shell.toNativePath(self.installPrefix())
        options += [f"--prefix={prefix}"]
        if not self.subinfo.options.configure.noCacheFile:
            options += [f"--cache-file={self.shell.toNativePath(self.buildDir())}/config.cache"]
        if not self.subinfo.options.configure.noLibDir:
            options += [f"--libdir={prefix}/lib"]
        if OsUtils.isWin() and not self.subinfo.options.configure.noDataRootDir:
            options += [f"--datarootdir={self.shell.toNativePath(CraftCore.standardDirs.locations.data)}"]
        if self.subinfo.options.configure.staticArgs is not None:
            options += self.subinfo.options.configure.staticArgs
        else:
            options += [
                f"--{self.subinfo.options.dynamic.buildStatic.asEnableDisable}-static",
                f"--{self.subinfo.options.dynamic.buildStatic.inverted.asEnableDisable}-shared",
            ]
        options += self.platform
        return options
