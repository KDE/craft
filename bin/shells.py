#!/usr/bin/env python

"""
    provides shells
"""

from CraftStandardDirs import CraftStandardDirs
from CraftOS.OsDetection import OsDetection
from options import *


class BashShell(object):
    def __init__(self):
        self._environment = None
        self._useMSVCCompatEnv = False


    @property
    def useMSVCCompatEnv(self):
        return self._useMSVCCompatEnv

    @useMSVCCompatEnv.setter
    def useMSVCCompatEnv(self, b):
        self._useMSVCCompatEnv = b
        self._environment = {}

    @property
    def environment(self):
        if self._environment is None:
            self._environment = {}

            mergeroot = self.toNativePath(CraftStandardDirs.craftRoot())
            cflags = ""
            ldflags = ""
            if not CraftCore.compiler.isMSVC():
                ldflags = f"-L{mergeroot}/lib "
                cflags = f"-I{mergeroot}/include "

                if self.buildType == "RelWithDebInfo":
                    cflags += " -O2 -g "
                elif self.buildType == "Debug":
                    cflags += " -O0 -g3 "

            if OsDetection.isWin():
                self._environment["MSYS2_PATH_TYPE"] = "inherit"  # inherit the windows path
                if "make" in self._environment:
                    del self._environment["make"]
                if CraftCore.compiler.isMinGW():
                    self._environment["MSYSTEM"] = f"MINGW{CraftCore.compiler.bits}_CRAFT"
                elif CraftCore.compiler.isMSVC():
                    self._environment["MSYSTEM"] = f"CYGWIN{CraftCore.compiler.bits}_CRAFT"

                if self.useMSVCCompatEnv and CraftCore.compiler.isMSVC():
                    self._environment["LIB"] = f"{os.environ['LIB']};{CraftStandardDirs.craftRoot()}\\lib"
                    self._environment["INCLUDE"] = f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot()}\\include"

                    if False:
                        cl = "clang-cl"
                    else:
                        cl = "cl"
                    self._environment["LD"] = "link -NOLOGO"
                    self._environment["CC"] = "%s -nologo" % cl
                    self._environment["CXX"] = self._environment["CC"]
                    self._environment["CPP"] = "%s -nologo -EP" % cl
                    self._environment["CXXCPP"] = self._environment["CPP"]
                    self._environment["NM"] = "dumpbin -symbols"
                    self._environment["AR"] = "lib"
                    self._environment["WINDRES"] = "rc"
                    # self.environment[ "RC","rc-windres"
                    self._environment["STRIP"] = ":"
                    self._environment["RANLIB"] = ":"
                    self._environment["F77"] = "no"
                    self._environment["FC"] = "no"

                    ldflags = ""
                    cflags = " -O2 -MD -GR -W3 -EHsc -D_USE_MATH_DEFINES -DWIN32_LEAN_AND_MEAN -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS"  # dynamic and exceptions enabled
                    if CraftCore.compiler.getMsvcPlatformToolset() > 120:
                        cflags += " -FS"

            self._environment["PKG_CONFIG_PATH"] = self.toNativePath(
                os.path.join(CraftStandardDirs.craftRoot(), "lib", "pkgconfig"))


            self._environment["CFLAGS"] = cflags
            self._environment["CXXFLAGS"] = cflags
            self._environment["LDFLAGS"] = ldflags
        return self._environment

    @property
    def buildType(self):
        return CraftCore.settings.get("Compile", "BuildType", "RelWithDebInfo")

    @staticmethod
    def toNativePath(path):
        if OsUtils.isWin():
            return OsUtils.toMSysPath(path)
        else:
            return path

    def _findBash(self):
        msysdir = CraftStandardDirs.msysDir()
        bash = CraftCore.cache.findApplication("bash", os.path.join(msysdir, "bin"))
        if not bash:
            bash = CraftCore.cache.findApplication("bash", os.path.join(msysdir, "usr", "bin"))
        if not bash:
            CraftCore.log.critical("Failed to detect bash")
        return bash

    def execute(self, path, cmd, args="", out=sys.stdout, err=sys.stderr, displayProgress=False):

        export = ""
        env = os.environ.copy()
        for k, v in self.environment.items():
            export += f"{k}='{v}' "
            env[k] = v
        if CraftCore.debug.verbose() >= 1:
            # log msys env
            export += "&& export && which gcc "
        command = f"{self._findBash()} --login -c \"{export} && cd {self.toNativePath(path)} && {self.toNativePath(cmd)} {args}\""
        CraftCore.debug.step("bash execute: %s" % command)
        CraftCore.log.debug("bash environment: %s" % self.environment)
        return utils.system(command, stdout=out, stderr=err, env=env, displayProgress=displayProgress)

    def login(self):
        self.environment["CHERE_INVOKING"] = "1"
        command = "bash --login -i"
        return self.execute(".", command, displayProgress=True)

def main():
    shell = BashShell()
    shell.login()

if __name__ == '__main__':
    main()
