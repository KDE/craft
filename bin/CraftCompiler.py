# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Hannah von Reth <vonreth@kde.org>

import utils
from CraftConfig import *
from CraftDebug import craftDebug, deprecated


class CraftCompiler(object):
    __supportedPlatforms = ["windows", "linux", "macos", "freebsd"]

    def __init__(self):
        compiler = craftSettings.get("General", "KDECOMPILER", "")
        if compiler != "":
            arch = "32" if craftSettings.get("General", "Architecture") == "x86" else "64"
            if compiler.startswith("msvc"):
                split = ["windows", f"{compiler}_{arch}", "cl"]
            elif compiler.startswith("mingw"):
                split = ["windows", f"mingw_{arch}", "gcc"]
            elif compiler.startswith("linux"):
                split = ["linux", "gcc"]
            elif compiler.startswith("mac"):
                split = ["macos", "clang"]
            if not craftSettings.getboolean("ContinuousIntegration", "Enabled", False):
                print(f"Your using the old compiler setting\n"
                      f"\t[General]\n"
                      f"\tKDECOMPILER={compiler}\n"
                      f"please update your settings to\n"
                      f"\t[General]\n"
                      f"\tABI=" + "-".join(split),
                      file=sys.stderr)
        else:
            split = craftSettings.get("General", "ABI").split("-")
        if len(split) != 3:
            raise Exception("Invalid compiler: " + craftSettings.get("General", "ABI"))

        self._platform, self._abi, self._compiler = split

        self._architecture = "x86" if self._abi.endswith("32") else "x64"

        if not self._platform in CraftCompiler.__supportedPlatforms:
            raise Exception("Unsupported platform: " + self._platform)

    def __str__(self):
        return "-".join(self.signature)

    @property
    def signature(self):
        return self.platform, self.abi, self.compiler

    @property
    def platform(self):
        return self._platform

    @property
    def abi(self):
        return self._abi

    @property
    def compiler(self):
        return self._compiler

    @property
    def architecture(self):
        return self._architecture

    def _getGCCTarget(self):
        result = utils.utilsCache.getCommandOutput("gcc", "-dumpmachine")
        if result:
            result = result.strip()
            craftDebug.log.debug(f"GCC Target Processor: {result}")
        else:
            # if no mingw is installed return mingw-w32 it is part of base
            if self.isX64():
                result = "x86_64-w64-mingw32"
            else:
                result = "i686-w64-mingw32"
        return result

    def isNative(self):
        # TODO: any reason to keep that?
        return craftSettings.getboolean("General", "Native", True)

    def isX64(self):
        return self.architecture == "x64"

    def isX86(self):
        return self.architecture == "x86"

    def isGCC(self):
        return self.compiler == "gcc"

    def isClang(self):
        return self.compiler == "clang"

    def isGCCLike(self):
        return self.isGCC() or self.isClang()

    def isCl(self):
        return self.compiler == "cl"

    def isMinGW(self):
        return self.abi.startswith("mingw")

    def isMinGW_W32(self):
        return self.isMinGW() and self.isX86()

    def isMinGW_W64(self):
        return self.isMinGW() and self.isX64()

    def isMSVC(self):
        return self.abi.startswith("msvc")

    def isMSVC2010(self):
        return self.abi.startswith("msvc2010")

    def isMSVC2012(self):
        return self.abi.startswith("msvc2012")

    def isMSVC2013(self):
        return self.abi.startswith("msvc2013")

    def isMSVC2015(self):
        return self.abi.startswith("msvc2015")

    def isMSVC2017(self):
        return self.abi.startswith("msvc2017")

    def isIntel(self):
        return self.compiler == "intel"

    @deprecated("self.compiler")
    def getCompilerExecutableName(self):
        return self.compiler

    @deprecated("craftCompiler")
    def getCompilerName(self):
        return str(craftCompiler)

    @deprecated("craftCompiler")
    def getSimpleCompilerName(self):
        return str(craftCompiler)

    def getGCCLikeVersion(self, compilerExecutable):
        result = utils.utilsCache.getCommandOutput(compilerExecutable, "--version")
        if result:
            result = re.findall("\d+\.\d+\.?\d*", result)[0]
            craftDebug.log.debug("{0} Version: {1}".format(compilerExecutable, result))
        return result or "0"

    def getVersion(self):
        if self.isGCCLike():
            return self.getGCCLikeVersion(self.getCompilerExecutableName())
        elif self.isMSVC():
            return self.getInternalVersion()
        else:
            return None

    def getVersionWithName(self):
        if self.isGCCLike():
            return f"{self.getCompilerName()} {self.getVersion()}"
        elif self.isIntel():
            return os.getenv("PRODUCT_NAME_FULL")
        elif self.isMSVC():
            return f"Microsoft Visual Studio {self.getVersion()}"
        else:
            return None

    def getShortName(self):
        if not self.isMSVC():
            return self.getCompilerName()
        return f"vc{self.getInternalVersion()}"

    def getInternalVersion(self):
        if not self.isMSVC():
            return self.getVersion()
        versions = {
            "msvc2010": 10,
            "msvc2012": 11,
            "msvc2013": 12,
            "msvc2015": 14,
            "msvc2017": 15
        }
        c = self.abi.split("_")[0]
        if c not in versions:
            craftDebug.log.critical(f"Unknown MSVC Compiler {self.abi}")
        return versions[c]

    def getMsvcPlatformToolset(self):
        versions = {
            "msvc2010": 100,
            "msvc2012": 110,
            "msvc2013": 120,
            "msvc2015": 140,
            "msvc2017": 141
        }
        c = self.abi.split("_")[0]
        if c not in versions:
            craftDebug.log.critical(f"Unknown MSVC Compiler {self.abi}")
        return versions[c]


craftCompiler = CraftCompiler()

if __name__ == '__main__':
    print("Testing Compiler.py")
    print(f"Configured compiler (ABI): {craftCompiler}")
    print("Version: %s" % craftCompiler.getVersionWithName())
    print("Compiler Name: %s" % craftCompiler.getCompilerName())
    print("Native compiler: %s" % ("No", "Yes")[craftCompiler.isNative()])
    if craftCompiler.isGCCLike():
        print("Compiler Version: %s" % craftCompiler.getGCCLikeVersion(craftCompiler.getCompilerExecutableName()))
        print("Compiler Target: %s" % craftCompiler._getGCCTarget())
