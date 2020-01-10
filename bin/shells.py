#!/usr/bin/env python

"""
    provides shells
"""
import platform
import subprocess
import sys

from CraftCore import CraftCore
from Blueprints.CraftVersion import CraftVersion
from CraftOS.osutils import OsUtils
import utils

import os
import shutil

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
            mergeroot = self.toNativePath(CraftCore.standardDirs.craftRoot())

            ldflags = f" -L{mergeroot}/lib "
            cflags = f" -I{mergeroot}/include "

            if CraftCore.compiler.isMacOS:
                # Only look for includes/libraries in the XCode SDK on MacOS to avoid errors with
                # libraries installed by homebrew (causes errors e.g. with iconv since headers will be
                # found in /usr/local/include first but libraries are searched for in /usr/lib before
                # /usr/local/lib. See https://langui.sh/2015/07/24/osx-clang-include-lib-search-paths/
                # Ensure that /usr/include comes before /usr/local/include in the header search path to avoid
                # pulling in headers from /usr/local/include (e.g. installed by homebrew) that will cause
                # linker errors later.
                sdkPath = CraftCore.cache.getCommandOutput("xcrun", "--show-sdk-path")[1].strip()
                deploymentFlag = f"-mmacosx-version-min={os.environ['MACOSX_DEPLOYMENT_TARGET']}"
                cflags = f" -isysroot {sdkPath} {deploymentFlag} {cflags} -isystem /usr/include"
                # See https://github.com/Homebrew/homebrew-core/issues/2674 for the -no_weak_imports flag
                ldflags = f" -isysroot {sdkPath} {deploymentFlag} -Wl,-no_weak_imports {ldflags}"

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

            if OsUtils.isWin():
                def convertPath(path : str):
                    return ":".join([self.toNativePath(p) for p in path.split(os.path.pathsep)])
                path = "/usr/local/bin:/usr/bin:/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl"
                if CraftCore.compiler.isMinGW():
                    gcc = shutil.which("gcc")
                    if gcc:
                        path = f"{self.toNativePath(os.path.dirname(gcc))}:{path}"
                elif CraftCore.compiler.isMSVC():
                        path = f"{self.toNativePath(os.path.dirname(shutil.which('cl')))}:{path}"
                self._environment["PATH"] = f"{path}:{convertPath(os.environ['PATH'])}"
                self._environment["PKG_CONFIG_PATH"] = convertPath(os.environ["PKG_CONFIG_PATH"])

                if "make" in self._environment:
                    del self._environment["make"]
                # MSYSTEM is used by uname
                if CraftCore.compiler.isMinGW():
                    self._environment["MSYSTEM"] = f"MINGW{CraftCore.compiler.bits}_CRAFT"
                elif CraftCore.compiler.isMSVC():
                    self._environment["MSYSTEM"] = f"MSYS{CraftCore.compiler.bits}_CRAFT"

                if self.useMSVCCompatEnv and CraftCore.compiler.isMSVC():

                    automake = []
                    for d in os.scandir(os.path.join(os.path.dirname(self._findBash()), "..", "share")):
                        if d.name.startswith("automake"):
                            automake += [(d.name.rsplit("-")[1], os.path.realpath(d.path))]
                    automake.sort(key=lambda x: CraftVersion(x[0]))
                    latestAutomake = automake[-1][1]
                    if False:
                        cl = "clang-cl"
                    else:
                        cl = "cl"
                    clWrapper = self.toNativePath(os.path.join(latestAutomake, "compile"))
                    self._environment["LD"] = "link -nologo"
                    self._environment["CC"] = f"{clWrapper} {cl} -nologo"
                    self._environment["CXX"] = self._environment["CC"]
                    self._environment["CPP"] = f"{cl} -nologo -EP"
                    self._environment["CXXCPP"] = self._environment["CPP"]
                    self._environment["NM"] = "dumpbin -symbols"
                    self._environment["RC"] = f"windres -O COFF --target={'pe-i386' if CraftCore.compiler.isX86() else 'pe-x86-64'} --preprocessor='cl -nologo -EP -DRC_INVOKED -DWINAPI_FAMILY=0'"

                    self._environment["STRIP"] = ":"
                    self._environment["RANLIB"] = ":"
                    self._environment["F77"] = "no"
                    self._environment["FC"] = "no"

                    cflags += (" -GR -W3 -EHsc"  # dynamic and exceptions enabled
                               " -D_USE_MATH_DEFINES -DWIN32_LEAN_AND_MEAN -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS"
                               " -wd4005"  # don't warn on redefine
                               " -wd4996"  # The POSIX name for this item is deprecated.
                               )
                    if CraftCore.compiler.getMsvcPlatformToolset() > 120:
                        cflags += " -FS"



            self._environment["CFLAGS"] = os.environ.get("CFLAGS", "").replace("$", "$$") + cflags
            self._environment["CXXFLAGS"] = os.environ.get("CXXFLAGS", "").replace("$", "$$") + cflags
            self._environment["LDFLAGS"] = os.environ.get("LDFLAGS", "").replace("$", "$$") + ldflags
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
            msysdir = CraftCore.standardDirs.msysDir()
            bash = CraftCore.cache.findApplication("bash", os.path.join(msysdir, "usr", "bin"))
        else:
            bash = CraftCore.cache.findApplication("bash")
        if not bash:
            CraftCore.log.critical("Failed to detect bash")
        return bash

    def execute(self, path, cmd, args="", **kwargs):
        # try to locate the command
        tmp = CraftCore.cache.findApplication(cmd)
        if tmp:
            cmd = tmp
        if CraftCore.compiler.isWindows:
            command = f"{self._findBash()} -c \"{self.toNativePath(cmd)} {args}\""
        else:
            command = f"{self.toNativePath(cmd)} {args}"

        env = dict(os.environ)
        env.update(self.environment)
        env.update(kwargs.get("env", {}))
        return utils.system(command, cwd=path, env=env,**kwargs)

    def login(self):
        if CraftCore.compiler.isMSVC():
            self.useMSVCCompatEnv = True
        return self.execute(os.curdir, self._findBash(),  "-i", displayProgress=True)

class Powershell(object):
    def __init__(self):
        self.pwsh = CraftCore.cache.findApplication("pwsh")
        if not self.pwsh:
            if platform.architecture()[0] == "32bit":
                self.pwsh = CraftCore.cache.findApplication("powershell", os.path.join(os.environ["WINDIR"], "sysnative", "WindowsPowerShell", "v1.0" ))
            if not self.pwsh:
                self.pwsh = CraftCore.cache.findApplication("powershell")
        if not self.pwsh:
            CraftCore.log.warning("Failed to detect powershell")

    def quote(self, s : str) -> str:
        return f"'{s}'"

    def execute(self, args :[str]) -> bool:
        return utils.system([self.pwsh, "-NoProfile", "-ExecutionPolicy", "ByPass", "-Command"] + args)

def main():
    shell = BashShell()
    shell.login()

def testColor():
    shell = BashShell()
    shell.execute(CraftCore.standardDirs.craftRoot(), os.path.join(CraftCore.standardDirs.craftBin(), "data", "ansi_color.sh"))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "color":
            testColor()
    else:
        main()
