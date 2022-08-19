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
    class Architecture(IntFlag):
        x86     = 0x1 << 0
        x86_32  = 0x1 << 1 | x86
        x86_64  = 0x1 << 2 | x86
        arm     = 0x1 << 3
        arm32   = 0x1 << 4 | arm
        arm64   = 0x1 << 5 | arm
        arm64e  = 0x1 << 6 | arm64 # Apple
        # TODO:...

        @classmethod
        def fromString(cls, name):
            if not hasattr(cls, "__sting_map"):
                cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
            return cls.__sting_map[name.lower()]

    class Platforms(IntFlag):
        NoPlatform  = 0
        Windows     = 0x1 << 0
        Linux       = 0x1 << 1
        MacOS       = 0x1 << 2
        FreeBSD     = 0x1 << 3
        Android     = 0x1 << 4

        Unix        = Linux | MacOS | FreeBSD
        All         = ~0

        # define inverted values to allow usage in info.ini
        NotLinux     = ~Linux
        NotMacOS     = ~MacOS
        NotFreeBSD   = ~FreeBSD
        NotWindows   = ~Windows
        NotUnix      = ~Unix
        NotAndroid   = ~Android

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
        split = CraftCore.settings.get("General", "ABI").split("-")
        if len(split) != 3:
            raise Exception("Invalid compiler: " + CraftCore.settings.get("General", "ABI"))

        platform, self._abi, compiler = split

        self._compiler = CraftCompiler.Compiler.fromString(compiler)
        self._platform = CraftCompiler.Platforms.fromString(platform)

        self._MSVCToolset = None
        if self.isMSVC():
            self._MSVCToolset = CraftCore.settings.get("General", "MSVCToolset", "")

        if self.isAndroid:
            self._architecture = self._architecture = CraftCompiler.Architecture.fromString(arch)
            if self.architecture == CraftCompiler.Architecture.arm:
                self._abi = "armeabi-v7a"
            elif self.architecture == CraftCompiler.Architecture.arm64:
                self._abi = "arm64-v8a"
            self._apiLevel = CraftCore.settings.get("General", "AndroidAPI", 21)
        else:
            arch = self._abi.split("_", 1)[-1]
            if arch == "32":
                # legacy
                self._architecture = CraftCompiler.Architecture.x86_32
            elif arch == "64":
                # legacy
                self._architecture = CraftCompiler.Architecture.x86_64
            else:
                self._architecture = CraftCompiler.Architecture.fromString(arch)


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
    def architecture(self) -> Architecture:
        return self._architecture

    @property
    def msvcToolset(self):
        return self._MSVCToolset

    @property
    def bits(self) -> str:
        if self.architecture in {CraftCompiler.Architecture.x86_64, CraftCompiler.Architecture.arm64}:
            return "64"
        if self.architecture in {CraftCompiler.Architecture.x86_32, CraftCompiler.Architecture.arm32}:
            return "32"
        raise Exception("Unsupported architecture")

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
    def isAndroid(self) -> bool:
        return self.platform == CraftCompiler.Platforms.Android

    @property
    def isUnix(self) -> bool:
        return bool(self.platform & CraftCompiler.Platforms.Unix)

    @property
    def executableSuffix(self):
        return ".exe" if self.isWindows else ""

    def isNative(self):
        return CraftCore.settings.getboolean("General", "Native", True)

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
        return self.isMinGW() and self.architecture == CraftCompiler.Architecture.x86_32

    def isMinGW_W64(self):
        return self.isMinGW() and self.architecture == CraftCompiler.Architecture.x86_64

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

    def isMSVC2019(self):
        return self.abi.startswith("msvc2019")

    def isMSVC2022(self):
        return self.abi.startswith("msvc2022")

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
            "msvc2017": 15,
            "msvc2019": 16,
            "msvc2022": 17
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
            "msvc2017": 141,
            "msvc2019": 142,
            "msvc2022": 143
        }
        c = self.abi.split("_")[0]
        if c not in versions:
            CraftCore.log.critical(f"Unknown MSVC Compiler {self.abi}")
        return versions[c]

    def androidApiLevel(self):
        return self._apiLevel

if __name__ == '__main__':
    print("Testing Compiler.py")
    print(f"Configured compiler (ABI): {CraftCore.compiler}")
    print("Version: %s" % CraftCore.compiler.getVersionWithName())
    print("Compiler Name: %s" % CraftCore.compiler.getCompilerName())
    print("Native compiler: %s" % ("No", "Yes")[CraftCore.compiler.isNative()])
    if CraftCore.compiler.isGCCLike():
        print("Compiler Version: %s" % CraftCore.compiler.getGCCLikeVersion(CraftCore.compiler.compiler.name))