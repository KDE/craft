# -*- coding: utf-8 -*-
# Helper script for substitution of paths, independent of cmd or powershell
# copyright:
# Hannah von Reth <vonreth [AT] kde [DOT] org>

import argparse
import collections
import subprocess
import copy

from CraftConfig import *
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
# The minimum python version for craft please edit here
# if you add code that changes this requirement
from CraftStandardDirs import CraftStandardDirs, TemporaryUseShortpath

MIN_PY_VERSION = (3, 6, 0)


def log(msg):
    if not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
        CraftCore.debug.print(msg, sys.stderr)
    else:
        CraftCore.log.debug(msg)


if sys.version_info[0:3] < MIN_PY_VERSION:
    log("Error: Python too old!")
    log("Craft needs at least Python Version %s.%s.%s" % MIN_PY_VERSION)
    log("Please install it and adapt your CraftSettings.ini")
    exit(1)


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
            blackList += ["sh"]
        if CraftCore.compiler.isMSVC():
            blackList += ["gcc", "g++"]
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
        env = copy.deepcopy(os.environ)
        for line in string.split("\n"):
            key, value = line.strip().split("=", 1)
            env[key] = value
        return env

    @staticmethod
    def getMSVCEnv(version=None, architecture="x86", native=True) -> str:
        architectures = {"x86": "x86", "x64": "amd64", "x64_cross": "x86_amd64"}
        vswhere = os.path.join(CraftCore.standardDirs.craftBin(), "3rdparty", "vswhere", "vswhere.exe")
        command = [vswhere, "-property", "installationPath", "-nologo", "-latest"]
        if version:
            command += ["-version", f"[{version},{version+1})"]
            if version < 15:
                command.append("-legacy")
            else:
                command += ["-products", "*", "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64"]
        _, path = SetupHelper._getOutput(command)
        arg = architectures[architecture] + ("_cross" if not native else "")

        # msvc2015: we require the windows 8.1 kit for the correct tools (rc.exe, mt.exe)
        if version == 14:
            arg = f"{arg} 8.1"

        path = os.path.join(path, "VC")
        if not os.path.exists(os.path.join(path, "vcvarsall.bat")):
            path = os.path.join(path, "Auxiliary", "Build")
        path = os.path.join(path, "vcvarsall.bat")
        if not os.path.isfile(path):
            log(f"Failed to setup msvc compiler.\n"
                f"{path} does not exist.")
            exit(1)
        status, result = SetupHelper._getOutput(f"\"{path}\" {arg} > NUL && set", shell=True)
        if status != 0:
            log(f"Failed to setup msvc compiler.\n"
                f"Command: {result} ")
            exit(1)
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
                log("Failed to setup intel compiler")
                exit(1)
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
        self.prependEnvVar("LD_LIBRARY_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "lib"),
                                             os.path.join(CraftStandardDirs.craftRoot(), "lib", "x86_64-linux-gnu")])
        if OsUtils.isMac():
            self.prependEnvVar("DYLD_LIBRARY_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "lib")])

    def _setupWin(self):
        if not "HOME" in os.environ:
            self.addEnvVar("HOME", os.getenv("USERPROFILE"))


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

        if OsUtils.isWin():
            self._setupWin()
        else:
            self.setXDG()

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

        if CraftCore.settings.getboolean("General", "AllowAnsiColor", False):
            self.addEnvVar("CLICOLOR_FORCE", "1")
            self.addEnvVar("CLICOLOR", "1")
            if CraftCore.compiler.isClang() and CraftCore.compiler.isMSVC():
                self.prependEnvVar("CFLAGS", "-fcolor-diagnostics", sep=" ")
                self.prependEnvVar("CXXFLAGS", "-fcolor-diagnostics", sep=" ")
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
            CraftCore.log.info(f"{key}={val}")

    @property
    def version(self):
        return CraftCore.settings.version


if __name__ == '__main__':
    helper = SetupHelper()
    helper.run()
