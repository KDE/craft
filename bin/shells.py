#!/usr/bin/env python

"""
    provides shells
"""
import os
import platform
import shutil
import sys
from pathlib import Path

import utils
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Utils.Arguments import Arguments


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
            if OsUtils.isWin():

                def convertPath(path: str):
                    return ":".join([str(self.toNativePath(p)) for p in path.split(os.path.pathsep)])

            mergeroot = self.toNativePath(CraftCore.standardDirs.craftRoot())
            ldflags = f" -L{mergeroot}/lib "
            cflags = f" -I{mergeroot}/include "

            if CraftCore.compiler.platform.isApple:
                # Only look for includes/libraries in the XCode SDK on MacOS to avoid errors with
                # libraries installed by homebrew (causes errors e.g. with iconv since headers will be
                # found in /usr/local/include first but libraries are searched for in /usr/lib before
                # /usr/local/lib. See https://langui.sh/2015/07/24/osx-clang-include-lib-search-paths/
                # Ensure that /usr/include comes before /usr/local/include in the header search path to avoid
                # pulling in headers from /usr/local/include (e.g. installed by homebrew) that will cause
                # linker errors later.
                platform = "macosx" if CraftCore.compiler.platform.isMacOS else "iphonesimulator"
                sdkPath = CraftCore.cache.getCommandOutput("xcrun", f"--sdk {platform} --show-sdk-path")[1].strip()
                if CraftCore.compiler.platform.isMacOS:
                    deploymentFlag = f"-mmacosx-version-min={os.environ['MACOSX_DEPLOYMENT_TARGET']}"
                else:
                    deploymentFlag = ""
                cflags = f" -isysroot {sdkPath} {deploymentFlag} {cflags} -isystem /usr/include"
                ldflags = f" -isysroot {sdkPath} {deploymentFlag} {ldflags}"

                if not CraftCore.compiler.architecture.isNative:
                    arch = CraftCore.compiler.architecture.name.lower()
                    self._environment["CC"] = f"{os.environ['CC']} -arch {arch}"
                    self._environment["CXX"] = f"{os.environ['CXX']} -arch {arch}"

                # TODO: well that sounded like a good idea, but is broken with recent xcode
                # when fixed we probably should also set that flag for the rest too?
                # See https://github.com/Homebrew/homebrew-core/issues/2674 for the -no_weak_imports flag
                # ldflags = f" -Wl,-no_weak_imports {ldflags}"

            if CraftCore.compiler.compiler.isMSVC:
                self._environment["INCLUDE"] = f"{mergeroot}/include:{convertPath(os.environ['INCLUDE'])}"
                self._environment["LIB"] = f"{mergeroot}/lib:{convertPath(os.environ['LIB'])}"

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
                if OsUtils.supportsSymlinks():
                    self._environment["MSYS"] = "winsymlinks:nativestrict"
                # we really want to use all the tools from msys, don't prepend our dirs
                path = "/usr/local/bin:/usr/bin:/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl"
                if CraftCore.compiler.compiler.isMinGW:
                    gcc = shutil.which("gcc")
                    if gcc:
                        path = f"{self.toNativePath(os.path.dirname(gcc))}:{path}"
                elif CraftCore.compiler.compiler.isMSVC:
                    path = f"{self.toNativePath(os.path.dirname(shutil.which('cl')))}:{path}"
                self._environment["PATH"] = f"{path}:{convertPath(os.environ['PATH'])}"
                self._environment["PKG_CONFIG_PATH"] = convertPath(os.environ["PKG_CONFIG_PATH"])

                if "make" in self._environment:
                    del self._environment["make"]
                # MSYSTEM is used by uname
                if CraftCore.compiler.compiler.isMinGW:
                    self._environment["MSYSTEM"] = f"MINGW{CraftCore.compiler.architecture.bits}_CRAFT"
                elif CraftCore.compiler.compiler.isMSVC:
                    self._environment["MSYSTEM"] = f"MSYS{CraftCore.compiler.architecture.bits}_CRAFT"

                if self.useMSVCCompatEnv and CraftCore.compiler.compiler.isMSVC:
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
                    self._environment["AR"] = f"{self.toNativePath(os.path.join(latestAutomake, 'ar-lib'))} lib"
                    self._environment["LD"] = "link -nologo"
                    self._environment["CC"] = f"{clWrapper} {cl} -nologo"
                    self._environment["CXX"] = self._environment["CC"]
                    self._environment["CPP"] = f"{cl} -nologo -E"
                    self._environment["CXXCPP"] = self._environment["CPP"]
                    self._environment["NM"] = "dumpbin -nologo -symbols"

                    windresArg = " --preprocessor-arg=".join(
                        [
                            "",
                            "-nologo",
                            "-EP",
                            "-DRC_INVOKED",
                            "-DWINAPI_FAMILY=WINAPI_FAMILY_DESKTOP_APP",
                        ]
                    )
                    self._environment[
                        "WINDRES"
                    ] = f"windres --target={'pe-i386' if CraftCore.compiler.architecture == CraftCore.compiler.Architecture.x86_32 else 'pe-x86-64'} --preprocessor=cl {windresArg}"
                    self._environment["RC"] = f"{self._environment['WINDRES']} -O COFF"

                    self._environment["STRIP"] = ":"
                    self._environment["RANLIB"] = ":"
                    self._environment["F77"] = "no"
                    self._environment["FC"] = "no"

                    cflags += (
                        " -GR -W3 -EHsc"  # dynamic and exceptions enabled
                        " -D_USE_MATH_DEFINES -DWIN32_LEAN_AND_MEAN -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS -D_WIN32_WINN=_WIN32_WINNT_WIN7"
                        " -wd4005"  # don't warn on redefine
                        " -wd4996"  # The POSIX name for this item is deprecated.
                    )
                    if CraftCore.compiler.getMsvcPlatformToolset() > 120:
                        cflags += " -FS"

            if CraftCore.compiler.platform.isAndroid:
                toolchainPath = os.path.join(
                    CraftCore.standardDirs.tmpDir(),
                    f"android-{CraftCore.compiler.architecture}-toolchain",
                )
                utils.system(
                    [
                        "python3",
                        os.path.join(
                            os.environ.get("ANDROID_NDK_ROOT"),
                            "build/tools/make_standalone_toolchain.py",
                        ),
                        "--install-dir",
                        toolchainPath,
                        "--arch",
                        CraftCore.compiler.architecture.androidArchitecture,
                        "--api",
                        CraftCore.compiler.androidApiLevel(),
                    ]
                )
                self._environment["PATH"] = os.path.join(toolchainPath, "bin") + ":" + os.environ["PATH"]
                self._environment["AR"] = "ar"
                self._environment["AS"] = "clang"
                self._environment["CC"] = "clang"
                self._environment["CXX"] = "clang++"
                self._environment["LD"] = "ld"
                self._environment["STRIP"] = "strip"
                self._environment["RANLIB"] = "ranlib"

            self._environment["CFLAGS"] = os.environ.get("CFLAGS", "").replace("$", "$$") + cflags
            self._environment["CXXFLAGS"] = os.environ.get("CXXFLAGS", "").replace("$", "$$") + cflags
            self._environment["LDFLAGS"] = os.environ.get("LDFLAGS", "").replace("$", "$$") + ldflags
        return self._environment

    @property
    def buildType(self):
        return CraftCore.settings.get("Compile", "BuildType", "RelWithDebInfo")

    @staticmethod
    def toNativePath(path) -> Path:
        if OsUtils.isWin():
            return OsUtils.toMSysPath(str(path))
        else:
            return Path(str(path))

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
        bashArgs = []
        if "bashArguments" in kwargs:
            bashArgs = kwargs.pop("bashArguments")
        if CraftCore.compiler.platform.isWindows:
            tmp = CraftCore.cache.findApplication(cmd)
            if tmp:
                cmd = tmp
            command = Arguments([self._findBash()] + bashArgs + ["-c", str(Arguments([self.toNativePath(cmd), args]))])
        else:
            command = Arguments(bashArgs + [cmd, args])
        env = dict(os.environ)
        env.update(self.environment)
        env.update(kwargs.get("env", {}))
        return utils.system(command, cwd=path, env=env, **kwargs)

    def login(self):
        if CraftCore.compiler.compiler.isMSVC:
            self.useMSVCCompatEnv = True
        return self.execute(os.curdir, self._findBash(), "-i", displayProgress=True)


class Powershell(object):
    def __init__(self):
        self.pwsh = CraftCore.cache.findApplication("pwsh")
        if not self.pwsh:
            if platform.architecture()[0] == "32bit":
                self.pwsh = CraftCore.cache.findApplication(
                    "powershell",
                    os.path.join(os.environ["WINDIR"], "sysnative", "WindowsPowerShell", "v1.0"),
                )
            if not self.pwsh:
                self.pwsh = CraftCore.cache.findApplication("powershell")
        if not self.pwsh:
            CraftCore.log.warning("Failed to detect powershell")

    def quote(self, s: str) -> str:
        return f"'{s}'"

    def execute(self, args: list[str], **kw) -> bool:
        return utils.system(
            [self.pwsh, "-NoProfile", "-ExecutionPolicy", "ByPass", "-Command"] + args,
            **kw,
        )


def main():
    shell = BashShell()
    shell.login()


def testColor():
    shell = BashShell()
    shell.execute(
        CraftCore.standardDirs.craftRoot(),
        os.path.join(CraftCore.standardDirs.craftBin(), "data", "ansi_color.sh"),
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "color":
            testColor()
    else:
        main()
