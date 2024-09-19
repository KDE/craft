# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2009 Ralf Habacker <ralf.habacker@freenet.de>
# SPDX-FileCopyrightText: 2020 Nicolas Fella <nicolas.fella@gmx.de>
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

"""@package provides cmake build system"""

import multiprocessing
import os
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from BuildSystem.BuildSystemBase import BuildSystemBase
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

    def __makeFileGenerator(self):
        """return cmake related make file generator"""
        if self.makeProgram == "ninja":
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
            "-DBUILD_TESTING={testing}".format(testing="ON" if self.buildTests else "OFF"),
            "-DBUILD_SHARED_LIBS={shared}".format(shared="OFF" if self.subinfo.options.buildStatic else "ON"),
            f"-DCMAKE_INSTALL_PREFIX={craftRoot}",
            f"-DCMAKE_PREFIX_PATH={craftRoot}",
            f"-DCMAKE_REQUIRED_INCLUDES={craftRoot}/include",
            f"-DCMAKE_C_STANDARD_INCLUDE_DIRECTORIES={craftRoot}/include",
            "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
        ]
        if not CraftCore.compiler.platform.isNative:
            options += [f"-DCMAKE_FIND_ROOT_PATH={CraftCore.standardDirs.craftRoot()}"]

        if self.buildType() is not None:
            options.append(f"-DCMAKE_BUILD_TYPE={self.buildType()}")

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            options.append("-DKDE_L10N_AUTO_TRANSLATIONS=ON")
            options.append("-DKDE_L10N_SYNC_TRANSLATIONS=ON")

        if CraftCore.compiler.platform.isWindows:
            # people use InstallRequiredSystemLibraries.cmake wrong and unconditionally install the
            # msvc crt...
            options.append("-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=ON")
        elif CraftCore.compiler.platform.isMacOS:
            options += [
                f"-DKDE_INSTALL_BUNDLEDIR={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/Applications/KDE",
                "-DAPPLE_SUPPRESS_X11_WARNING=ON",
                f"-DCMAKE_OSX_ARCHITECTURES={CraftCore.compiler.architecture.name.lower()}",
            ]
        elif CraftCore.compiler.platform.isIOS:
            toolChain = CraftCore.standardDirs.craftRoot() / "lib/cmake/Qt6/qt.toolchain.cmake"
            if toolChain.exists():
                options += [f"-DCMAKE_TOOLCHAIN_FILE={toolChain}"]
            options += [
                "-DCMAKE_OSX_SYSROOT=iphonesimulator",
                "-DCMAKE_OSX_DEPLOYMENT_TARGET=17.5",
            ]
        elif CraftCore.compiler.platform.isLinux:
            # use the same lib dir on all distributions
            options += ["-DCMAKE_INSTALL_LIBDIR:PATH=lib"]
        elif CraftCore.compiler.platform.isAndroid:
            kfVersion = CraftCore.settings.get("General", "KFHostToolingVersion", "5")
            nativeToolingRoot = CraftCore.settings.get("General", f"KF{kfVersion}HostToolingRoot", "/opt/nativetooling")

            # prefer the toolchain file ECM installed, fall back to the one in the host tools
            ecmToolchain = os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "share/ECM/toolchain/Android.cmake")
            if not os.path.exists(ecmToolchain):
                ecmToolchain = os.path.join(nativeToolingRoot, "share/ECM/toolchain/Android.cmake")

            if kfVersion == "5":
                nativeToolingCMake = CraftCore.settings.get(
                    "General",
                    "KF5HostToolingCMakePath",
                    "/opt/nativetooling/lib/x86_64-linux-gnu/cmake/",
                )
                options += [
                    f"-DCMAKE_TOOLCHAIN_FILE={ecmToolchain}",
                    f"-DKF5_HOST_TOOLING={nativeToolingCMake}",
                ]
            elif kfVersion == "6":
                nativeToolingCMake = CraftCore.settings.get(
                    "General",
                    "KF6HostToolingCMakePath",
                    "/opt/nativetooling6/lib/x86_64-linux-gnu/cmake/",
                )
                qtToolchainPath = os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "lib/cmake/Qt6/qt.toolchain.cmake")
                if os.path.exists(qtToolchainPath):
                    options += [
                        f"-DCMAKE_TOOLCHAIN_FILE={qtToolchainPath}",
                        f"-DQT_CHAINLOAD_TOOLCHAIN_FILE={ecmToolchain}",
                        f"-DKF6_HOST_TOOLING={nativeToolingCMake}",
                    ]
                else:
                    # the ECM toolchain file still works standalone, if we don't have Qt's own toolchain file yet
                    options += [
                        f"-DCMAKE_TOOLCHAIN_FILE={ecmToolchain}",
                        f"-DKF6_HOST_TOOLING={nativeToolingCMake}",
                    ]

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
        options += ["-S", self.configureSourceDir()]
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
                str(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count())),
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
