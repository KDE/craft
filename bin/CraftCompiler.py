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
import os
import platform
import re
from enum import Enum, IntFlag, auto, unique

from CraftCore import CraftCore


class CraftCompilerSignature(object):
    def __init__(self, platform, compiler, abiString, architecture, sourceString: str = None) -> None:
        self.platform = platform
        self.compiler = compiler
        self.abi = CraftCompiler.Abi.fromString(abiString) if abiString else None
        self.architecture = architecture
        self._sourceString = sourceString

    def __str__(self):
        return "-".join(self.signature)

    def __iter__(self):
        return self.signature.__iter__()

    @property
    def signature(self):
        if self.abi:
            return (
                self.platform.name.lower(),
                self.compiler.name.lower(),
                self.abi.name.lower(),
                self.architecture.name.lower(),
            )
        else:
            return (
                self.platform.name.lower(),
                self.compiler.name.lower(),
                self.architecture.name.lower(),
            )

    @staticmethod
    def parseAbi(s: str):
        split = s.split("-")
        if 3 < len(split) < 4:
            raise Exception(f"Invalid compiler: {s}")

        abi = None
        platform = CraftCompiler.Platforms.fromString(split[0])

        try:
            if len(split) == 4:
                compiler = CraftCompiler.Compiler.fromString(split[1])
                abi = split[2]
                arch = CraftCompiler.Architecture.fromString(split[3])
            else:
                abi = None
                compiler = CraftCompiler.Compiler.fromString(split[1])
                arch = CraftCompiler.Architecture.fromString(split[2])
        except Exception as e:
            # legacy
            try:
                compiler = CraftCompiler.Compiler.fromString(split[2])
                if "_" in split[1]:
                    abi, arch = split[1].split("_", 1)
                else:
                    abi = None
                    arch = split[1]
                if arch == "32":
                    # legacy
                    arch = CraftCompiler.Architecture.x86_32
                elif arch == "64":
                    # legacy
                    arch = CraftCompiler.Architecture.x86_64
                else:
                    arch = CraftCompiler.Architecture.fromString(arch)
                if abi == "mingw":
                    # no need to keep that as it doesn't cary any information
                    abi = None
            except:
                raise Exception(f"Invalid compiler: {s}")
        return CraftCompilerSignature(platform, compiler, abi, arch, sourceString=s)


class CraftCompiler(object):
    class Architecture(IntFlag):
        NoArchitecture = 0
        x86 = 0x1 << 0
        x86_32 = 0x1 << 1 | x86
        x86_64 = 0x1 << 2 | x86
        arm = 0x1 << 3
        arm32 = 0x1 << 4 | arm
        arm64 = 0x1 << 5 | arm
        arm64e = 0x1 << 6 | arm64  # Apple

        All = ~0
        # TODO:...

        @classmethod
        def fromString(cls, name):
            if not hasattr(cls, "__sting_map"):
                cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
            return cls.__sting_map[name.lower()]

    class Platforms(IntFlag):
        NoPlatform = 0
        Windows = 0x1 << 0
        Linux = 0x1 << 1
        MacOS = 0x1 << 2
        FreeBSD = 0x1 << 3
        Android = 0x1 << 4

        Unix = Linux | MacOS | FreeBSD | Android
        All = ~0

        # define inverted values to allow usage in info.ini
        NotLinux = ~Linux
        NotMacOS = ~MacOS
        NotFreeBSD = ~FreeBSD
        NotWindows = ~Windows
        NotUnix = ~Unix
        NotAndroid = ~Android

        @classmethod
        def fromString(cls, name):
            if not hasattr(cls, "__sting_map"):
                cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
            return cls.__sting_map[name.lower()]

    @unique
    class Abi(Enum):
        Error = auto()
        msvc2017 = auto()
        msvc2019 = auto()
        msvc2022 = auto()

        @classmethod
        def fromString(cls, name):
            if not hasattr(cls, "__sting_map"):
                cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
            return cls.__sting_map[name.lower().replace("-", "_")] or cls.Error

    @unique
    class Compiler(IntFlag):
        NoCompiler = 0
        CL = 0x1 << 0
        GCC = 0x1 << 1
        CLANG = 0x1 << 2

        GCCLike = CLANG | GCC
        All = ~0

        @classmethod
        def fromString(cls, name):
            if not hasattr(cls, "__sting_map"):
                cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
            return cls.__sting_map[name.lower()]

    def __init__(self):
        self.signature = CraftCompilerSignature.parseAbi(CraftCore.settings.get("General", "ABI"))
        self._hostArchitecture = None

        self._MSVCToolset = None
        self._apiLevel = None
        if self.isMSVC():
            self._MSVCToolset = CraftCore.settings.get("General", "MSVCToolset", "")
        if self.isAndroid:
            self._apiLevel = CraftCore.settings.get("General", "AndroidAPI", 21)

    def __str__(self):
        return str(self.signature)

    @property
    def platform(self) -> Platforms:
        return self.signature.platform

    @property
    def compiler(self) -> Compiler:
        return self.signature.compiler

    @property
    def architecture(self) -> Architecture:
        return self.signature.architecture

    @property
    def hostArchitecture(self) -> Architecture:
        if not self._hostArchitecture:
            # if we are in a x64 binary on mac the platform class will not report the correct arch
            if self.isMacOS and self.architecture == CraftCompiler.Architecture.x86_64:
                if "RELEASE_ARM64" in platform.uname().version:
                    self._hostArchitecture = CraftCompiler.Architecture.arm64
            if not self._hostArchitecture:
                arch_map = {
                    "i386": CraftCompiler.Architecture.x86_32,
                    "amd64": CraftCompiler.Architecture.x86_64,
                    "x86_64": CraftCompiler.Architecture.x86_64,
                    "arm64": CraftCompiler.Architecture.arm64,
                }
                self._hostArchitecture = arch_map.get(platform.machine().lower())
                if not self._hostArchitecture:
                    print("Unsupported host platform:", platform.machine())
                    exit(1)
        return self._hostArchitecture

    @property
    def rpmArchitecture(self):
        architectures = {
            # values from Fedora, your mileage may vary on other distributions
            CraftCompiler.Architecture.x86_32: "i686",
            CraftCompiler.Architecture.x86_64: "x86_64",
            CraftCompiler.Architecture.arm32: "armhfp",
            CraftCompiler.Architecture.arm64: "arm64",
        }
        return architectures[self.architecture]

    @property
    def debArchitecture(self):
        # https://wiki.debian.org/SupportedArchitectures
        architectures = {
            CraftCompiler.Architecture.x86_32: "i386",
            CraftCompiler.Architecture.x86_64: "amd64",
            CraftCompiler.Architecture.arm32: "armhf",
            CraftCompiler.Architecture.arm64: "arm64",
        }
        return architectures[self.architecture]

    @property
    def appImageArchitecture(self):
        architectures = {
            CraftCompiler.Architecture.x86_32: "i686",
            CraftCompiler.Architecture.x86_64: "x86_64",
            CraftCompiler.Architecture.arm32: "armhf",
            CraftCompiler.Architecture.arm64: "aarch64",
        }
        return architectures[self.architecture]

    @property
    def msvcToolset(self):
        return self._MSVCToolset

    @property
    def bits(self) -> str:
        if self.architecture in {
            CraftCompiler.Architecture.x86_64,
            CraftCompiler.Architecture.arm64,
        }:
            return "64"
        if self.architecture in {
            CraftCompiler.Architecture.x86_32,
            CraftCompiler.Architecture.arm32,
        }:
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

    @property
    def symbolsSuffix(self):
        if self.isMacOS:
            return ".dSYM"
        elif self.isMSVC():
            return ".pdb"
        else:
            return ".debug"

    def isNative(self):
        return self.architecture == self.hostArchitecture and CraftCore.settings.getboolean("General", "Native", True)

    def isGCC(self) -> bool:
        return self.compiler == CraftCompiler.Compiler.GCC

    def isClang(self) -> bool:
        return self.compiler == CraftCompiler.Compiler.CLANG

    def isGCCLike(self) -> bool:
        return bool(self.compiler & CraftCompiler.Compiler.GCCLike)

    def isCl(self) -> bool:
        return self.compiler == CraftCompiler.Compiler.CL

    def isMinGW(self):
        return self.isWindows and self.isGCC()

    def isMinGW_W32(self):
        return self.isMinGW() and self.architecture == CraftCompiler.Architecture.x86_32

    def isMinGW_W64(self):
        return self.isMinGW() and self.architecture == CraftCompiler.Architecture.x86_64

    def isMSVC(self):
        return self.compiler == CraftCompiler.Compiler.CL

    def isMSVC2017(self):
        return self.signature.abi == CraftCompiler.Abi.msvc2017

    def isMSVC2019(self):
        return self.signature.abi == CraftCompiler.Abi.msvc2019

    def isMSVC2022(self):
        return self.signature.abi == CraftCompiler.Abi.msvc2022

    def getGCCLikeVersion(self, compilerExecutable):
        _, result = CraftCore.cache.getCommandOutput(compilerExecutable, "--version")
        if result:
            result = re.findall(r"\d+\.\d+\.?\d*", result)[0]
            CraftCore.log.debug("{0} Version: {1}".format(compilerExecutable, result))
        return result or "0"

    def getVersion(self):
        if self.isGCCLike():
            return self.getGCCLikeVersion(os.environ.get("CXX"))
        elif self.isMSVC():
            return self.getInternalVersion()
        else:
            return None

    def getVersionWithName(self):
        if self.isGCCLike():
            return f"{self.getCompilerName()} {self.getVersion()}"
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
            CraftCompiler.Abi.msvc2017: 15,
            CraftCompiler.Abi.msvc2019: 16,
            CraftCompiler.Abi.msvc2022: 17,
        }
        if self.signature.abi not in versions:
            CraftCore.log.critical(f"Unknown MSVC Compiler {self.signature.abi}")
        return versions[self.signature.abi]

    def getMsvcPlatformToolset(self):
        versions = {
            CraftCompiler.Abi.msvc2017: 141,
            CraftCompiler.Abi.msvc2019: 142,
            CraftCompiler.Abi.msvc2022: 143,
        }
        if self.signature.abi not in versions:
            CraftCore.log.critical(f"Unknown MSVC Compiler {self.signature.abi}")
        return versions[self.signature.abi]

    def androidApiLevel(self):
        return self._apiLevel

    @property
    def androidArchitecture(self):
        architectures = {
            CraftCompiler.Architecture.x86_32: "x86",
            CraftCompiler.Architecture.x86_64: "x86_64",
            CraftCompiler.Architecture.arm32: "arm",
            CraftCompiler.Architecture.arm64: "arm64",
        }
        return architectures[self.architecture]

    @property
    def androidAbi(self):
        architectures = {
            CraftCompiler.Architecture.x86_32: "x86",
            CraftCompiler.Architecture.x86_64: "x86_64",
            CraftCompiler.Architecture.arm32: "armeabi-v7a",
            CraftCompiler.Architecture.arm64: "arm64-v8a",
        }
        return architectures[self.architecture]


if __name__ == "__main__":
    print("Testing Compiler.py")
    print(f"Configured compiler (ABI): {CraftCore.compiler}")
    print("Version: %s" % CraftCore.compiler.getVersionWithName())
    print("Compiler Name: %s" % CraftCore.compiler.getCompilerName())
    print("Architecture: %s" % CraftCore.compiler.architecture)
    print("HostArchitecture: %s" % CraftCore.compiler.hostArchitecture)
    print("Native compiler: %s" % ("No", "Yes")[CraftCore.compiler.isNative()])
    if CraftCore.compiler.isGCCLike():
        print("Compiler Version: %s" % CraftCore.compiler.getGCCLikeVersion(CraftCore.compiler.compiler.name))
