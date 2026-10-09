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
import sys
from enum import Enum, IntFlag, auto, unique
from typing import Optional

from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore
from Utils.CraftBool import CraftBool


class CraftCompilerSignature(object):
    def __init__(
        self,
        platform,
        compiler: "CraftCompiler.Compiler" = None,
        abiString: str = None,
        architecture: "CraftCompiler.Architecture" = None,
        host: "CraftCompilerSignature" = None,
        sourceString: Optional[str] = None,
    ) -> None:
        self.platform = platform
        self.compiler = compiler
        self.abi = CraftCompiler.Abi.fromString(abiString) if abiString else CraftCompiler.Abi.Other
        self.architecture = architecture
        self._sourceString = sourceString

        if self.compiler and self.compiler.isGCC and self.platform.isWindows:
            # I'm pretty sure there is a more elegant solution
            self.compiler |= CraftCompiler.Compiler.MinGW

        if not host or self.architecture.key == host.architecture.key:
            self.architecture |= CraftCompiler.Architecture.Native

        if not host or self.platform & host.platform:
            self.platform |= CraftCompiler.Platforms.Native

    def __str__(self):
        return "-".join(self.signature)

    def __iter__(self):
        return self.signature.__iter__()

    @property
    def signature(self):
        sig = [self.platform.key.name.lower()]
        if self.compiler:
            sig += [self.compiler.key.name.lower()]
        if self.abi != CraftCompiler.Abi.Other:
            sig += [self.abi.key.name.lower()]

        sig += [self.architecture.key.name.lower()]
        return tuple(sig)

    @staticmethod
    def parseAbi(s: str, host: "CraftCompilerSignature"):
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
        except Exception:
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
        return CraftCompilerSignature(platform, compiler, abi, arch, host=host, sourceString=s)


class CompilerFilter(object):
    """
    A requirement on CraftCompiler.CompilerFlags, used by the categoryInfo of a blueprint.

    A single flag matches if any of its keys and all of its modifiers are set,
    Linux|Native matches a native Linux, Native matches any native platform.
    Filters and flags can be combined with &, | and ~:
        categoryInfo.platforms &= ~CraftCore.compiler.Platforms.Android
        categoryInfo.platforms &= CraftCore.compiler.Platforms.Native

    The default filter matches everything.
    """

    @staticmethod
    def wrap(value) -> "CompilerFilter":
        if isinstance(value, CompilerFilter):
            return value
        return _FlagFilter(value)

    @staticmethod
    def parse(flagType: type, values: list[str]) -> "CompilerFilter":
        """
        Parse the values of an info.ini, e.g. platforms = Linux;Windows;Native
        - Linux, x86_64: matches if any of them matches
        - Native, bits64: a flag without key, required for every match
        - ~Android, ~Native: does not match if any of the exclusions matches
        """
        include = None
        result = CompilerFilter()
        for v in values:
            if v.startswith("~"):
                result &= ~CompilerFilter.wrap(flagType.fromString(v[1:]))
            else:
                flag = flagType.fromString(v)
                if flag and not flag.key:
                    result &= flag
                else:
                    include = CompilerFilter.wrap(flag) if include is None else include | flag
        if include is not None:
            result = include & result
        return result

    def matches(self, target: "CraftCompiler.CompilerFlags") -> CraftBool:
        return CraftBool(self._match(target))

    def _match(self, target: "CraftCompiler.CompilerFlags") -> bool:
        return True

    def __and__(self, other) -> "CompilerFilter":
        other = CompilerFilter.wrap(other)
        if type(self) is CompilerFilter:
            return other
        if type(other) is CompilerFilter:
            return self
        return _AndFilter(self, other)

    def __rand__(self, other) -> "CompilerFilter":
        return CompilerFilter.wrap(other) & self

    def __or__(self, other) -> "CompilerFilter":
        other = CompilerFilter.wrap(other)
        if type(self) is CompilerFilter or type(other) is CompilerFilter:
            return CompilerFilter()
        return _OrFilter(self, other)

    def __ror__(self, other) -> "CompilerFilter":
        return CompilerFilter.wrap(other) | self

    def __invert__(self) -> "CompilerFilter":
        return _NotFilter(self)

    def __str__(self):
        return "All"

    def __repr__(self):
        return f"CompilerFilter({self})"


class _FlagFilter(CompilerFilter):
    def __init__(self, flag: "CraftCompiler.CompilerFlags"):
        self.flag = flag

    def _match(self, target: "CraftCompiler.CompilerFlags") -> bool:
        # NoPlatform, NoCompiler etc. match nothing
        return bool(self.flag) and target.matchTerm(self.flag)

    def __str__(self):
        return self.flag.name or str(int(self.flag))


class _NotFilter(CompilerFilter):
    def __init__(self, child: CompilerFilter):
        self.child = child

    def _match(self, target: "CraftCompiler.CompilerFlags") -> bool:
        return not self.child._match(target)

    def __invert__(self) -> CompilerFilter:
        return self.child

    def __str__(self):
        return f"~{self.child}"


class _AndFilter(CompilerFilter):
    def __init__(self, left: CompilerFilter, right: CompilerFilter):
        self.left = left
        self.right = right

    def _match(self, target: "CraftCompiler.CompilerFlags") -> bool:
        return self.left._match(target) and self.right._match(target)

    def __str__(self):
        return f"({self.left} & {self.right})"


class _OrFilter(CompilerFilter):
    def __init__(self, left: CompilerFilter, right: CompilerFilter):
        self.left = left
        self.right = right

    def _match(self, target: "CraftCompiler.CompilerFlags") -> bool:
        return self.left._match(target) or self.right._match(target)

    def __str__(self):
        return f"({self.left} | {self.right})"


class CraftCompiler(object):
    CompilerFilter = CompilerFilter

    class CompilerFlags(IntFlag):
        __str__ = Enum.__str__

        @classmethod
        def fromString(cls, name):
            if not hasattr(cls, "__sting_map"):
                cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
            return cls.__sting_map[name.lower()]

        @property
        def key(self):
            """
            Raw value without modifiers, to be used as key in dict's etc
            """
            mask = ~(~0 << 16)
            return self & mask

        @property
        def modifier(self):
            """
            The modifiers, flags that indicate additional conditions like Native
            """
            return self & ~int(self.key)

        def __invert__(self) -> "CompilerFilter":
            """
            ~Platforms.Android: a filter that matches everything but Android
            """
            return ~CompilerFilter.wrap(self)

        def matchTerm(self, term: "CraftCompiler.CompilerFlags") -> bool:
            """
            Match self against a single requirement.
            Any of the keys of term must be set, all of the modifiers of term must be set.
            A term without a key only checks the modifiers.
            """
            if term.key and not (self.key & term.key):
                return False
            return (self.modifier & term.modifier) == term.modifier

    @unique
    class Architecture(CompilerFlags):
        NoArchitecture = 0
        # Values
        x86 = 0x1 << 1
        arm = 0x1 << 2

        # Modifiers, flags that indicate additional conditions

        # Native: Whether the Architecture is cross compiled
        Native = 0x1 << 17

        bits64 = 0x1 << 18
        bits32 = 0x1 << 19

        # actual values
        x86_32 = bits32 | x86
        x86_64 = bits64 | x86
        arm32 = bits32 | arm
        arm64 = bits64 | arm
        arm64e = 0x1 << 4 | arm64  # Apple

        @property
        def isX86(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Architecture.x86)

        @property
        def isX86_32(self) -> CraftBool:
            return CraftBool(self.isX86 and self.is32bit)

        @property
        def isX86_64(self) -> CraftBool:
            return CraftBool(self.isX86 and self.is64bit)

        @property
        def isArm(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Architecture.arm)

        @property
        def isArm32(self) -> CraftBool:
            return CraftBool(self.isArm and self.is32bit)

        @property
        def isArm64(self) -> CraftBool:
            return CraftBool(self.isArm and self.is64bit)

        @property
        def isArm64e(self) -> CraftBool:
            arm64e = CraftCompiler.Architecture.arm64e.key
            return CraftBool(self.key & arm64e == arm64e)

        @property
        def is32bit(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Architecture.bits32)

        @property
        def is64bit(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Architecture.bits64)

        @property
        def bits(self) -> str:
            if self.value & CraftCompiler.Architecture.bits64:
                return "64"
            if self.value & CraftCompiler.Architecture.bits32:
                return "32"
            raise Exception("Unsupported architecture")

        @property
        def isNative(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Architecture.Native)

        @property
        def rpmArchitecture(self):
            architectures = {
                # values from Fedora, your mileage may vary on other distributions
                CraftCompiler.Architecture.x86_32: "i686",
                CraftCompiler.Architecture.x86_64: "x86_64",
                CraftCompiler.Architecture.arm32: "armhfp",
                CraftCompiler.Architecture.arm64: "arm64",
            }
            return architectures[self.key]

        @property
        def debArchitecture(self):
            # https://wiki.debian.org/SupportedArchitectures
            architectures = {
                CraftCompiler.Architecture.x86_32: "i386",
                CraftCompiler.Architecture.x86_64: "amd64",
                CraftCompiler.Architecture.arm32: "armhf",
                CraftCompiler.Architecture.arm64: "arm64",
            }
            return architectures[self.key]

        @property
        def appImageArchitecture(self):
            architectures = {
                CraftCompiler.Architecture.x86_32: "i686",
                CraftCompiler.Architecture.x86_64: "x86_64",
                CraftCompiler.Architecture.arm32: "armhf",
                CraftCompiler.Architecture.arm64: "aarch64",
            }
            return architectures.get(self.key, None)

        @property
        def androidArchitecture(self):
            architectures = {
                CraftCompiler.Architecture.x86_32: "x86",
                CraftCompiler.Architecture.x86_64: "x86_64",
                CraftCompiler.Architecture.arm32: "arm",
                CraftCompiler.Architecture.arm64: "arm64",
            }
            return architectures.get(self.key, None)

        @property
        def androidAbi(self):
            architectures = {
                CraftCompiler.Architecture.x86_32: "x86",
                CraftCompiler.Architecture.x86_64: "x86_64",
                CraftCompiler.Architecture.arm32: "armeabi-v7a",
                CraftCompiler.Architecture.arm64: "arm64-v8a",
            }
            return architectures.get(self.key, None)

    @unique
    class Platforms(CompilerFlags):
        NoPlatform = 0

        Windows = 0x1 << 0
        Linux = 0x1 << 1
        MacOS = 0x1 << 2
        FreeBSD = 0x1 << 3
        Android = 0x1 << 4
        iOS = 0x1 << 5

        Mobile = Android | iOS
        Unix = Linux | MacOS | FreeBSD | Android
        Apple = MacOS | iOS

        # Modifiers, flags that indicate additional conditions

        # Native: Whether the Platform is cross compiled
        Native = 0x1 << 17

        @property
        def isWindows(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.Windows)

        @property
        def isMacOS(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.MacOS)

        @property
        def isIOS(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.iOS)

        @property
        def isLinux(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.Linux)

        @property
        def isFreeBSD(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.FreeBSD)

        @property
        def isAndroid(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.Android)

        @property
        def isUnix(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.Unix)

        @property
        def isApple(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.Apple)

        @property
        def isMobile(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.Mobile)

        @property
        def isNative(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Platforms.Native)

        @property
        def executableSuffix(self):
            return ".exe" if self.isWindows else ""

    @unique
    class Abi(CompilerFlags):
        Other = auto()
        msvc2019 = auto()
        msvc2022 = auto()
        msvc2026 = auto()

        @property
        def isMSVC2019(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Abi.msvc2019)

        @property
        def isMSVC2022(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Abi.msvc2022)

        @property
        def isMSVC2026(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Abi.msvc2026)

    @unique
    class Compiler(CompilerFlags):
        NoCompiler = 0

        CL = 0x1 << 0
        GCC = 0x1 << 1
        CLANG = 0x1 << 2

        GCCLike = CLANG | GCC
        # Modifiers, flags that indicate additional conditions

        # Native: Whether the Compiler is cross compiling
        Native = 0x1 << 17
        MinGW = 0x1 << 18

        @property
        def isGCC(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Compiler.GCC)

        @property
        def isClang(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Compiler.CLANG)

        @property
        def isGCCLike(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Compiler.GCCLike)

        @property
        def isCl(self) -> CraftBool:
            return CraftBool(self.value & CraftCompiler.Compiler.CL)

        @property
        def isMinGW(self):
            return CraftBool(self.value & CraftCompiler.Compiler.MinGW)

        @property
        def isMSVC(self):
            return CraftBool(self.value & CraftCompiler.Compiler.CL)

    # EnumType replaces __invert__ of every Flag class with Flag.__invert__, restore ours
    for _flags in (Architecture, Platforms, Abi, Compiler):
        _flags.__invert__ = CompilerFlags.__invert__
    del _flags

    def __init__(self):
        self.hostSignature = self._detectHost()
        self.signature = CraftCompilerSignature.parseAbi(CraftCore.settings.get("General", "ABI"), self.hostSignature)

        self._MSVCToolset = None
        self._apiLevel = None
        if self.compiler.isMSVC:
            self._MSVCToolset = CraftCore.settings.get("General", "MSVCToolset", "")
        if self.platform.isAndroid:
            self._apiLevel = CraftCore.settings.get("General", "AndroidAPI", 28)

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
    def abi(self) -> Abi:
        return self.signature.abi

    @staticmethod
    def _detectHost() -> CraftCompilerSignature:
        hostPlatform = {
            "windows": CraftCompiler.Platforms.Windows,
            "linux": CraftCompiler.Platforms.Linux,
            "darwin": CraftCompiler.Platforms.MacOS,
        }.get(platform.system().lower())

        # if we are in a x64 binary on mac the platform class will not report the correct arch
        if hostPlatform == CraftCompiler.Platforms.MacOS and "RELEASE_ARM64" in platform.uname().version:
            hostArchitecture = CraftCompiler.Architecture.arm64
        else:
            hostArchitecture = {
                "i386": CraftCompiler.Architecture.x86_32,
                "amd64": CraftCompiler.Architecture.x86_64,
                "x86_64": CraftCompiler.Architecture.x86_64,
                "arm64": CraftCompiler.Architecture.arm64,
            }.get(platform.machine().lower())
        if not hostArchitecture or not hostPlatform:
            print(f"Unsupported host platform: {platform.system()} {platform.machine()}", file=sys.stderr)
            exit(1)
        return CraftCompilerSignature(hostPlatform | CraftCompiler.Platforms.Native, architecture=hostArchitecture | CraftCompiler.Architecture.Native)

    @property
    def hostPlatform(self) -> Platforms:
        return self.hostSignature.platform

    @property
    def hostArchitecture(self) -> Architecture:
        return self.hostSignature.architecture

    @property
    def msvcToolset(self):
        return self._MSVCToolset

    @property
    def symbolsSuffix(self):
        if self.platform.isApple:
            return ".dSYM"
        elif self.compiler.isMSVC:
            return ".pdb"
        else:
            return ".debug"

    def getGCCLikeVersion(self, compilerExecutable):
        _, result = CraftCore.cache.getCommandOutput(compilerExecutable, "--version")
        if result:
            result = re.findall(r"\d+\.\d+\.?\d*", result)[0]
            CraftCore.log.debug("{0} Version: {1}".format(compilerExecutable, result))
        return result or "0"

    def getVersion(self):
        if self.compiler.isGCCLike:
            return self.getGCCLikeVersion(os.environ.get("CXX"))
        elif self.compiler.isMSVC:
            return self.getInternalVersion()
        else:
            return None

    def getInternalVersion(self):
        if not self.compiler.isMSVC:
            return self.getVersion()
        versions = {
            CraftCompiler.Abi.msvc2019: 16,
            CraftCompiler.Abi.msvc2022: 17,
            CraftCompiler.Abi.msvc2026: 18,
        }
        if self.signature.abi not in versions:
            CraftCore.log.critical(f"Unknown MSVC Compiler {self.signature.abi}")
        return versions[self.signature.abi.key]

    def getMsvcPlatformToolset(self):
        versions = {
            CraftCompiler.Abi.msvc2019: 142,
            CraftCompiler.Abi.msvc2022: 143,
            # Microsoft skipped v144, see https://stackoverflow.com/a/72951716
            CraftCompiler.Abi.msvc2026: 145,
        }
        if self.signature.abi not in versions:
            CraftCore.log.critical(f"Unknown MSVC Compiler {self.signature.abi}")
        return versions[self.signature.abi.key]

    def getMsvcYear(self):
        years = {
            CraftCompiler.Abi.msvc2019: 2019,
            CraftCompiler.Abi.msvc2022: 2022,
            CraftCompiler.Abi.msvc2026: 2026,
        }
        if self.signature.abi not in years:
            CraftCore.log.critical(f"Unknown MSVC Compiler {self.signature.abi}")
        return years[self.signature.abi]

    def androidApiLevel(self):
        return self._apiLevel

    @property
    def macOSDeploymentTarget(self) -> CraftVersion:
        return CraftVersion(CraftCore.settings.get("General", "MacDeploymentTarget", "13.3"))


if __name__ == "__main__":
    print("Testing Compiler.py")
    print(f"Configured compiler (ABI): {CraftCore.compiler}")
    print("Architecture: %s" % CraftCore.compiler.signature)
    print("HostArchitecture: %s" % CraftCore.compiler.hostSignature)
    print(f"Native compiler: {CraftCore.compiler.platform.isNative.asYesNo}")
    if CraftCore.compiler.compiler.isGCCLike:
        print("Compiler Version: %s" % CraftCore.compiler.getGCCLikeVersion(CraftCore.compiler.compiler.name))
