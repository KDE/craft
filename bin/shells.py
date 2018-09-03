#!/usr/bin/env python

"""
    provides shells
"""

from CraftStandardDirs import CraftStandardDirs
from CraftOS.OsDetection import OsDetection
from options import *


class BashShell(object):
    def __init__(self):
        self._environment = {}
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
        if not self._environment:

            mergeroot = self.toNativePath(CraftStandardDirs.craftRoot())

            ldflags = f" -L{mergeroot}/lib "
            cflags = f" -I{mergeroot}/include "
            if CraftCore.compiler.isMSVC():
                # based on Windows-MSVC.cmake
                if self.buildType == "Release":
                    cflags += " -MD -O2 -Ob2 -DNDEBUG "
                elif self.buildType == "RelWithDebInfo":
                    cflags += " -MD -Zi -O2 -Ob1 -DNDEBUG "
                    ldflags += " -debug "
                elif self.buildType == "Debug":
                    cflags += " -MDd -Zi -Ob0 -Od "
                    ldflags += " -debug -pdbtype:sept "
            else:
                if self.buildType == "Release":
                    cflags += " -O3 -DNDEBUG "
                if self.buildType == "RelWithDebInfo":
                    cflags += " -O2 -g -DNDEBUG "
                elif self.buildType == "Debug":
                    cflags += " -O0 -g3 "

            if OsDetection.isWin():
                path = "/usr/local/bin:/usr/bin:/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl"
                if CraftCore.compiler.isMinGW():
                    gcc = shutil.which("gcc")
                    if gcc:
                        path = f"{self.toNativePath(os.path.dirname(gcc))}:{path}"
                for p in os.environ["PATH"].split(";"):
                    path += f":{self.toNativePath(p)}"
                self._environment["PATH"] = path
                if "make" in self._environment:
                    del self._environment["make"]
                # MSYSTEM is used by uname
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
                    self._environment["CC"] = f"{cl} -nologo"
                    self._environment["CXX"] = self._environment["CC"]
                    self._environment["CPP"] = f"{cl} -nologo -EP"
                    self._environment["CXXCPP"] = self._environment["CPP"]
                    self._environment["NM"] = "dumpbin -symbols"
                    self._environment["AR"] = "lib"
                    self._environment["WINDRES"] = "rc"
                    # self.environment[ "RC","rc-windres"
                    self._environment["STRIP"] = ":"
                    self._environment["RANLIB"] = ":"
                    self._environment["F77"] = "no"
                    self._environment["FC"] = "no"

                    ldflags += ""
                    cflags += " -GR -W3 -EHsc -D_USE_MATH_DEFINES -DWIN32_LEAN_AND_MEAN -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS"  # dynamic and exceptions enabled
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
        if OsUtils.isWin():
            msysdir = CraftStandardDirs.msysDir()
            bash = CraftCore.cache.findApplication("bash", os.path.join(msysdir, "bin"))
        else:
            bash = CraftCore.cache.findApplication("bash")
        if not bash:
            bash = CraftCore.cache.findApplication("bash", os.path.join(msysdir, "usr", "bin"))
        if not bash:
            CraftCore.log.critical("Failed to detect bash")
        return bash

    def execute(self, path, cmd, args="", out=sys.stdout, err=sys.stderr, displayProgress=False):
        # try to locate the command
        tmp = CraftCore.cache.findApplication(cmd)
        if tmp:
            cmd = tmp
        command = f"{self._findBash()} -c \"cd {self.toNativePath(path)} && {self.toNativePath(cmd)} {args}\""
        CraftCore.debug.step("bash execute: %s" % command)
        CraftCore.log.debug("bash environment: %s" % self.environment)

        env = dict(os.environ)
        env.update(self.environment)

        out = utils.system(command, stdout=out, stderr=err, displayProgress=displayProgress, env=env)
        return out

    def login(self):
        if CraftCore.compiler.isMSVC():
            self.useMSVCCompatEnv = True
        return self.execute(os.curdir, "bash",  "-i", displayProgress=True)

def main():
    shell = BashShell()
    shell.login()

if __name__ == '__main__':
    main()
