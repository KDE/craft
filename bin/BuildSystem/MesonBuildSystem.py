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

import multiprocessing
import os
import textwrap

import utils
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Utils.Arguments import Arguments


class MesonBuildSystem(BuildSystemBase):
    def __init__(self, **kwargs):
        BuildSystemBase.__init__(self, **kwargs, typeName="meson")

    @property
    def __meson(self):
        return CraftCore.cache.findApplication("meson")

    def __env(self):
        env = {
            "LDFLAGS": self.subinfo.options.configure.ldflags + " " + os.environ.get("LDFLAGS", ""),
            "CFLAGS": self.subinfo.options.configure.cflags + " " + os.environ.get("CFLAGS", ""),
            "CXXFLAGS": self.subinfo.options.configure.cxxflags + " " + os.environ.get("CXXFLAGS", ""),
        }
        if CraftCore.settings.getboolean("General", "AllowAnsiColor", True):
            env["FORCE_COLOR"] = 1
        if CraftCore.compiler.compiler.isMSVC:
            env.update(
                {
                    "LIB": f"{os.environ['LIB']};{CraftStandardDirs.craftRoot() / 'lib'}",
                    "INCLUDE": f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot() / 'include'}",
                }
            )
        else:
            env["LDFLAGS"] = f"-L{CraftStandardDirs.craftRoot() / 'lib'} {env['LDFLAGS']}"
            env["CFLAGS"] = f"-I{CraftStandardDirs.craftRoot() / 'include'} {env['CFLAGS']}"
            env["CXXFLAGS"] = f"-I{CraftStandardDirs.craftRoot() / 'include'} {env['CXXFLAGS']}"
        return env

    def configureOptions(self, defines=""):
        buildType = {
            "Release": "release",
            "RelWithDebInfo": "debugoptimized",
            "MinSizeRel": "minsize",
            "Debug": "debug",
        }.get(self.buildType())
        return Arguments(
            [
                defines,
                "--prefix",
                CraftCore.standardDirs.craftRoot(),
                "--libdir",
                "lib",
                "--datadir",
                CraftCore.standardDirs.locations.data,
                "--buildtype",
                buildType,
                "--cmake-prefix-path",
                CraftCore.standardDirs.craftRoot(),
                self.buildDir(),
                self.sourceDir(),
                f"-Ddefault_library={'static' if self.subinfo.options.buildStatic else 'shared'}",
                BuildSystemBase.configureOptions(self),
            ]
        )

    def craftCrossFile(self):
        craftCrossFilePath = CraftStandardDirs.craftRoot() / "etc/craft-cross-file.txt"
        args = []
        config = ""

        if CraftCore.compiler.platform.isAndroid:
            if CraftCore.compiler.architecture.isArm64:
                toolchain = "aarch64-linux-android"
                compiler = "aarch64-linux-android"
            elif CraftCore.compiler.architecture.isArm32:
                toolchain = "arm-linux-androideabi"
                compiler = "armv7a-linux-androideabi"
            elif CraftCore.compiler.architecture.isX86_32:
                toolchain = "i686-linux-android"
                compiler = "i686-linux-android"
            else:
                toolchain = f"{CraftCore.compiler.architecture.androidArchitecture}-linux-android"
                compiler = f"{CraftCore.compiler.architecture.androidArchitecture}-linux-android"

            toolchain_path = os.path.join(os.environ["ANDROID_NDK"], "toolchains/llvm/prebuilt", os.environ.get("ANDROID_NDK_HOST", "linux-x86_64"), "bin")

            config = (
                "[constants]\n"
                f"android_ndk = '{toolchain_path}/'\n"
                f"toolchain = '{toolchain}'\n"
                f"compiler = '{compiler}'\n"
                f"abiversion = '{CraftCore.compiler.androidApiLevel()}'\n"
                "[binaries]\n"
                "c = android_ndk + compiler + abiversion + '-clang'\n"
                "cpp = android_ndk + compiler + abiversion + '-clang++'\n"
                "ar = android_ndk + 'llvm-ar'\n"
                "ld = android_ndk + 'lld'\n"
                "objcopy = android_ndk + 'llvm-objcopy'\n"
                "strip = android_ndk + 'llvm-strip'\n"
                "pkgconfig = '/usr/bin/pkg-config'\n"
                "[host_machine]\n"
                "system = 'linux'\n"
                f"cpu_family = '{CraftCore.compiler.architecture.androidArchitecture}'\n"
                f"cpu = '{CraftCore.compiler.architecture.androidArchitecture}'\n"  # according to meson, this value is meaningless (https://github.com/mesonbuild/meson/issues/7037#issuecomment-620137436)
                "endian = 'little'\n"
            )
            args = ["--cross-file", craftCrossFilePath]
        elif CraftCore.compiler.platform.isMacOS and not CraftCore.compiler.architecture.isNative:
            # based on https://github.com/mesonbuild/meson-python/blob/main/mesonpy/__init__.py#L687
            arch = CraftCore.compiler.architecture.name.lower()
            config = textwrap.dedent(
                f"""
                        [binaries]
                        c = ['cc', '-arch', {arch!r}]
                        cpp = ['c++', '-arch', {arch!r}]
                        objc = ['cc', '-arch', {arch!r}]
                        objcpp = ['c++', '-arch', {arch!r}]
                    """
            )
            args = ["--native-file", craftCrossFilePath]
        if config:
            with craftCrossFilePath.open("wt", encoding="UTF-8") as f:
                f.write(config)

        return args

    def configure(self, defines=""):
        with utils.ScopedEnv(self.__env()):
            extra_options = self.craftCrossFile()
            if not utils.system(Arguments([self.__meson, "setup", extra_options, self.configureOptions(defines)])):
                logFile = self.buildDir() / "meson-logs/meson-log.txt"
                if logFile.exists():
                    with logFile.open("rt", encoding="UTF-8") as log:
                        CraftCore.log.info(logFile)
                        CraftCore.debug.debug_line()
                        CraftCore.log.info(log.read())
                        CraftCore.debug.debug_line()
                return False
            return True

    def make(self):
        with utils.ScopedEnv(self.__env()):
            # cwd should not be the build dir as it might confuse the dependencie resolution
            return utils.system(
                Arguments(
                    [
                        self.__meson,
                        "compile",
                        "-C",
                        self.buildDir(),
                        self.makeOptions(self.subinfo.options.make.args),
                    ]
                ),
                cwd=CraftCore.standardDirs.craftRoot(),
            )

    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False
        env = self.__env()
        env["DESTDIR"] = self.installDir()
        with utils.ScopedEnv(env):
            return utils.system([self.__meson, "install"], cwd=self.buildDir()) and self._fixInstallPrefix()

    def unittest(self):
        """running make tests"""
        return utils.system([self.__meson, "test"], cwd=self.buildDir())

    def makeOptions(self, args):
        defines = Arguments()
        if CraftCore.debug.verbose() > 0:
            defines.append("-v")
        if self.subinfo.options.make.supportsMultijob:
            if ("Compile", "Jobs") in CraftCore.settings:
                defines += [
                    "-j",
                    str(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count())),
                ]
        if args:
            defines.append(args)
        return defines
