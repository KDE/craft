# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Hannah von Reth <vonreth@kde.org>

"""@package provides boost build system"""
from Blueprints.CraftVersion import CraftVersion
from BuildSystem.BuildSystemBase import *
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs


class BoostBuildSystem(BuildSystemBase):
    """ cmake build support """

    def __init__(self):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self, "boost")
        self.subinfo.options.package.packSources = False

    def craftUserConfig(self):
        craftUserConfigPath = os.path.join(CraftStandardDirs.craftRoot(), "etc", "craft-boost-config.jam")
        if not os.path.exists(craftUserConfigPath):
            config = ""
            if CraftCore.compiler.isMacOS:
                config += "using clang : : /usr/bin/clang++ ;"
            if config:
                with open(craftUserConfigPath, "wt", encoding="UTF-8") as f:
                    f.write(config + "\n")

        if os.path.exists(craftUserConfigPath):
            return f" --user-config={craftUserConfigPath}"
        return ""

    def configureOptions(self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)

        options += [f"-j{multiprocessing.cpu_count()}",
                    f"--build-dir={self.buildDir()}",
                    "--build-type=minimal",
                    #                " --debug-configuration"
                    "threading=multi",
                    f"include=\"{CraftCore.standardDirs.craftRoot()}/include\"",
                    f"library-path=\"{CraftCore.standardDirs.craftRoot()}/lib\""
        ]
        if CraftCore.debug.verbose() >= 1:
            options += ["--dx13"]

        if not self.subinfo.options.buildStatic:
            options += ["link=shared",
                        "runtime-link=shared"]
        else:
            options += ["link=static",
                        "runtime-link=shared"]
        if CraftCore.compiler.isX64():
            options += ["address-model=64", "architecture=x86"]
        else:
            options += ["address-model=32", "architecture=x86"]

        if self.buildType() == "Debug":
            options += ["variant=debug"]
        else:
            options += ["variant=release"]

        toolset = "toolset="
        if CraftCore.compiler.isClang():
            toolset += "clang"
            if CraftCore.compiler.isGCC():
                toolset += " threadapi=pthread"
        elif CraftCore.compiler.isGCC():
            toolset += "gcc"
        elif CraftCore.compiler.isMSVC():
            platform = str(CraftCore.compiler.getMsvcPlatformToolset())
            if CraftVersion(self.buildTarget) < CraftVersion("1_65_1") and CraftCore.compiler.isMSVC2017():
                # pretend to be 2015
                toolset += f"msvc-{platform[:2]}.0"
            elif CraftVersion(self.buildTarget) < CraftVersion("1.70.0") and CraftCore.compiler.isMSVC2019():
                # pretend to be 2017
                toolset += f"msvc-{platform[:2]}.1"
            else:
                toolset += f"msvc-{platform[:2]}.{platform[2:]}"
        options += [toolset]
        options += self.craftUserConfig()
        return options

    def configure(self, defines=""):
        return True

    def make(self):
        """implements the make step for cmake projects"""
        boost = CraftPackageObject.get('libs/boost/boost-headers').instance
        self.subinfo.targetInstSrc[self.subinfo.buildTarget] = os.path.join(boost.sourceDir(), "libs",
                                                                            self.subinfo.targetInstSrc[self.subinfo.buildTarget],
                                                                            "build")

        self.enterSourceDir()
        return utils.system(Arguments.formatCommand(["bjam"], self.configureOptions(self.subinfo.options.configure.args)))



    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False

        reLib = re.compile("(^.*\.lib$|^.*\.a$|^.*\.so.*$)")

        for root, dirs, files in os.walk(self.buildDir()):
            for f in files:
                if f.endswith(".dll"):
                    utils.copyFile(os.path.join(root, f), os.path.join(self.imageDir(), "lib", f))
                    utils.copyFile(os.path.join(root, f), os.path.join(self.imageDir(), "bin", f))
                elif reLib.search(f):
                    utils.copyFile(os.path.join(root, f), os.path.join(self.imageDir(), "lib", f))
                    if CraftCore.compiler.isUnix and not f.endswith(".a"):
                      name, ext = os.path.splitext(f)
                      while not ext == ".so":
                        utils.createSymlink(os.path.join(self.imageDir(), "lib", os.path.basename(f)), os.path.join(self.imageDir(), "lib", name))
                        name, ext = os.path.splitext(name)

        return True



    def unittest(self):
        return True
