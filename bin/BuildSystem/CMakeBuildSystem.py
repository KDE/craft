# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2009 Ralf Habacker <ralf.habacker@freenet.de>
# SPDX-FileCopyrightText: 2020 Nicolas Fella <nicolas.fella@gmx.de>
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

"""@package provides cmake build system"""

from BuildSystem.BuildSystemBase import *
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs
from Utils.PostInstallRoutines import *
from Utils.Arguments import Arguments

import os


class CMakeBuildSystem(BuildSystemBase):
    """ cmake build support """

    def __init__(self):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self, "cmake")
        self.supportsNinja = True
        self.androidApkTargets = set()
        self.androidApkDirs = set()

    def __makeFileGenerator(self):
        """return cmake related make file generator"""
        if self.makeProgram == "ninja":
            return "Ninja"
        if OsUtils.isWin():
            if CraftCore.compiler.isMSVC() and not CraftCore.compiler.isIntel():
                return "NMake Makefiles"
            if CraftCore.compiler.isMinGW():
                return "MinGW Makefiles"
        elif OsUtils.isUnix():
            return "Unix Makefiles"
        else:
            CraftCore.log.critical(f"unknown {CraftCore.compiler} compiler")

    def __autodetectAndroidApkTargets(self):
        """Android APK parameter auto-detection,
           see https://invent.kde.org/sysadmin/ci-tooling/-/blob/master/system-images/android/sdk/get-apk-args.py"""
        if not CraftCore.compiler.isAndroid or self.androidApkTargets == None or len(self.androidApkTargets) > 0:
            return

        import glob
        from xml.etree import ElementTree
        files = glob.iglob(f"{self.sourceDir()}/**/AndroidManifest.xml*", recursive=True)
        for file in files:
            if "3rdparty" in file or "examples" in file or "tests" in file:
                continue
            tree = ElementTree.parse(file)
            prefix = '{http://schemas.android.com/apk/res/android}'
            for md in tree.findall("application/activity/meta-data"):
                if md.attrib[prefix + 'name'] == 'android.app.lib_name':
                    targetName = md.attrib[prefix + 'value']
                    if not targetName in self.androidApkTargets:
                        self.androidApkTargets.add(targetName)
                        self.androidApkDirs.add(os.path.dirname(file))

    def configureOptions(self, defines=""):
        """returns default configure options"""
        craftRoot = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        options = Arguments([defines])
        options += [
                    "-DBUILD_TESTING={testing}".format(testing="ON" if self.buildTests else "OFF"),
                    "-DBUILD_SHARED_LIBS={shared}".format(shared="OFF" if self.subinfo.options.buildStatic else "ON"),
                    BuildSystemBase.configureOptions(self),
                    f"-DCMAKE_INSTALL_PREFIX={craftRoot}",
                    f"-DCMAKE_PREFIX_PATH={craftRoot}"
                ]

        if self.buildType() is not None:
            options.append(f"-DCMAKE_BUILD_TYPE={self.buildType()}")

        #if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative():
        #    options += " -DCMAKE_TOOLCHAIN_FILE=%s" % os.path.join(CraftStandardDirs.craftRoot(), "craft", "bin", "toolchains", "Toolchain-cross-mingw32-linux-%s.cmake" % CraftCore.compiler.architecture)

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            options.append("-DKDE_L10N_AUTO_TRANSLATIONS=ON")

        if CraftCore.compiler.isWindows:
            # people use InstallRequiredSystemLibraries.cmake wrong and unconditionally install the
            # msvc crt...
            options.append("-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=ON")
        elif CraftCore.compiler.isMacOS:
            options += [f"-DKDE_INSTALL_BUNDLEDIR={OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())}/Applications/KDE", "-DAPPLE_SUPPRESS_X11_WARNING=ON"]
        elif CraftCore.compiler.isLinux:
            # use the same lib dir on all distributions
            options += ["-DCMAKE_INSTALL_LIBDIR=lib"]
        elif CraftCore.compiler.isAndroid:
            nativeToolingRoot = CraftCore.settings.get("General", "KF5HostToolingRoot", "/opt/nativetooling")
            nativeToolingCMake = CraftCore.settings.get("General", "KF5HostToolingCMakePath", "/opt/nativetooling/lib/x86_64-linux-gnu/cmake/")
            additionalFindRoots = ";".join(filter(None, [CraftCore.settings.get("General", "AndroidAdditionalFindRootPath", ""), craftRoot]))
            options += [f"-DCMAKE_TOOLCHAIN_FILE={nativeToolingRoot}/share/ECM/toolchain/Android.cmake",
                        f"-DECM_ADDITIONAL_FIND_ROOT_PATH='{additionalFindRoots}'",
                        f"-DKF5_HOST_TOOLING={nativeToolingCMake}",
                        f"-DANDROID_APK_OUTPUT_DIR={self.packageDestinationDir()}",
                        f"-DANDROID_FASTLANE_METADATA_OUTPUT_DIR={self.packageDestinationDir()}"]
            self.__autodetectAndroidApkTargets()
            if self.androidApkTargets != None and len(self.androidApkTargets) > 0:
                options += [f"-DQTANDROID_EXPORTED_TARGET={';'.join(self.androidApkTargets)}",
                            f"-DANDROID_APK_DIR={';'.join(self.androidApkDirs)}"]
            if self.buildType() == "Release" or self.buildType() == "MinSizeRel":
                options += ["-DANDROIDDEPLOYQT_EXTRA_ARGS=--release"]

        if CraftCore.compiler.isWindows or CraftCore.compiler.isMacOS:
            options.append("-DKDE_INSTALL_USE_QT_SYS_PATHS=ON")

        if self.subinfo.options.buildTools:
            options += self.subinfo.options.configure.toolsDefine
        if self.subinfo.options.buildStatic and self.subinfo.options.configure.staticArgs:
            options += self.subinfo.options.configure.staticArgs
        if CraftCore.compiler.isIntel():
            # this is needed because otherwise it'll detect the MSVC environment
            options += " -DCMAKE_CXX_COMPILER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                      "icl.exe").replace("\\", "/")
            options += " -DCMAKE_C_COMPILER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                    "icl.exe").replace("\\", "/")
            options += " -DCMAKE_LINKER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"),
                                                                "xilink.exe").replace("\\", "/")
        options += ["-S", self.configureSourceDir()]
        return options

    def configure(self, defines=""):
        """implements configure step for cmake projects"""

        self.enterBuildDir()
        env = {}
        if self.supportsCCACHE and CraftCore.cache.findApplication("ccache"):
            env["CXX"] = CraftCore.standardDirs.craftRoot()/ "dev-utils/ccache/bin" / Path(os.environ["CXX"]).name
            env["CC"] = CraftCore.standardDirs.craftRoot()/ "dev-utils/ccache/bin" / Path(os.environ["CC"]).name
        with utils.ScopedEnv(env):
            command = Arguments.formatCommand(["cmake", "-G",  self.__makeFileGenerator()], self.configureOptions(defines))
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


        with utils.ScopedEnv({"DESTDIR" : self.installDir()}):
            command = Arguments.formatCommand([self.makeProgram], self.makeOptions(self.subinfo.options.install.args))
            return (utils.system(" ".join(command)) and
                    self._fixInstallPrefix())

    def unittest(self):
        """running cmake based unittests"""

        self.enterBuildDir()

        command = ["ctest", "--output-on-failure", "--timeout", "300", "-j", str(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count()))]
        if CraftCore.debug.verbose() == 1:
            command += ["-V"]
        elif CraftCore.debug.verbose() > 1:
            command += ["-VV"]
        return utils.system(command)

    def internalPostQmerge(self):
        if not super().internalPostQmerge():
            return False
        return PostInstallRoutines.updateSharedMimeInfo(self)

    def createPackage(self):
        self.__autodetectAndroidApkTargets()
        if CraftCore.compiler.isAndroid and self.androidApkTargets != None and len(self.androidApkTargets) > 0:
            self.enterBuildDir()
            command = Arguments.formatCommand([self.makeProgram], ["create-apk"])
            return utils.system(command)
