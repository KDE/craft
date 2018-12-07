# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import argparse
import collections
import subprocess
import copy
import platform

from CraftConfig import *
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
# The minimum python version for craft please edit here
# if you add code that changes this requirement
from CraftStandardDirs import CraftStandardDirs, TemporaryUseShortpath

MIN_PY_VERSION = (3, 6, 0)


def log(msg, critical=False):
    if critical or not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
        CraftCore.debug.print(msg, sys.stderr)
    else:
        CraftCore.log.debug(msg)
    if critical:
      exit(1)


if sys.version_info[0:3] < MIN_PY_VERSION:
    log("Error: Python too old!\n"
        "Craft needs at least Python Version %s.%s.%s\n"
        "Please install it and adapt your CraftSettings.ini" % MIN_PY_VERSION, critical=True)

if not platform.machine().endswith("64"):
    log(f"Craft requires a 64bit operating system. Your are using: {platform.machine()}", critical=True)


class SetupHelper(object):
    CraftVersion = "master"
    def __init__(self, args=None):
        self.args = args
        if CraftCore.settings.getboolean("General", "AllowAnsiColor", False):
            OsUtils.enableAnsiColors()


    @staticmethod
    def _getOutput(command, shell=False):
        CraftCore.log.debug(f"SetupHelper._getOutput: {command}")
        p = subprocess.run(command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=shell,
                           universal_newlines=True,
                           errors="backslashreplace")
        out = p.stdout.strip()
        CraftCore.log.debug(f"SetupHelper._getOutput: return {p.returncode} {out}")
        return p.returncode, out

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--subst", action="store_true")
        parser.add_argument("--get", action="store_true")
        parser.add_argument("--print-banner", action="store_true")
        parser.add_argument("--getenv", action="store_true")
        parser.add_argument("--setup", action="store_true")
        parser.add_argument("rest", nargs=argparse.REMAINDER)
        args = parser.parse_args()

        if args.subst:
            self.subst()
        elif args.get:
            default = ""
            if len(args.rest) == 3:
                default = args.rest[2]
            CraftCore.log.info(CraftCore.settings.get(args.rest[0], args.rest[1], default))
        elif args.print_banner:
            self.printBanner()
        elif args.getenv:
            self.printEnv()
        elif args.setup:
            self.subst()
            self.printEnv()
            self.printBanner()

    def checkForEvilApplication(self):
        blackList = []
        if OsUtils.isWin():
            blackList += ["sh", "gcc", "g++", "cpp"]
        for app in blackList:
            location = shutil.which(app)
            if location:
                location = os.path.dirname(location)
                if not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
                    log(
                        f"Found \"{app}\" in your PATH: \"{location}\"\n"
                        f"This application is known to cause problems with your configuration of Craft.\n"
                        f"Please remove it from PATH or manually set a value for PATH in your CraftSettings.ini:\n"
                        f"\n"
                        f"[Environment]\n"
                        f"PATH="
                        f"\n")
                else:
                    path = collections.OrderedDict.fromkeys(os.environ["Path"].split(os.path.pathsep))
                    del path[location]
                    self.addEnvVar("Path", os.path.pathsep.join(path))

    def subst(self):
        if not OsUtils.isWin():
            return
        def _subst(path, drive):
            if not os.path.exists(path):
                os.makedirs(path)
            SetupHelper._getOutput(["subst",
                             CraftCore.settings.get("ShortPath", drive),
                             path])

        if CraftCore.settings.getboolean("ShortPath", "Enabled", False):
            with TemporaryUseShortpath(False):
                if ("ShortPath", "RootDrive") in CraftCore.settings:
                    _subst(CraftStandardDirs.craftRoot(), "RootDrive")
                if ("ShortPath", "DownloadDrive") in CraftCore.settings:
                    _subst(CraftStandardDirs.downloadDir(), "DownloadDrive")
                if ("ShortPath", "GitDrive") in CraftCore.settings:
                    _subst(CraftStandardDirs.gitDir(), "GitDrive")

        if CraftCore.settings.getboolean("ShortPath", "EnableJunctions", False):
            with TemporaryUseShortpath(False):
                if ("ShortPath", "JunctionDrive") in CraftCore.settings:
                    _subst(CraftCore.standardDirs._junctionDir.longPath, "JunctionDrive")

    def printBanner(self):
        def printRow(name, value):
            log(f"{name:20}: {value}")

        if CraftStandardDirs.isShortPathEnabled():
            with TemporaryUseShortpath(False):
                printRow("Craft Root", CraftStandardDirs.craftRoot())
            printRow("Craft", CraftStandardDirs.craftRoot())
            printRow("Svn directory", CraftStandardDirs.svnDir())
            printRow("Git directory", CraftStandardDirs.gitDir())
        else:
            printRow("Craft", CraftStandardDirs.craftRoot())
        printRow("Version", SetupHelper.CraftVersion)
        printRow("ABI", CraftCore.compiler)
        printRow("Download directory", CraftStandardDirs.downloadDir())

    def addEnvVar(self, key, val):
        os.environ[key] = val

    def prependEnvVar(self, key : str, var : str, sep : str=os.path.pathsep) -> None:
        if not type(var) == list:
            var = [var]
        if key in os.environ:
            env = var + os.environ[key].split(sep)
            var = list(collections.OrderedDict.fromkeys(env))
        val = sep.join(var)
        CraftCore.log.debug(f"Setting {key}={val}")
        os.environ[key] = val

    @staticmethod
    def stringToEnv(string : str):
        for line in string.strip().split("\n"):
            kv = line.strip().split("=", 1)
            if len(kv) != 2:
                log(f"Failed to parse environment variable: {line}\n{string}")
                continue
            # TODO: why?
            if kv[0] == "Path":
                kv[0] = "PATH"
            os.environ[kv[0]] = kv[1]
        return os.environ

    @staticmethod
    def _callVCVER(version : int, args : []=None, native : bool=True) -> str:
        if not args:
            args = []
        vswhere = os.path.join(CraftCore.standardDirs.craftBin(), "3rdparty", "vswhere", "vswhere.exe")
        command = [vswhere, "-property", "installationPath", "-nologo", "-latest"]
        if version:
            command += ["-version", f"[{version},{version+1})"]
            if version < 15:
                command.append("-legacy")
            else:
                if not args:
                    args = ["-products", "*"]
                    if native:
                        # this fails with express versions
                        args += ["-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64"]
        return SetupHelper._getOutput(command + args)[1]

    @staticmethod
    def getMSVCEnv(version=None, architecture="x86", native=True) -> str:
        if native:
            architectures = {"x86": "amd64_x86", "x64": "amd64"}
        else:
            architectures = {"x86": "x86", "x64": "x86_amd64"}

        args = architectures[architecture]
        path = ""
        if version == 14:
            # are we using msvc2017 with "VC++ 2015.3 v14.00 (v140) toolset for desktop"
            path = SetupHelper._callVCVER(15, args=["-products", "*", "-requires", "Microsoft.VisualStudio.Component.VC.140"], native=native)
            if path:
                args += " -vcvars_ver=14.0"
        if not path:
            path = SetupHelper._callVCVER(version, native=native)

        path = os.path.join(path, "VC")
        if not os.path.exists(os.path.join(path, "vcvarsall.bat")):
            path = os.path.join(path, "Auxiliary", "Build")
        path = os.path.join(path, "vcvarsall.bat")
        if not os.path.isfile(path):
            log(f"Failed to setup msvc compiler.\n"
                f"{path} does not exist.", critical=True)
        status, result = SetupHelper._getOutput(f"\"{path}\" {args} > NUL && set", shell=True)
        if status != 0:
            log(f"Failed to setup msvc compiler.\n"
                f"Command: {result} ", critical=True)
        return SetupHelper.stringToEnv(result)

    def getEnv(self):
        if CraftCore.compiler.isMSVC():
            return SetupHelper.getMSVCEnv(CraftCore.compiler.getInternalVersion(),
                                                                  CraftCore.compiler.architecture,
                                                                  CraftCore.compiler.isNative())
        elif CraftCore.compiler.isIntel():
            architectures = {"x86": "ia32", "x64": "intel64"}
            programFiles = os.getenv("ProgramFiles(x86)") or os.getenv("ProgramFiles")
            status, result = SetupHelper._getOutput(
                "\"%s\\Intel\\Composer XE\\bin\\compilervars.bat\" %s > NUL && set" % (
                    programFiles, architectures[CraftCore.compiler.architecture]), shell=True)
            if status != 0:
                log("Failed to setup intel compiler", critical=True)
            return SetupHelper.stringToEnv(result)
        return os.environ

    def setXDG(self):
        self.prependEnvVar("XDG_DATA_DIRS", [os.path.join(CraftStandardDirs.craftRoot(), "share")])
        if OsUtils.isUnix():
            self.prependEnvVar("XDG_CONFIG_DIRS", [os.path.join(CraftStandardDirs.craftRoot(), "etc", "xdg")])
            self.addEnvVar("XDG_DATA_HOME",
                           os.path.join(CraftStandardDirs.craftRoot(), "home", os.getenv("USER"), ".local5", "share"))
            self.addEnvVar("XDG_CONFIG_HOME",
                           os.path.join(CraftStandardDirs.craftRoot(), "home", os.getenv("USER"), ".config"))
            self.addEnvVar("XDG_CACHE_HOME",
                           os.path.join(CraftStandardDirs.craftRoot(), "home", os.getenv("USER"), ".cache"))

    def _setupUnix(self):
        if CraftCore.compiler.isLinux:
            self.prependEnvVar("LDFLAGS", "-Wl,-rpath,'$ORIGIN/../lib'", sep=" ")
            self.prependEnvVar("LD_LIBRARY_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "lib"),
                                                   os.path.join(CraftStandardDirs.craftRoot(), "lib", "x86_64-linux-gnu")])
        self.prependEnvVar("BISON_PKGDATADIR", os.path.join(CraftStandardDirs.craftRoot(), "share", "bison"))
        self.prependEnvVar("M4", os.path.join(CraftStandardDirs.craftRoot(), "dev-utils", "bin", "m4"))

    def _setupWin(self):
        if not "HOME" in os.environ:
            self.addEnvVar("HOME", os.getenv("USERPROFILE"))

        if CraftCore.compiler.isMinGW():
            if not CraftCore.settings.getboolean("QtSDK", "Enabled", "false"):
                if CraftCore.compiler.isX86():
                    self.prependEnvVar("PATH", os.path.join(CraftStandardDirs.craftRoot(), "mingw", "bin"))
                else:
                    self.prependEnvVar("PATH", os.path.join(CraftStandardDirs.craftRoot(), "mingw64", "bin"))
            else:
                compilerName = CraftCore.settings.get("QtSDK", "Compiler")
                compilerMap = {"mingw53_32": "mingw530_32"}
                self.prependEnvVar("PATH", os.path.join(CraftCore.settings.get("QtSDK", "Path"), "Tools",
                                                      compilerMap.get(compilerName, compilerName), "bin"))
        if CraftCore.settings.getboolean("QtSDK", "Enabled", "false"):
            self.prependEnvVar("PATH",
                             os.path.join(CraftCore.settings.get("QtSDK", "Path"), CraftCore.settings.get("QtSDK", "Version"),
                                          CraftCore.settings.get("QtSDK", "Compiler"), "bin"))

        if CraftCore.compiler.isMinGW():
            if not CraftCore.settings.getboolean("QtSDK", "Enabled", "false"):
                if CraftCore.compiler.isX86():
                    self.prependEnvVar("PATH", os.path.join(CraftStandardDirs.craftRoot(), "mingw", "bin"))
                else:
                    self.prependEnvVar("PATH", os.path.join(CraftStandardDirs.craftRoot(), "mingw64", "bin"))
            else:
                compilerName = CraftCore.settings.get("QtSDK", "Compiler")
                compilerMap = {"mingw53_32": "mingw530_32"}
                self.prependEnvVar("PATH", os.path.join(CraftCore.settings.get("QtSDK", "Path"), "Tools",
                                                      compilerMap.get(compilerName, compilerName), "bin"))

    def setupEnvironment(self):
        for var, value in CraftCore.settings.getSection("Environment"):  # set and override existing values
            # the ini is case insensitive so sections are lowercase....
            self.addEnvVar(var.upper(), value)
        self.prependEnvVar("PATH", os.path.dirname(sys.executable))
        os.environ = self.getEnv()
        self.checkForEvilApplication()

        self.addEnvVar("KDEROOT", CraftStandardDirs.craftRoot())

        if CraftCore.settings.getboolean("Compile", "UseCCache", False):
            self.addEnvVar("CCACHE_DIR",
                           CraftCore.settings.get("Paths", "CCACHE_DIR", os.path.join(CraftStandardDirs.craftRoot(),
                                                                                 "build", "CCACHE")))

        if CraftCore.settings.getboolean("QtSDK", "Enabled", "false"):
            sdkPath = os.path.join(CraftCore.settings.get("QtSDK", "Path"),
                                   CraftCore.settings.get("QtSDK", "Version"),
                                   CraftCore.settings.get("QtSDK", "Compiler"), "bin")
            if not os.path.exists(sdkPath):
                log(f"Please ensure that you have installed the Qt SDK in {sdkPath}", critical=True)
            self.prependEnvVar("PATH", sdkPath)

        if OsUtils.isWin():
            self._setupWin()
        else:
            self._setupUnix()

        self.prependEnvVar("PKG_CONFIG_PATH", os.path.join(CraftStandardDirs.craftRoot(), "lib", "pkgconfig"))

        self.prependEnvVar("QT_PLUGIN_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "plugins"),
                                            os.path.join(CraftStandardDirs.craftRoot(), "lib", "plugins"),
                                            os.path.join(CraftStandardDirs.craftRoot(), "lib64", "plugins"),
                                            os.path.join(CraftStandardDirs.craftRoot(), "lib", "x86_64-linux-gnu",
                                                         "plugins"),
                                            os.path.join(CraftStandardDirs.craftRoot(), "lib", "plugin")
                                            ])

        self.prependEnvVar("QML2_IMPORT_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "qml"),
                                              os.path.join(CraftStandardDirs.craftRoot(), "lib", "qml"),
                                              os.path.join(CraftStandardDirs.craftRoot(), "lib64", "qml"),
                                              os.path.join(CraftStandardDirs.craftRoot(), "lib", "x86_64-linux-gnu",
                                                           "qml")
                                              ])
        self.prependEnvVar("QML_IMPORT_PATH", os.environ["QML2_IMPORT_PATH"])
        self.prependEnvVar("QT_DATA_DIRS", CraftCore.standardDirs.locations.data)

        self.setXDG()

        self.prependEnvVar("PATH", CraftStandardDirs.craftBin())

        # make sure thate craftroot bin is the first to look for dlls etc
        self.prependEnvVar("PATH", os.path.join(CraftStandardDirs.craftRoot(), "bin"))
        self.prependEnvVar("PATH", os.path.join(CraftStandardDirs.craftRoot(), "dev-utils", "bin"))

        # add python site packages to pythonpath
        self.prependEnvVar("PYTHONPATH", os.path.join(CraftStandardDirs.craftRoot(), "lib", "site-packages"))


        if CraftCore.compiler.isClang():
            if OsUtils.isUnix():
                self.addEnvVar("CC", "/usr/bin/clang")
                self.addEnvVar("CXX", "/usr/bin/clang++")
            else:
                if CraftCore.compiler.isMSVC():
                    self.addEnvVar("CC", "clang-cl")
                    self.addEnvVar("CXX", "clang-cl")
                else:
                    self.addEnvVar("CC", "clang")
                    self.addEnvVar("CXX", "clang")
        elif CraftCore.compiler.isGCC():
            if not CraftCore.compiler.isNative() and CraftCore.compiler.isX86():
                self.addEnvVar("CC", "gcc -m32")
                self.addEnvVar("CXX", "g++ -m32")
                self.addEnvVar("AS", "gcc -c -m32")
            else:
                self.addEnvVar("CC", "gcc")
                self.addEnvVar("CXX", "g++")

        if CraftCore.settings.getboolean("General", "AllowAnsiColor", False):
            self.addEnvVar("CLICOLOR_FORCE", "1")
            self.addEnvVar("CLICOLOR", "1")
            if CraftCore.compiler.isClang() and CraftCore.compiler.isMSVC():
                self.prependEnvVar("CFLAGS", "-fcolor-diagnostics -fansi-escape-codes", sep=" ")
                self.prependEnvVar("CXXFLAGS", "-fcolor-diagnostics -fansi-escape-codes", sep=" ")
            elif CraftCore.compiler.isGCCLike():
                self.prependEnvVar("CFLAGS", "-fdiagnostics-color=always", sep=" ")
                self.prependEnvVar("CXXFLAGS", "-fdiagnostics-color=always", sep=" ")

            if OsUtils.isWin():
                os.environ["TERM"] = "xterm" # pretend to be a common smart terminal


    def printEnv(self):
        self.setupEnvironment()
        for key, val in os.environ.items():
            if "\n" in val:
                log(f"Not adding ${key} to environment since it contains "
                     "a newline character and that breaks craftenv.sh")
                continue
            if key.startswith("BASH_FUNC_"):
                continue
            # weird protected env vars
            if key in {"PROFILEREAD"}:
                continue
            CraftCore.log.info(f"{key}={val}")

    @property
    def version(self):
        return CraftCore.settings.version


if __name__ == '__main__':
    helper = SetupHelper()
    helper.run()
