# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2009 Ralf Habacker <ralf.habacker@freenet.de>
# SPDX-FileCopyrightText: 2020 Nicolas Fella <nicolas.fella@gmx.de>
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

"""@package provides cmake build system"""

import os
import sys
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Utils.Arguments import Arguments
from Utils.PostInstallRoutines import PostInstallRoutines


class CMakeBuildSystem(BuildSystemBase):
    """cmake build support"""

    def __init__(self, package: CraftPackageObject):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self, package, "cmake")
        self.supportsNinja = True

    @staticmethod
    def __cmakeSystem() -> tuple[str, str]:
        """return CMAKE_SYSTEM_NAME and CMAKE_SYSTEM_PROCESSOR for the target"""
        arch = CraftCore.compiler.architecture.key
        platform = CraftCore.compiler.platform
        if platform.isWindows:
            processors = {
                CraftCompiler.Architecture.x86_32: "X86",
                CraftCompiler.Architecture.x86_64: "AMD64",
                CraftCompiler.Architecture.arm64: "ARM64",
            }
            return "Windows", processors[arch]
        if platform.isApple:
            processors = {
                CraftCompiler.Architecture.x86_64: "x86_64",
                CraftCompiler.Architecture.arm64: "arm64",
                CraftCompiler.Architecture.arm64e: "arm64e",
            }
            return "iOS" if platform.isIOS else "Darwin", processors[arch]
        if platform.isFreeBSD:
            return "FreeBSD", arch.autotoolsArchitecture
        return "Linux", arch.autotoolsArchitecture

    def __toolchain(self) -> str:
        """return base toolchain file, chain loading the ECM or Qt toolchain where applicable"""
        useQtToolchain = True
        lines = [
            # Qt's toolchain file chain loads the toolchain qtbase was configured with, which is this one
            "if(__craft_qt_toolchain_loading)",
            "    return()",
            "endif()",
        ]
        python = CraftCore.standardDirs.craftHostRoot() / f"bin/python3{CraftCore.compiler.hostPlatform.executableSuffix}"
        python = (python if python.exists() else Path(sys.executable)).as_posix()
        lines += [f'set({name} "{python}" CACHE FILEPATH "")' for name in ["Python3_EXECUTABLE", "Python_EXECUTABLE", "PYTHON_EXECUTABLE"]]
        if CraftCore.compiler.platform.isAndroid:
            kfVersion = CraftCore.settings.get("General", "KFHostToolingVersion", "5")
            nativeToolingRoot = Path(CraftCore.settings.get("General", f"KF{kfVersion}HostToolingRoot", "/opt/nativetooling"))
            ecmToolchain = CraftCore.standardDirs.craftRoot() / "share/ECM/toolchain/Android.cmake"
            if not ecmToolchain.exists():
                ecmToolchain = nativeToolingRoot / "share/ECM/toolchain/Android.cmake"
            lines += [f'include("{ecmToolchain.as_posix()}")']
            useQtToolchain = kfVersion == "6"
        # CMake ignores CMAKE_SYSTEM_PROCESSOR unless CMAKE_SYSTEM_NAME is set, which also enables CMAKE_CROSSCOMPILING
        elif CraftCore.compiler.isCrossCompiling:
            systemName, processor = self.__cmakeSystem()
            hostRoot = CraftCore.standardDirs.craftHostRoot()
            lines += [
                f'set(CMAKE_SYSTEM_NAME "{systemName}")',
                f'set(CMAKE_SYSTEM_PROCESSOR "{processor}")',
                # programs are searched in the prefix paths before PATH, the host ones must come first.
                # The host prefixes are not below the find root, so the ONLY mode hides them from find_package
                f'list(PREPEND CMAKE_PREFIX_PATH "{(hostRoot / "dev-utils").as_posix()}" "{hostRoot.as_posix()}")',
                f'list(PREPEND CMAKE_FIND_ROOT_PATH "{CraftCore.standardDirs.craftRoot().as_posix()}")',
                "set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)",
                "set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)",
            ]
        if useQtToolchain:
            # the existence check is done by CMake so the file is the same before and after qtbase is installed,
            # qtbase itself must not be built with its own toolchain file, see CRAFT_SKIP_QT_TOOLCHAIN
            qtToolchain = (CraftCore.standardDirs.craftRoot() / "lib/cmake/Qt6/qt.toolchain.cmake").as_posix()
            lines += [
                "list(APPEND CMAKE_TRY_COMPILE_PLATFORM_VARIABLES CRAFT_SKIP_QT_TOOLCHAIN)",
                f'if(NOT CRAFT_SKIP_QT_TOOLCHAIN AND EXISTS "{qtToolchain}")',
                "    set(__craft_qt_toolchain_loading ON)",
                f'    include("{qtToolchain}")',
                "    unset(__craft_qt_toolchain_loading)",
                "endif()",
            ]
        content = "\n".join(lines) + "\n"
        toolchain = CraftCore.standardDirs.etcDir() / "toolchain.cmake"
        # shared by all builds, rewriting it would trigger a reconfigure
        if not toolchain.exists() or toolchain.read_text(encoding="utf-8") != content:
            toolchain.parent.mkdir(parents=True, exist_ok=True)
            toolchain.write_text(content, encoding="utf-8")
        return toolchain.as_posix()

    def __makeFileGenerator(self):
        """return cmake related make file generator"""
        if self.makeProgram == CraftCore.cache.findApplication("ninja"):
            return "Ninja"
        if OsUtils.isWin():
            if CraftCore.compiler.compiler.isMSVC:
                return "NMake Makefiles"
            if CraftCore.compiler.compiler.isMinGW:
                return "MinGW Makefiles"
        elif OsUtils.isUnix():
            return "Unix Makefiles"
        else:
            CraftCore.log.critical(f"unknown {CraftCore.compiler} compiler")

    def configureOptions(self, defines=""):
        """returns default configure options"""
        craftRoot = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        options = Arguments([defines])
        options += [
            f"-DBUILD_TESTING={self.buildTests.asOnOff}",
            f"-DBUILD_SHARED_LIBS={self.subinfo.options.buildStatic.inverted.asOnOff}",
            f"-DCMAKE_INSTALL_PREFIX={craftRoot}",
            f"-DCMAKE_PREFIX_PATH={craftRoot}",
            f"-DCMAKE_REQUIRED_INCLUDES={craftRoot}/include",
            f"-DCMAKE_C_STANDARD_INCLUDE_DIRECTORIES={craftRoot}/include",
            "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
            f"-DCMAKE_TOOLCHAIN_FILE={self.__toolchain()}",
        ]
        if self.package == "libs/qt6/qtbase":
            options.append("-DCRAFT_SKIP_QT_TOOLCHAIN=ON")

        if self.buildType() is not None:
            options.append(f"-DCMAKE_BUILD_TYPE={self.buildType()}")

        # if CraftCore.compiler.isGCC() and not CraftCore.compiler.platform.isNative:
        #    options += " -DCMAKE_TOOLCHAIN_FILE=%s" % os.path.join(CraftStandardDirs.craftRoot(), "craft", "bin", "toolchains", "Toolchain-cross-mingw32-linux-%s.cmake" % CraftCore.compiler.architecture)

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            options.append("-DKDE_L10N_AUTO_TRANSLATIONS=ON")
            options.append("-DKDE_L10N_SYNC_TRANSLATIONS=ON")

        if CraftCore.compiler.platform.isWindows:
            # people use InstallRequiredSystemLibraries.cmake wrong and unconditionally install the
            # msvc crt...
            options += ["-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=ON"]
            if CraftCore.compiler.isCrossCompiling:
                hostRoot = CraftCore.standardDirs.craftHostRoot()
                options += [f"-DKF6_HOST_TOOLING={(hostRoot / 'lib/cmake').as_posix()};{(hostRoot / 'bin').as_posix()}"]
        elif CraftCore.compiler.platform.isMacOS:
            options += [
                f"-DKDE_INSTALL_BUNDLEDIR={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/Applications/KDE",
                "-DAPPLE_SUPPRESS_X11_WARNING=ON",
                f"-DCMAKE_OSX_ARCHITECTURES={CraftCore.compiler.architecture.key.name.lower()}",
                # we want to provide everything ourselves
                "-DCMAKE_IGNORE_PREFIX_PATH=/opt/homebrew/",
            ]
        elif CraftCore.compiler.platform.isLinux:
            # use the same lib dir on all distributions
            options += ["-DCMAKE_INSTALL_LIBDIR:PATH=lib"]
        elif CraftCore.compiler.platform.isAndroid:
            kfVersion = CraftCore.settings.get("General", "KFHostToolingVersion", "5")
            if kfVersion == "5":
                nativeToolingCMake = CraftCore.settings.get(
                    "General",
                    "KF5HostToolingCMakePath",
                    "/opt/nativetooling/lib/x86_64-linux-gnu/cmake/",
                )
                options += [f"-DKF5_HOST_TOOLING={nativeToolingCMake}"]
            elif kfVersion == "6":
                nativeToolingCMake = CraftCore.settings.get(
                    "General",
                    "KF6HostToolingCMakePath",
                    "/opt/nativetooling6/lib/x86_64-linux-gnu/cmake/",
                )
                options += [f"-DKF6_HOST_TOOLING={nativeToolingCMake}"]

            additionalFindRoots = ";".join(
                filter(
                    None,
                    [
                        CraftCore.settings.get("General", "AndroidAdditionalFindRootPath", ""),
                        craftRoot,
                    ],
                )
            )
            options += [
                f"-DECM_ADDITIONAL_FIND_ROOT_PATH='{additionalFindRoots}'",
                f"-DANDROID_APK_OUTPUT_DIR={self.packageDestinationDir()}",
                f"-DANDROID_FASTLANE_METADATA_OUTPUT_DIR={self.packageDestinationDir()}",
                f"-DCMAKE_ANDROID_API={CraftCore.compiler.androidApiLevel()}",
            ]
            # should we detect the apk targets
            if hasattr(self, "androidApkDirs"):
                if self.androidApkTargets:
                    options += [
                        f"-DECM_APK_STAGING_ROOT_PATH='{self.archiveDir()}'",
                        f"-DQTANDROID_EXPORTED_TARGET='{';'.join(self.androidApkTargets)}'",
                        f"-DANDROID_APK_DIR='{';'.join(self.androidApkDirs)}'",
                    ]
                if self.buildType() == "Release" or self.buildType() == "MinSizeRel":
                    options += ["-DANDROIDDEPLOYQT_EXTRA_ARGS=--release"]

        if CraftCore.compiler.platform.isWindows or CraftCore.compiler.platform.isMacOS:
            options.append("-DKDE_INSTALL_USE_QT_SYS_PATHS=ON")

        if self.subinfo.options.dynamic.buildTools:
            options += self.subinfo.options.configure.toolsDefine
        if self.subinfo.options.buildStatic and self.subinfo.options.configure.staticArgs is not None:
            options += self.subinfo.options.configure.staticArgs

        options += [BuildSystemBase.configureOptions(self)]
        options += ["-B", self.buildDir(), "-S", self.configureSourceDir()]
        return options

    def configure(self, defines=""):
        """implements configure step for cmake projects"""

        self.enterBuildDir()
        env = {}
        if self.supportsCCACHE:
            cxx = CraftCore.standardDirs.craftHostRoot() / "dev-utils/ccache/bin" / Path(os.environ["CXX"]).name
            if CraftCore.compiler.platform.isWindows and not cxx.suffix:
                cxx = Path(str(cxx) + CraftCore.compiler.platform.executableSuffix)
            if cxx.exists():
                env["CXX"] = cxx
                env["CC"] = cxx.parent / Path(os.environ["CC"]).name
        with utils.ScopedEnv(env):
            command = Arguments.formatCommand(
                ["cmake", "-G", self.__makeFileGenerator()],
                self.configureOptions(defines),
            )
            return utils.system(command)

    def make(self):
        """implements the make step for cmake projects"""

        self.enterBuildDir()

        command = Arguments.formatCommand([self.makeProgram], self.makeOptions(self.subinfo.options.make.args))
        return utils.system(command)

    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False

        self.enterBuildDir()

        with utils.ScopedEnv({"DESTDIR": self.installDir()}):
            command = Arguments.formatCommand([self.makeProgram], self.makeOptions(self.subinfo.options.install.args))
            return utils.system(command) and self._fixInstallPrefix()

    def unittest(self):
        """running cmake based unittests"""
        self.enterBuildDir()
        with utils.ScopedEnv({"QT_FORCE_STDERR_LOGGING": 1, "QT_ASSUME_STDERR_HAS_CONSOLE": 1}):
            command = [
                "ctest",
                "--output-on-failure",
                "--timeout",
                "300",
                "-j",
                self.subinfo.options.make.parallelMakeJobs,
            ]
            if CraftCore.debug.verbose() == 1:
                command += ["-V"]
            elif CraftCore.debug.verbose() > 1:
                command += ["-VV"]
            return utils.system(command)

    def internalPostQmerge(self):
        if not super().internalPostQmerge():
            return False
        return PostInstallRoutines.updateSharedMimeInfo(self)
