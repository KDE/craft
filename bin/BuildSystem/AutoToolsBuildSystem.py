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

        autogen = os.path.join(self.sourceDir(), "autogen.sh")
        if self.subinfo.options.configure.bootstrap and os.path.exists(autogen):
            self.shell.execute(self.sourceDir(), autogen)
        elif self.subinfo.options.configure.autoreconf:
            self.shell.execute(self.sourceDir(), "autoreconf", self.subinfo.options.configure.autoreconfArgs + f" -B{self.shell.toNativePath(CraftCore.standardDirs.locations.data)}/aclocal")

        if not self.subinfo.options.useShadowBuild:
            ret = self.shell.execute(self.sourceDir(), configure, self.configureOptions(self))
        else:
            ret = self.shell.execute(self.buildDir(), configure, self.configureOptions(self))
        return ret

    def make(self, dummyBuildType=None):
        """Using the *make program"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        command = self.makeProgram
        args = self.makeOptions(self.subinfo.options.make.args)

        # adding Targets later
        if not self.subinfo.options.useShadowBuild:
            if not self.shell.execute(self.sourceDir(), self.makeProgram, "clean"):
                print("while Make'ing. cmd: %s clean" % self.makeProgram)
                return False
            if not self.shell.execute(self.sourceDir(), command, args):
                print("while Make'ing. cmd: %s" % command)
                return False
        else:
            if not self.shell.execute(self.buildDir(), command, args):
                print("while Make'ing. cmd: %s" % command)
                return False
        return True

    def install(self):
        """Using *make install"""
        self.cleanImage()
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        command = self.makeProgram
        args = self.makeOptions(self.subinfo.options.install.args)

        args += f" DESTDIR={self.shell.toNativePath(self.installDir())}"
        if not self.subinfo.options.useShadowBuild:
            if not self.shell.execute(self.sourceDir(), command, args):
                print("while installing. cmd: %s %s" % (command, args))
                return False
        else:
            if not self.shell.execute(self.buildDir(), command, args):
                print("while installing. cmd: %s %s" % (command, args))
                return False


        # la files aren't relocatable and until now we lived good without them
        laFiles = glob.glob(os.path.join(self.imageDir(), "**/*.la"), recursive=True)
        for laFile in laFiles:
            if not utils.deleteFile(laFile):
                return False

        return self._fixInstallPrefix(self.shell.toNativePath(self.installPrefix()))

    def runTest(self):
        """running unittests"""
        return True

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)
        prefix = self.shell.toNativePath(self.installPrefix())
        options += f" --prefix='{prefix}' "
        if OsDetection.isWin() and not self.subinfo.options.configure.noDataRootDir:
            options += f" --datarootdir='{self.shell.toNativePath(CraftCore.standardDirs.locations.data)}' "
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
