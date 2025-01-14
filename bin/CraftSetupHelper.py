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
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Utils.CaseInsensitiveDict import CaseInsensitiveDict

# The minimum python version for craft please edit here
# if you add code that changes this requirement
MIN_PY_VERSION = (3, 9, 0)


def log(msg, critical=False):
    CraftCore.debug.print(msg, sys.stderr)
    if critical:
        exit(1)


if sys.version_info[0:3] < MIN_PY_VERSION:
    log(
        "Error: Python too old!\n" "Craft needs at least Python Version %s.%s.%s\n" "Please install it and adapt your CraftSettings.ini" % MIN_PY_VERSION,
        critical=True,
    )

if not platform.machine().endswith("64"):
    log(
        f"Craft requires a 64bit operating system. Your are using: {platform.machine()}",
        critical=True,
    )


class SetupHelper(object):
    NeedsSetup = "KDEROOT" not in os.environ

    def __init__(self, args=None):
        self.args = args
        if CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
            CraftCore.settings.set("General", "AllowAnsiColor", "False")

        if SetupHelper.NeedsSetup:
            SetupHelper.NeedsSetup = False
            self.checkForEvilApplication()
            self.setupEnvironment()

    @staticmethod
    def _getOutput(command, shell=False):
        CraftCore.log.debug(f"SetupHelper._getOutput: {command}")
        p = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=shell,
            universal_newlines=True,
            errors="backslashreplace",
        )
        out = p.stdout.strip()
        CraftCore.log.debug(f"SetupHelper._getOutput: return {p.returncode} {out}")
        return p.returncode, out

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--get", action="store_true")
        parser.add_argument("--print-banner", action="store_true")
        parser.add_argument("--getenv", action="store_true")
        parser.add_argument("--setup", action="store_true")
        parser.add_argument("--format", action="store", choices=["json", "text", "null"], default="text")
        parser.add_argument("rest", nargs=argparse.REMAINDER)
        args = parser.parse_args()

        if args.get:
            default = ""
            if len(args.rest) == 3:
                default = args.rest[2]
            CraftCore.log.info(CraftCore.settings.get(args.rest[0], args.rest[1], default))
        elif args.print_banner:
            self.printBanner()
        elif args.getenv:
            self.printEnv(args.format)
        elif args.setup:
            self.printEnv(args.format)
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
                        f'Found "{app}" in your PATH: "{location}"\n'
                        f"This application is known to cause problems with your configuration of Craft.\n"
                        f"Please remove it from PATH or manually set a value for PATH in your CraftSettings.ini:\n"
                        f"\n"
                        f"[Environment]\n"
                        f"PATH="
                        f"\n"
                    )
                else:
                    path = collections.OrderedDict.fromkeys(os.environ["Path"].split(os.path.pathsep))
                    del path[location]
                    self.addEnvVar("Path", os.path.pathsep.join(path))

    @staticmethod
    def printBanner():
        def printRow(name, value):
            log(f"{name:20}: {value}")

        printRow("Craft", CraftCore.standardDirs.craftRoot())
        printRow("ABI", CraftCore.compiler)
        printRow("Download directory", CraftCore.standardDirs.downloadDir())
        printRow("Cache repository", ", ".join(CraftCore.settings.cacheRepositoryUrls()))

    def addEnvVar(self, key, val):
        os.environ[key] = str(val)

    def removeEnvVar(self, key):
        if key in os.environ:
            del os.environ[key]

    def addDefaultEnvVar(self, key, val):
        if key not in os.environ:
            self.addEnvVar(key, val)

    def prependEnvVar(self, key: str, var: str, sep: str = os.path.pathsep) -> None:
        if not isinstance(var, list):
            var = [var]
        if key in os.environ:
            env = var + os.environ[key].split(sep)
            var = list(collections.OrderedDict.fromkeys(env))
        val = sep.join([str(x) for x in var])
        CraftCore.log.debug(f"Setting {key}={val}")
        os.environ[key] = val

    @staticmethod
    def _callVCVER(version: int, args: list = None, native: bool = True, prerelease: bool = False) -> str:
        if not args:
            args = []
        vswhere = os.path.join(CraftCore.standardDirs.craftBin(), "3rdparty", "vswhere", "vswhere.exe")
        command = [vswhere, "-property", "installationPath", "-nologo", "-latest", "-products", "*"]
        if prerelease:
            command += ["-prerelease"]
        if version:
            command += ["-version", f"[{version},{version+1})"]
            if version < 15:
                command.append("-legacy")
            else:
                if not args:
                    if native:
                        # this fails with express versions
                        args = [
                            "-requires",
                            "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                        ]
        return SetupHelper._getOutput(command + args)[1]

    @staticmethod
    def getMSVCEnv(
        version: int = 0,
        architecture=None,
        toolset=None,
        native=True,
    ) -> str:
        if not architecture:
            architecture = CraftCore.compiler.Architecture.x86_64
        if native:
            architectures = {
                CraftCore.compiler.Architecture.x86_32: "amd64_x86",
                CraftCore.compiler.Architecture.x86_64: "amd64",
            }
        else:
            architectures = {
                CraftCore.compiler.Architecture.x86_32: "x86",
                CraftCore.compiler.Architecture.x86_64: "x86_amd64",
            }

        args = architectures[architecture]
        path = ""
        # we prefer newer compiler that provide legacy toolchains
        if version:
            if version == 16:
                # todo find a more generic id
                component = "Microsoft.VisualStudio.Component.VC.14.29.16.11.x86.x64"
            else:
                component = "Microsoft.VisualStudio.Component.VC."
                if version == 14:
                    component += str(CraftCore.compiler.getMsvcPlatformToolset())
                else:
                    component += f"v{CraftCore.compiler.getMsvcPlatformToolset()}.x86.x64"
            # todo directly get the correct version
            for v in [17, 16, 15]:
                path = SetupHelper._callVCVER(v, args=["-products", "*", "-requires", component], native=native)
                if path:
                    if not toolset:
                        toolset = str(CraftCore.compiler.getMsvcPlatformToolset() / 10)
                    break

        if toolset:
            args += f" -vcvars_ver={toolset}"

        if not path:
            path = SetupHelper._callVCVER(version, native=native)
            if not path:
                path = SetupHelper._callVCVER(version, native=native, prerelease=True)
                if path:
                    log("Found MSVS only in a prerelease version. I will use that.")
        if not path:
            log(
                "Unable to locate Visual Studio.  Please install it with the C++ component. Aborting.",
                critical=True,
            )

        path = os.path.join(path, "VC")
        if not os.path.exists(os.path.join(path, "vcvarsall.bat")):
            path = os.path.join(path, "Auxiliary", "Build")
        path = os.path.join(path, "vcvarsall.bat")
        if not os.path.isfile(path):
            log(
                f"Failed to setup msvc compiler.\n" f"{path} does not exist.",
                critical=True,
            )
        status, result = SetupHelper._getOutput(f'"{path}" {args} > NUL && "{sys.executable}" "{Path(__file__).parent}/dumpenv.py"', shell=True)
        if status != 0:
            log(f"Failed to setup msvc compiler.\n" f"Command: {result} ", critical=True)
        return CaseInsensitiveDict(json.loads(result))

    def getEnv(self):
        if CraftCore.compiler.isMSVC():
            return SetupHelper.getMSVCEnv(
                CraftCore.compiler.getInternalVersion(),
                CraftCore.compiler.architecture,
                CraftCore.compiler.msvcToolset,
                CraftCore.compiler.isNative(),
            )
        return os.environ

    def setXDG(self):
        if OsUtils.isWin():
            self.prependEnvVar(
                "XDG_DATA_DIRS",
                [os.path.join(CraftCore.standardDirs.craftRoot(), "bin/data")],
            )
        else:
            self.prependEnvVar(
                "XDG_DATA_DIRS",
                [os.path.join(CraftCore.standardDirs.craftRoot(), "share")],
            )
            user = os.getenv("USER", self._getOutput(["id", "-u", "-n"])[1])
            self.prependEnvVar(
                "XDG_CONFIG_DIRS",
                [os.path.join(CraftCore.standardDirs.craftRoot(), "etc", "xdg")],
            )
            self.addEnvVar(
                "XDG_DATA_HOME",
                os.path.join(CraftCore.standardDirs.craftRoot(), "home", user, ".local5", "share"),
            )
            self.addEnvVar(
                "XDG_CONFIG_HOME",
                os.path.join(CraftCore.standardDirs.craftRoot(), "home", user, ".config"),
            )
            self.addEnvVar(
                "XDG_CACHE_HOME",
                os.path.join(CraftCore.standardDirs.craftRoot(), "home", user, ".cache"),
            )

    def _setupUnix(self):
        craftLibDir = CraftCore.standardDirs.craftRoot() / "lib"

        if CraftCore.compiler.isFreeBSD:
            self.prependEnvVar("LD_LIBRARY_PATH", [craftLibDir])
            self.prependEnvVar("LDFLAGS", ["-Wl,-rpath,'$ORIGIN/../lib'", f"-L{craftLibDir}"], sep=" ")
        elif CraftCore.compiler.isLinux:
            # we will later replace the hard coded path in BuildSystemBase.internalPostInstall
            self.prependEnvVar("LDFLAGS", [f"-Wl,-rpath,{craftLibDir}", f"-L{craftLibDir}"], sep=" ")
        self.prependEnvVar(
            "BISON_PKGDATADIR",
            os.path.join(CraftCore.standardDirs.craftRoot(), "share", "bison"),
        )
        self.prependEnvVar("M4", os.path.join(CraftCore.standardDirs.craftRoot(), "bin", "m4"))

        # use the system fonts, keep the logic in sync with AppImagePackager
        fontConfigPath = Path("/etc/fonts")
        self.addEnvVar("FONTCONFIG_PATH", fontConfigPath if fontConfigPath.exists() else CraftCore.standardDirs.craftRoot() / "etc/fonts")

    def _setupMac(self):
        # self.prependEnvVar("DYLD_LIBRARY_PATH", os.path.join(CraftCore.standardDirs.craftRoot(), "lib"))
        # we will later replace the hard coded path in BuildSystemBase.internalPostInstall
        self.prependEnvVar(
            "LDFLAGS",
            [f"-Wl,-rpath,{CraftCore.standardDirs.craftRoot() / 'lib'}", f"-L{CraftCore.standardDirs.craftRoot() / 'lib'}"],
            sep=" ",
        )
        if CraftCore.compiler.macOSDeploymentTarget < 12:
            # https://developer.apple.com/documentation/xcode-release-notes/xcode-15-release-notes
            # Binaries using symbols with a weak definition crash at runtime on iOS 14/macOS 12 or older. This impacts primarily C++ projects due to their extensive use of weak symbols. (114813650) (FB13097713)
            # Workaround: Bump the minimum deployment target to iOS 15, macOS 12, watchOS 8 or tvOS 15, or add -Wl,-ld_classic to the OTHER_LDFLAGS build setting.
            try:
                # does ld support -ld_classic
                subprocess.check_call(
                    """echo "int main() {}" | /usr/bin/clang "-Wl,-ld_classic" -x c++ - -o /dev/null""", shell=True, stderr=subprocess.DEVNULL
                )
                self.prependEnvVar(
                    "LDFLAGS",
                    ["-Wl,-ld_classic"],
                    sep=" ",
                )
            except:
                pass
        self.addEnvVar(
            "MACOSX_DEPLOYMENT_TARGET",
            str(CraftCore.compiler.macOSDeploymentTarget),
        )
        self.prependEnvVar(
            "BISON_PKGDATADIR",
            os.path.join(CraftCore.standardDirs.craftRoot(), "share", "bison"),
        )
        self.prependEnvVar("M4", os.path.join(CraftCore.standardDirs.craftRoot(), "bin", "m4"))
        try:
            dbusInstalled = bool(CraftCore.installdb.isInstalled("libs/dbus"))
        except sqlite3.OperationalError:
            # db might be locked
            dbusInstalled = False

        if dbusInstalled:
            serviceAgent = os.path.join(
                CraftCore.standardDirs.craftRoot(),
                "Library",
                "LaunchAgents",
                "org.freedesktop.dbus-session.plist",
            )
            if os.path.exists(serviceAgent):
                SetupHelper._getOutput(["launchctl", "load", "-Fw", serviceAgent])

    def _setupWin(self):
        self.addEnvVar("PYTHONUTF8", "1")
        if "HOME" not in os.environ:
            self.addEnvVar("HOME", os.getenv("USERPROFILE"))

        self.addEnvVar(
            "QTWEBENGINE_RESOURCES_PATH",
            os.path.join(CraftCore.standardDirs.craftRoot(), "bin"),
        )

        if CraftCore.compiler.isMinGW():
            self.prependEnvVar(
                "PATH",
                os.path.join(CraftCore.standardDirs.craftRoot(), "mingw64", "bin"),
            )

    def _setupAndroid(self):
        self.addEnvVar("ANDROID_ARCH", CraftCore.compiler.androidArchitecture)
        self.addEnvVar("ANDROID_ARCH_ABI", CraftCore.compiler.androidAbi)

    def setupEnvironment(self):
        originaleEnv = CaseInsensitiveDict(os.environ)

        # don't propagate a possibly set mkspec from the outside
        self.removeEnvVar("QMAKESPEC")

        for var, value in CraftCore.settings.getSection("Environment"):  # set and override existing values
            # the ini is case insensitive so sections are lowercase....
            self.addEnvVar(var.upper(), value)
        os.environ.update(self.getEnv())

        self.addEnvVar("KDEROOT", CraftCore.standardDirs.craftRoot())
        # only set if not already explicitly set
        self.addDefaultEnvVar("SSL_CERT_FILE", CraftCore.standardDirs.etcDir() / "cacert.pem")
        self.addDefaultEnvVar("REQUESTS_CA_BUNDLE", CraftCore.standardDirs.etcDir() / "cacert.pem")

        if CraftCore.settings.getboolean("Compile", "UseCCache", False):
            self.addDefaultEnvVar(
                "CCACHE_DIR",
                CraftCore.settings.get(
                    "Paths",
                    "CCACHE_DIR",
                    os.path.join(CraftCore.standardDirs.craftRoot(), "build", "CCACHE"),
                ),
            )

        if OsUtils.isWin():
            self._setupWin()
        elif OsUtils.isMac():
            self._setupMac()
        elif CraftCore.compiler.isAndroid:
            self._setupAndroid()
        else:
            self._setupUnix()

        PKG_CONFIG_PATH = collections.OrderedDict.fromkeys([os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "pkgconfig")])
        if "PKG_CONFIG_PATH" in originaleEnv:
            PKG_CONFIG_PATH.update(collections.OrderedDict.fromkeys(originaleEnv["PKG_CONFIG_PATH"].split(os.path.pathsep)))
        else:
            pkgCOnfig = shutil.which("pkg-config", path=originaleEnv["PATH"])
            if pkgCOnfig:
                out = self._getOutput("pkg-config --variable pc_path pkg-config", shell=True)
                if out[0] == 0:
                    PKG_CONFIG_PATH.update(collections.OrderedDict.fromkeys(out[1].split(os.path.pathsep)))
        self.prependEnvVar("PKG_CONFIG_PATH", os.path.pathsep.join(PKG_CONFIG_PATH.keys()))

        self.prependEnvVar(
            "QT_PLUGIN_PATH",
            [
                CraftCore.standardDirs.craftRoot() / "plugins",
                CraftCore.standardDirs.craftRoot() / "lib/plugins",
                CraftCore.standardDirs.craftRoot() / "lib64/plugins",
                CraftCore.standardDirs.craftRoot() / "lib/x86_64-linux-gnu/plugins",
                CraftCore.standardDirs.craftRoot() / "lib/plugin",
            ],
        )

        self.prependEnvVar(
            "QML2_IMPORT_PATH",
            [
                CraftCore.standardDirs.craftRoot() / "qml",
                CraftCore.standardDirs.craftRoot() / "lib/qml",
                CraftCore.standardDirs.craftRoot() / "lib64/qml",
                CraftCore.standardDirs.craftRoot() / "lib/x86_64-linux-gnu/qml",
            ],
        )
        self.prependEnvVar("QML_IMPORT_PATH", os.environ["QML2_IMPORT_PATH"])
        self.prependEnvVar("QT_DATA_DIRS", CraftCore.standardDirs.locations.data)
        # force unit tests to not crop the log
        self.addEnvVar("QTEST_MAX_WARNINGS", 0)

        if CraftCore.settings.getboolean("General", "UseSandboxConfig", True):
            self.setXDG()

        self.prependEnvVar("PATH", CraftCore.standardDirs.craftBin())

        # add python site packages to pythonpath
        if CraftCore.compiler.isMacOS:
            self.prependEnvVar(
                "PYTHONPATH",
                CraftCore.standardDirs.craftRoot() / "lib/Python.framework/Versions/Current/lib/site-packages",
            )
        else:
            # yes, this path is correct: we created it as a symlink in the libs\python blueprint
            self.prependEnvVar(
                "PYTHONPATH",
                CraftCore.standardDirs.craftRoot() / "lib/python/site-packages",
            )

        # prepend our venv python
        self.prependEnvVar(
            "PATH",
            [
                os.path.join(
                    CraftCore.standardDirs.etcDir(),
                    "virtualenv",
                    "3",
                    "Scripts" if CraftCore.compiler.isWindows else "bin",
                ),
            ],
        )

        # make sure that craftroot bin is the first to look for dlls etc
        self.prependEnvVar(
            "PATH",
            [CraftCore.standardDirs.craftRoot() / "dev-utils/bin", CraftCore.standardDirs.craftRoot() / "bin", CraftCore.standardDirs.craftRoot() / "libexec"],
        )

        if CraftCore.compiler.isClang() and not CraftCore.compiler.isAndroid:
            if OsUtils.isUnix() and CraftCore.settings.getboolean("General", "UseSystemClang", True):
                self.addEnvVar("CC", "/usr/bin/clang")
                self.addEnvVar("CXX", "/usr/bin/clang++")
            else:
                if CraftCore.compiler.isMSVC():
                    self.addDefaultEnvVar("CC", "clang-cl")
                    self.addDefaultEnvVar("CXX", "clang-cl")
                else:
                    self.addDefaultEnvVar("CC", "clang")
                    self.addDefaultEnvVar("CXX", "clang")
        elif CraftCore.compiler.isGCC():
            if not CraftCore.compiler.isNative() and CraftCore.compiler.architecture == CraftCore.compiler.Architecture.x86_32:
                self.addEnvVar("CC", "gcc -m32")
                self.addEnvVar("CXX", "g++ -m32")
                self.addEnvVar("AS", "gcc -c -m32")
            else:
                self.addDefaultEnvVar("CC", "gcc")
                self.addDefaultEnvVar("CXX", "g++")
        elif CraftCore.compiler.isMSVC():
            self.addDefaultEnvVar("CC", "cl")
            self.addDefaultEnvVar("CXX", "cl")

        if CraftCore.settings.getboolean(
            "General",
            "AllowAnsiColor",
            not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False),
        ):
            # different non standard env switches
            self.addEnvVar("CLICOLOR_FORCE", "1")
            self.addEnvVar("CLICOLOR", "1")
            self.addEnvVar("ANSICON", "1")
            if CraftCore.compiler.isClang() and CraftCore.compiler.isMSVC():
                self.prependEnvVar("CFLAGS", "-fcolor-diagnostics -fansi-escape-codes", sep=" ")
                self.prependEnvVar("CXXFLAGS", "-fcolor-diagnostics -fansi-escape-codes", sep=" ")
            elif CraftCore.compiler.isGCCLike():
                self.prependEnvVar("CFLAGS", "-fdiagnostics-color=always", sep=" ")
                self.prependEnvVar("CXXFLAGS", "-fdiagnostics-color=always", sep=" ")

            if OsUtils.isWin():
                self.addEnvVar("TERM", "xterm-256color")  # pretend to be a common smart terminal

    def printEnv(self, format: str):
        self.setupEnvironment()

        if format in ("null", "text"):
            envToDump = {}

            for key, val in os.environ.items():
                if key.startswith("BASH_FUNC_"):
                    continue

                # weird protected env vars
                if key in {"PROFILEREAD"}:
                    continue

                if format == "text" and "\n" in val:
                    log(f"Not adding ${key} to environment since it contains " "a newline character")
                    continue

                envToDump[key] = val

            if format == "null":
                end = "\0"
            else:
                end = "\n"

            CraftCore.log.info(end.join((f"{key}={val}" for key, val in envToDump.items())))

            return

        elif format == "json":
            CraftCore.log.info(json.dumps(dict(os.environ)))

            return

        raise RuntimeError(f"unsupported format: {format}")

    @property
    def version(self):
        return CraftCore.settings.version


helper = SetupHelper()
if __name__ == "__main__":
    helper.run()
