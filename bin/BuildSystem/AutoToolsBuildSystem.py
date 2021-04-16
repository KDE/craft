# -*- coding: utf-8 -*-
# definitions for the autotools build system

from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from shells import BashShell
import utils
from Utils.Arguments import Arguments

import os
import glob
import re
import stat


class AutoToolsBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "autotools")
        self._shell = BashShell()
        self.platform = ""# hope for auto detection
        if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative() and CraftCore.compiler.isX86():
            self.platform = Arguments(["--host=i686-pc-linux-gnu"])
        elif CraftCore.compiler.isWindows:
            if CraftCore.compiler.isX86():
                self.platform = Arguments(["--host=i686-w64-mingw32", "--build=i686-w64-mingw32", "--target=i686-w64-mingw32"])
            else:
                self.platform = Arguments(["--host=x86_64-w64-mingw32", "--build=x86_64-w64-mingw32", "--target=x86_64-w64-mingw32"])
        elif CraftCore.compiler.isAndroid:
            if CraftCore.compiler.architecture == "arm":
                self.platform = Arguments(["--host=arm-linux-androideabi"])
            elif CraftCore.compiler.architecture == "arm64":
                self.platform = Arguments(["--host=aarch64-linux-android"])
            else:
                self.platform = Arguments([f"--host={CraftCore.compiler.architecture}-linux-android"])

    @property
    def makeProgram(self):
        if CraftCore.compiler.isWindows:
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

        with utils.ScopedEnv({"CLICOLOR_FORCE": None}):
            autogen = self.sourceDir() / "autogen.sh"
            if self.subinfo.options.configure.bootstrap and autogen.exists():
                mode = os.stat(autogen).st_mode
                if mode & stat.S_IEXEC == 0:
                    os.chmod(autogen, mode | stat.S_IEXEC)
                self.shell.execute(self.sourceDir(), autogen)
            elif self.subinfo.options.configure.autoreconf and (self.sourceDir() / "configure.ac").exists():
                includesArgs = Arguments()
                if self.subinfo.options.configure.useDefaultAutoreconfIncludes:
                    includes = []
                    dataDirs = [CraftCore.standardDirs.craftRoot() / "dev-utils/cmake/share"]
                    if CraftCore.compiler.isWindows:
                        # on Windows data location lies outside of the autotools prefix (msys)
                        dataDirs.append(CraftCore.standardDirs.locations.data)
                    for i in dataDirs:
                        aclocalDir = i / "aclocal"
                        if aclocalDir.is_dir():
                            includes += [f"-I{self.shell.toNativePath(aclocalDir)}"]
                    includesArgs += includes
                if not self.shell.execute(self.sourceDir(), "autoreconf", Arguments(self.subinfo.options.configure.autoreconfArgs) + includesArgs):
                    return False

            return self.shell.execute(self.buildDir(), configure, self.configureOptions(self))


    def make(self, dummyBuildType=None):
        """Using the *make program"""
        self.enterBuildDir()

        command = self.makeProgram
        args = self.makeOptions(self.subinfo.options.make.args)

        # adding Targets later
        if not self.subinfo.options.useShadowBuild:
            if not self.shell.execute(self.buildDir(), self.makeProgram, "clean"):
                return False
        return self.shell.execute(self.buildDir(), command, args)

    def install(self):
        """Using *make install"""
        self.cleanImage()
        self.enterBuildDir()

        command = self.makeProgram
        args = self.makeOptions(self.subinfo.options.install.args)

        destDir = self.shell.toNativePath(self.installDir())
        args += [f"DESTDIR={destDir}"]
        with utils.ScopedEnv({"DESTDIR" : destDir}):
            if not self.shell.execute(self.buildDir(), command, args):
                return False

        # la files aren't relocatable and until now we lived good without them
        laFiles = glob.glob(os.path.join(self.imageDir(), "**/*.la"), recursive=True)
        for laFile in laFiles:
            if not utils.deleteFile(laFile):
                return False

        return self._fixInstallPrefix(self.shell.toNativePath(self.installPrefix()))

    def unittest(self):
        """running unittests"""
        return self.shell.execute(self.buildDir(), self.makeProgram, "check")

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)
        prefix = self.shell.toNativePath(self.installPrefix())
        options += [f"--prefix={prefix}"]
        if OsUtils.isWin() and not self.subinfo.options.configure.noDataRootDir:
            options += [f"--datarootdir={self.shell.toNativePath(CraftCore.standardDirs.locations.data)}"]
        options += self.platform
        return options

    def ccacheOptions(self):
        return [f"CC=ccache {os.environ['CC']}", f"CXX=ccache {os.environ['CXX']}"]
