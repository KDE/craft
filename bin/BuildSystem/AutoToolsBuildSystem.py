# -*- coding: utf-8 -*-
# definitions for the autotools build system
from BuildSystem.BuildSystemBase import *
from shells import *
import glob
import re


class AutoToolsBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "autotools")
        self._shell = BashShell()
        if not OsUtils.isWin():
            self.platform = ""# hope for auto detection
        else:
            if CraftCore.compiler.isX86():
                self.platform = "--host=i686-w64-mingw32 --build=i686-w64-mingw32 --target=i686-w64-mingw32 "
            else:
                self.platform = "--host=x86_64-w64-mingw32 --build=x86_64-w64-mingw32 --target=x86_64-w64-mingw32 "

    def _execute(self, path, cmd, args=""):
        if not self.subinfo.options.useShadowBuild:
            envDir = self.sourceDir()
        else:
            envDir = self.buildDir()
        return self.shell.execute(path, cmd, args, envDir=envDir)

    @property
    def makeProgram(self):
        return "make"

    # make sure shell cant be overwritten
    @property
    def shell(self):
        return self._shell

    def configureDefaultDefines(self):

        """defining the default cmake cmd line"""
        return ""

    def configure(self):
        """configure the target"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        configure = os.path.join(self.sourceDir(), self.subinfo.options.configure.projectFile or "configure")
        self.shell.environment["CFLAGS"] = self.subinfo.options.configure.cflags + self.shell.environment["CFLAGS"]
        self.shell.environment["CXXFLAGS"] = self.subinfo.options.configure.cxxflags + self.shell.environment["CXXFLAGS"]
        self.shell.environment["LDFLAGS"] = self.subinfo.options.configure.ldflags + self.shell.environment["LDFLAGS"]
        if self.subinfo.options.configure.bootstrap:
            autogen = os.path.join(self.sourceDir(), "autogen.sh")
            if os.path.exists(autogen):
                self._execute(self.sourceDir(), autogen)
            else:
                self._execute(self.sourceDir(), "autoreconf", "-vfi")

        if not self.subinfo.options.useShadowBuild:
            ret = self._execute(self.sourceDir(), configure, self.configureOptions(self))
        else:
            ret = self._execute(self.buildDir(), configure, self.configureOptions(self))
        return ret

    def make(self, dummyBuildType=None):
        """Using the *make program"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        command = self.makeProgram
        args = self.makeOptions()

        # adding Targets later
        if not self.subinfo.options.useShadowBuild:
            if not self._execute(self.sourceDir(), self.makeProgram, "clean"):
                print("while Make'ing. cmd: %s clean" % self.makeProgram)
                return False
            if not self._execute(self.sourceDir(), command, args):
                print("while Make'ing. cmd: %s" % command)
                return False
        else:
            if not self._execute(self.buildDir(), command, args):
                print("while Make'ing. cmd: %s" % command)
                return False
        return True

    def install(self):
        """Using *make install"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        command = self.makeProgram
        args = "install"

        args += f" DESTDIR={self.shell.toNativePath(self.installDir())}"
        if self.subinfo.optsions.install.args:
            args += f" {self.subinfo.optsions.install.args}"
        if self.subinfo.options.make.ignoreErrors:
            args += " -i"

        if self.subinfo.options.make.makeOptions:
            args += " %s" % self.subinfo.options.make.makeOptions
        if not self.subinfo.options.useShadowBuild:
            if not self._execute(self.sourceDir(), command, args):
                print("while installing. cmd: %s %s" % (command, args))
                return False
        else:
            if not self._execute(self.buildDir(), command, args):
                print("while installing. cmd: %s %s" % (command, args))
                return False
        if os.path.exists(os.path.join(self.imageDir(), "lib")):
            if not self._execute(os.path.join(self.imageDir(), "lib"), "rm", " -Rf *.la"):
                return False

        return self._fixInstallPrefix(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))

    def runTest(self):
        """running unittests"""
        return True

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)
        if self.subinfo.options.configure.noDefaultOptions == False:
            options += f" --prefix={self.shell.toNativePath(CraftCore.standardDirs.craftRoot())} "
        options += self.platform

        return options;

    def ccacheOptions(self):
        return " CC='ccache gcc' CXX='ccache g++' "


    def copyToMsvcImportLib(self):
        if not OsDetection.isWin():
            return True
        reDlla = re.compile(r"\.dll\.a$")
        reLib = re.compile(r"^lib")
        for f in glob.glob(f"{self.installDir()}/lib/*.dll.a"):
            path, name = os.path.split(f)
            name = re.sub(reDlla, ".lib", name)
            name = re.sub(reLib, "", name)
            if not utils.copyFile(f, os.path.join(path, name), linkOnly=False):
                return False
        return True
