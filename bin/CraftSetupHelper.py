# -*- coding: utf-8 -*-
# Helper script for substitution of paths, independent of cmd or powershell
# copyright:
# Hannah von Reth <vonreth [AT] kde [DOT] org>

import argparse
import collections
import subprocess

from CraftCompiler import craftCompiler
from CraftConfig import *
from CraftDebug import craftDebug
from CraftOS.osutils import OsUtils
# The minimum python version for craft please edit here
# if you add code that changes this requirement
from CraftStandardDirs import CraftStandardDirs, TemporaryUseShortpath

MIN_PY_VERSION = (3, 6, 0)


def log(msg):
    craftDebug.print(msg, sys.stderr)

if sys.version_info[0:3] < MIN_PY_VERSION:
    log("Error: Python too old!")
    log("Craft needs at least Python Version %s.%s.%s" % MIN_PY_VERSION)
    log("Please install it and adapt your CraftSettings.ini")
    exit(1)


class SetupHelper(object):
    CraftVersion = "master"
    def __init__(self, args=None):
        self.args = args

    def _getOutput(self, command):
        craftDebug.log.debug(f"SetupHelper._getOutput: {command}")
        status, output = subprocess.getstatusoutput(command)
        craftDebug.log.debug(f"SetupHelper._getOutput: return {status} {output}")
        return status, output

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
            craftDebug.log.info(craftSettings.get(args.rest[0], args.rest[1], default))
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
        if craftCompiler.isMSVC():
            blackList += ["gcc", "g++"]
        for app in blackList:
            location = shutil.which(app)
            if location:
                location = os.path.dirname(location)
                if not craftSettings.getboolean("ContinuousIntegration", "Enabled", False):
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
            self._getOutput("subst {drive} {path}".format(drive=craftSettings.get("ShortPath", drive),path=path))

        if craftSettings.getboolean("ShortPath", "Enabled", False):
            with TemporaryUseShortpath(False):
                if ("ShortPath", "RootDrive") in craftSettings:
                    _subst(CraftStandardDirs.craftRoot(), "RootDrive")
                if ("ShortPath", "DownloadDrive") in craftSettings:
                    _subst(CraftStandardDirs.downloadDir(), "DownloadDrive")
                if ("ShortPath", "GitDrive") in craftSettings:
                    _subst(CraftStandardDirs.gitDir(), "GitDrive")

        if craftSettings.getboolean("ShortPath", "EnableJunctions", False):
            with TemporaryUseShortpath(False):
                if ("ShortPath", "JunctionDrive") in craftSettings:
                    _subst(CraftStandardDirs.junctionsDir(getDir=True), "JunctionDrive")

    def printBanner(self):
        def printRow(name, value):
            log(f"{name:20}: {value}")

        if CraftStandardDirs.isShortPathEnabled():
            with TemporaryUseShortpath(False):
                printRow("Craft Root", CraftStandardDirs.craftRoot())
        printRow("Craft", CraftStandardDirs.craftRoot())
        printRow("Version", SetupHelper.CraftVersion)
        printRow("ABI", craftCompiler)
        printRow("Svn directory", CraftStandardDirs.svnDir())
        printRow("Git directory", CraftStandardDirs.gitDir())
        printRow("Download directory", CraftStandardDirs.downloadDir())
        if "CraftDeprecatedEntryScript" in os.environ:
            oldScript = os.environ["CraftDeprecatedEntryScript"]
            ext = ".ps1" if OsUtils.isWin() else ".sh"
            log(f"You used the deprecated script {oldScript}\n"
                f"Please use craftenv{ext} instead")

    def addEnvVar(self, key, val):
        os.environ[key] = val
        os.environ[key] = val

    def prependPath(self, key, var):
        if not type(var) == list:
            var = [var]
        if key in os.environ:
            env = var + os.environ[key].split(os.path.pathsep)
            var = list(collections.OrderedDict.fromkeys(env))
        os.environ[key] = os.path.pathsep.join(var)

    def stringToEnv(self, string):
        for line in string.split("\n"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

    def getEnv(self):
        if craftCompiler.isMSVC():
            architectures = {"x86": "x86", "x64": "amd64", "x64_cross": "x86_amd64"}
            version = craftCompiler.getInternalVersion()
            vswhere = os.path.join(CraftStandardDirs.craftBin(), "3rdparty", "vswhere", "vswhere.exe")
            path = subprocess.getoutput(f"\"{vswhere}\""
                                        f"  -version \"[{version},{version+1})\" -property installationPath -legacy -nologo -latest -products *")
            arg = architectures[craftCompiler.architecture] + ("_cross" if not craftCompiler.isNative() else "")
            path = os.path.join(path, "VC")
            if version >= 15:
                path = os.path.join(path, "Auxiliary", "Build")
            path = os.path.join(path, "vcvarsall.bat")
            if not os.path.isfile(path):
                log(f"Failed to setup msvc compiler.\n"
                    f"{path} does not exist.")
                exit(1)
            command = f"\"{path}\" {arg}"
            status, result = subprocess.getstatusoutput(f"{command} > NUL && set")
            craftDebug.log.debug(result)
            if status != 0:
                log(f"Failed to setup msvc compiler.\n"
                    f"Command: {command} ")
                exit(1)
            return self.stringToEnv(result)

        elif craftCompiler.isIntel():
            architectures = {"x86": "ia32", "x64": "intel64"}
            programFiles = os.getenv("ProgramFiles(x86)") or os.getenv("ProgramFiles")
            status, result = subprocess.getstatusoutput(
                "\"%s\\Intel\\Composer XE\\bin\\compilervars.bat\" %s > NUL && set" % (
                    programFiles, architectures[craftCompiler.architecture]))
            if status != 0:
                log("Failed to setup intel compiler")
                exit(1)
            return self.stringToEnv(result)

    def setXDG(self):
        self.prependPath("XDG_DATA_DIRS", [os.path.join(CraftStandardDirs.craftRoot(), "share")])
        if OsUtils.isUnix():
            self.prependPath("XDG_CONFIG_DIRS", [os.path.join(CraftStandardDirs.craftRoot(), "etc", "xdg")])
            self.addEnvVar("XDG_DATA_HOME",
                           os.path.join(CraftStandardDirs.craftRoot(), "home", os.getenv("USER"), ".local5", "share"))
            self.addEnvVar("XDG_CONFIG_HOME",
                           os.path.join(CraftStandardDirs.craftRoot(), "home", os.getenv("USER"), ".config"))
            self.addEnvVar("XDG_CACHE_HOME",
                           os.path.join(CraftStandardDirs.craftRoot(), "home", os.getenv("USER"), ".cache"))

    def setupEnvironment(self):
        for var, value in craftSettings.getSection("Environment"):  # set and overide existing values
            self.addEnvVar(var, value)
        self.prependPath("PATH", os.path.dirname(sys.executable))
        self.getEnv()
        self.checkForEvilApplication()

        self.addEnvVar("KDEROOT", CraftStandardDirs.craftRoot())

        if craftSettings.getboolean("Compile", "UseCCache", False):
            self.addEnvVar("CCACHE_DIR",
                           craftSettings.get("Paths", "CCACHE_DIR", os.path.join(CraftStandardDirs.craftRoot(),
                                                                                 "build", "CCACHE")))

        if self.version < 2:
            self.addEnvVar("GIT_SSH", "plink")
            self.addEnvVar("SVN_SSH", "plink")

        if not "HOME" in os.environ:
            self.addEnvVar("HOME", os.getenv("USERPROFILE"))

        self.prependPath("PKG_CONFIG_PATH", os.path.join(CraftStandardDirs.craftRoot(), "lib", "pkgconfig"))

        self.prependPath("QT_PLUGIN_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "plugins"),
                                            os.path.join(CraftStandardDirs.craftRoot(), "lib", "plugins"),
                                            os.path.join(CraftStandardDirs.craftRoot(), "lib64", "plugins"),
                                            os.path.join(CraftStandardDirs.craftRoot(), "lib", "x86_64-linux-gnu",
                                                         "plugins"),
                                            os.path.join(CraftStandardDirs.craftRoot(), "lib", "plugin")
                                            ])

        self.prependPath("QML2_IMPORT_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "qml"),
                                              os.path.join(CraftStandardDirs.craftRoot(), "lib", "qml"),
                                              os.path.join(CraftStandardDirs.craftRoot(), "lib64", "qml"),
                                              os.path.join(CraftStandardDirs.craftRoot(), "lib", "x86_64-linux-gnu",
                                                           "qml")
                                              ])
        self.prependPath("QML_IMPORT_PATH", os.environ["QML2_IMPORT_PATH"])

        if OsUtils.isUnix():
            self.prependPath("LD_LIBRARY_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "lib"),
                                                 os.path.join(CraftStandardDirs.craftRoot(), "lib",
                                                              "x86_64-linux-gnu")])
        if OsUtils.isMac():
            self.prependPath("DYLD_LIBRARY_PATH", [os.path.join(CraftStandardDirs.craftRoot(), "lib")])

        self.setXDG()

        if craftSettings.getboolean("QtSDK", "Enabled", "false"):
            self.prependPath("PATH",
                             os.path.join(craftSettings.get("QtSDK", "Path"), craftSettings.get("QtSDK", "Version"),
                                          craftSettings.get("QtSDK", "Compiler"), "bin"))

        if craftCompiler.isMinGW():
            if not craftSettings.getboolean("QtSDK", "Enabled", "false"):
                if craftCompiler.isX86():
                    self.prependPath("PATH", os.path.join(CraftStandardDirs.craftRoot(), "mingw", "bin"))
                else:
                    self.prependPath("PATH", os.path.join(CraftStandardDirs.craftRoot(), "mingw64", "bin"))
            else:
                compilerName = craftSettings.get("QtSDK", "Compiler")
                compilerMap = {"mingw53_32": "mingw530_32"}
                self.prependPath("PATH", os.path.join(craftSettings.get("QtSDK", "Path"), "Tools",
                                                      compilerMap.get(compilerName, compilerName), "bin"))

        if OsUtils.isUnix():
            self.prependPath("PATH", CraftStandardDirs.craftBin())
        self.prependPath("PATH", os.path.join(CraftStandardDirs.craftRoot(), "dev-utils", "bin"))

        # make sure thate craftroot bin is the first to look for dlls etc
        self.prependPath("PATH", os.path.join(CraftStandardDirs.craftRoot(), "bin"))

        # add python site packages to pythonpath
        self.prependPath("PythonPath", os.path.join(CraftStandardDirs.craftRoot(), "lib", "site-packages"))

    def printEnv(self):
        self.setupEnvironment()
        for key, val in os.environ.items():
            craftDebug.log.info(f"{key}={val}")

    @property
    def version(self):
        return craftSettings.version


if __name__ == '__main__':
    helper = SetupHelper()
    helper.run()
