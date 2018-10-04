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

import re
from enum import unique, IntFlag

import utils
from CraftConfig import *
from CraftCore import CraftCore
from CraftDebug import deprecated


class CraftCompiler(object):
    class Platforms(IntFlag):
        NoPlatform  = 0
        Windows     = 0x1 << 0
        Linux       = 0x1 << 1
        MacOS       = 0x1 << 2
        FreeBSD     = 0x1 << 3

        Unix        = Linux | MacOS | FreeBSD
        All         = ~0

        # define inverted values to allow usage in info.ini
        NotLinux     = ~Linux
        NotMacOS     = ~MacOS
        NotFreeBSD   = ~FreeBSD
        NotWindows   = Unix
        NotUnix      = ~Unix

        @classmethod
        def fromString(cls, name):
            if not hasattr(cls, "__sting_map"):
                cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
            return cls.__sting_map[name.lower()]

    @unique
    class Compiler(IntFlag):
        NoCompiler  = 0
        CL          = 0x1 << 0
        GCC         = 0x1 << 1
        CLANG       = 0x1 << 2

        GCCLike     = CLANG | GCC
        All         = ~0


        @classmethod
        def fromString(cls, name):
            if not hasattr(cls, "__sting_map"):
                cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
            return cls.__sting_map[name.lower()]


    def __init__(self):
        compiler = CraftCore.settings.get("General", "KDECOMPILER", "")
        if compiler != "":
            arch = "32" if CraftCore.settings.get("General", "Architecture") == "x86" else "64"
            if compiler.startswith("msvc"):
                split = ["windows", f"{compiler}_{arch}", "cl"]
            elif compiler.startswith("mingw"):
                split = ["windows", f"mingw_{arch}", "gcc"]
            elif compiler.startswith("linux"):
                split = ["linux", "gcc"]
            elif compiler.startswith("mac"):
                split = ["macos", "clang"]
            if not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
                print(f"Your using the old compiler setting\n"
                      f"\t[General]\n"
                      f"\tKDECOMPILER={compiler}\n"
                      f"please update your settings to\n"
                      f"\t[General]\n"
                      f"\tABI=" + "-".join(split),
                      file=sys.stderr)
        else:
            split = CraftCore.settings.get("General", "ABI").split("-")
        if len(split) != 3:
            raise Exception("Invalid compiler: " + CraftCore.settings.get("General", "ABI"))

        platform, self._abi, compiler = split

        self._compiler = CraftCompiler.Compiler.fromString(compiler)
        self._platform = CraftCompiler.Platforms.fromString(platform)

        self._architecture = "x86" if self._abi.endswith("32") else "x64"

    def __str__(self):
        return "-".join(self.signature)

    @property
    def signature(self):
        return self.platform.name.lower(), self.abi, self.compiler.name.lower()

    @property
    def platform(self) -> Platforms:
        return self._platform

    @property
    def abi(self):
        return self._abi

    @property
    def compiler(self) -> Compiler:
        return self._compiler

    @property
    def architecture(self):
        return self._architecture

    @property
    def gnuArchitecture(self):
        return "x86" if self.isX86() else "x86_64"

    @property
    def bits(self):
        return "64" if self.isX64() else "32"

    def _getGCCTarget(self):
        _, result = CraftCore.cache.getCommandOutput("gcc", "-dumpmachine")
        if result:
            result = result.strip()
            CraftCore.log.debug(f"GCC Target Processor: {result}")
        else:
            # if no mingw is installed return mingw-w32 it is part of base
            if self.isX64():
                result = "x86_64-w64-mingw32"
            else:
                result = "i686-w64-mingw32"
        return result

    @property
    def macOSDeploymentTarget(self) -> str:
        assert self.macUseSDK
        return "10.11"

    @property
    def macUseSDK(self) -> bool:
        assert self.isMacOS
        """Whether to compile against the macOS SDK instead of the libraries in /usr (off by default)"""
        return CraftCore.settings.getboolean("MacSDK", "Enabled", "False")

    @property
    def isWindows(self) -> bool:
        return self.platform == CraftCompiler.Platforms.Windows

    @property
    def isMacOS(self) -> bool:
        return self.platform == CraftCompiler.Platforms.MacOS

    @property
    def isLinux(self) -> bool:
        return self.platform == CraftCompiler.Platforms.Linux

    @property
    def isFreeBSD(self) -> bool:
        return self.platform == CraftCompiler.Platforms.FreeBSD

    @property
    def isUnix(self) -> bool:
        return bool(self.platform & CraftCompiler.Platforms.Unix)

    @property
    def executableSuffix(self):
        return ".exe" if self.isWindows else ""

    def isNative(self):
        # TODO: any reason to keep that?
        # tahts actually curretly only for msvc express
        return CraftCore.settings.getboolean("General", "Native", True)

    def isX64(self):
        return self.architecture == "x64"

    def isX86(self):
        return self.architecture == "x86"

    def isGCC(self) -> bool:
        return self.compiler == CraftCompiler.Compiler.GCC

    def isClang(self) -> bool:
        return self.compiler == CraftCompiler.Compiler.CLANG

    def isGCCLike(self) -> bool:
        return bool(self.compiler & CraftCompiler.Compiler.GCCLike)

    def isCl(self) -> bool:
        return self.compiler == CraftCompiler.Compiler.CL

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

    @deprecated("CraftCore.compiler")
    def getCompilerName(self):
        return str(CraftCore.compiler)

    @deprecated("CraftCore.compiler")
    def getSimpleCompilerName(self):
        return str(CraftCore.compiler)

    def getGCCLikeVersion(self, compilerExecutable):
        _, result = CraftCore.cache.getCommandOutput(compilerExecutable, "--version")
        if result:
            result = re.findall("\d+\.\d+\.?\d*", result)[0]
            CraftCore.log.debug("{0} Version: {1}".format(compilerExecutable, result))
        return result or "0"

    def getVersion(self):
        if self.isGCCLike():
            return self.getGCCLikeVersion(self.compiler.name)
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
            CraftCore.log.critical(f"Unknown MSVC Compiler {self.abi}")
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
            CraftCore.log.critical(f"Unknown MSVC Compiler {self.abi}")
        return versions[c]

if __name__ == '__main__':
    print("Testing Compiler.py")
    print(f"Configured compiler (ABI): {CraftCore.compiler}")
    print("Version: %s" % CraftCore.compiler.getVersionWithName())
    print("Compiler Name: %s" % CraftCore.compiler.getCompilerName())
    print("Native compiler: %s" % ("No", "Yes")[CraftCore.compiler.isNative()])
    if CraftCore.compiler.isGCCLike():
        print("Compiler Version: %s" % CraftCore.compiler.getGCCLikeVersion(CraftCore.compiler.compiler.name))
        if CraftCore.compiler.isGCC():
            print("Compiler Target: %s" % CraftCore.compiler._getGCCTarget())
    if CraftCore.compiler.isMacOS:
        print("Using SDK for macOS:", CraftCore.compiler.macUseSDK)
        if CraftCore.compiler.macUseSDK:
            print("macOS SDK deployment target:", CraftCore.compiler.macOSDeploymentTarget)
