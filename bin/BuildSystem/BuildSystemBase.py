#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

""" \package BuildSystemBase"""
import multiprocessing
import os
import re

from CraftBase import *
from CraftOS.osutils import OsUtils


class BuildSystemBase(CraftBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    debug = True

    def __init__(self, typeName=""):
        """constructor"""
        CraftBase.__init__(self)
        self.supportsNinja = False
        self.supportsCCACHE = CraftCore.settings.getboolean("Compile", "UseCCache", False) and CraftCore.compiler.isMinGW()
        self.supportsClang = True
        self.buildSystemType = typeName

    @property
    def makeProgram(self) -> str:
        if self.subinfo.options.make.supportsMultijob:
            if self.supportsNinja and CraftCore.settings.getboolean("Compile", "UseNinja", False):
                return "ninja"
            if ("Compile", "MakeProgram") in CraftCore.settings:
                CraftCore.log.debug("set custom make program: %s" % CraftCore.settings.get("Compile", "MakeProgram", ""))
                return CraftCore.settings.get("Compile", "MakeProgram", "")
        elif not self.subinfo.options.make.supportsMultijob:
            if "MAKE" in os.environ:
                del os.environ["MAKE"]

        if OsUtils.isWin():
            if CraftCore.compiler.isMSVC() or CraftCore.compiler.isIntel():
                return "nmake"
            elif CraftCore.compiler.isMinGW():
                return "mingw32-make"
            else:
                CraftCore.log.critical(f"unknown {CraftCore.compiler} compiler")
        elif OsUtils.isUnix():
            return "make"

    def compile(self):
        """convencience method - runs configure() and make()"""
        configure = getattr(self, 'configure')
        make = getattr(self, 'make')
        return configure() and make()

    def configureSourceDir(self):
        """returns source dir used for configure step"""
        # pylint: disable=E1101
        # this class never defines self.source, that happens only
        # in MultiSource.
        sourcedir = self.sourceDir()

        if self.subinfo.hasConfigurePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.configurePath())
        return sourcedir

    def configureOptions(self, defines=""):
        """return options for configure command line"""
        if self.subinfo.options.configure.args != None:
            defines += " %s" % self.subinfo.options.configure.args

        if self.supportsCCACHE:
            defines += " %s" % self.ccacheOptions()
        if CraftCore.compiler.isClang() and self.supportsClang:
            defines += " %s" % self.clangOptions()
        return defines

    def makeOptions(self, args):
        """return options for make command line"""
        defines = ""
        if self.subinfo.options.make.ignoreErrors:
            defines += " -i"
        defines += f" {args}"
        if self.makeProgram in {"make", "gmake", "mingw32-make"}:
            if self.subinfo.options.make.supportsMultijob:
                defines += f" -j{multiprocessing.cpu_count()}"
        if CraftCore.debug.verbose() > 0:
            if self.makeProgram == "ninja":
                defines += " -v "
            else:
                defines += " VERBOSE=1 V=1"
        return defines

    def configure(self):
        return True

    def make(self):
        return True

    def install(self) -> bool:
        return self.cleanImage()

    def unittest(self):
        """running unittests"""
        return True

    def ccacheOptions(self):
        return ""

    def clangOptions(self):
        return ""

    def _fixInstallPrefix(self, prefix=CraftStandardDirs.craftRoot()):
        CraftCore.log.debug(f"Begin: fixInstallPrefix {self}: {prefix}")
        def stripPath(path):
            rootPath = os.path.splitdrive(path)[1]
            if rootPath.startswith(os.path.sep) or rootPath.startswith("/"):
                rootPath = rootPath[1:]
            return rootPath
        badPrefix = os.path.join(self.installDir(), stripPath(prefix))

        if os.path.exists(badPrefix) and not os.path.samefile(self.installDir(), badPrefix):
            if not utils.mergeTree(badPrefix, self.installDir()):
                return False

        if CraftCore.settings.getboolean("QtSDK", "Enabled", False):
            qtDir = os.path.join(CraftCore.settings.get("QtSDK", "Path"),
                                 CraftCore.settings.get("QtSDK", "Version"),
                                 CraftCore.settings.get("QtSDK", "Compiler"))
            path = os.path.join(self.installDir(), stripPath(qtDir))
            if os.path.exists(path) and not os.path.samefile(self.installDir(), path):
                if not utils.mergeTree(path, self.installDir()):
                    return False

        if stripPath(prefix):
            oldPrefix = OsUtils.toUnixPath(stripPath(prefix)).split("/", 1)[0]
            utils.rmtree(os.path.join(self.installDir(), oldPrefix))

        CraftCore.log.debug(f"End: fixInstallPrefix {self}")
        return True

    def postInstall(self):
        if not super().postInstall():
            return False
        # a post install routine to fix the prefix (make things relocatable)
        pkgconfigPath = os.path.join(self.imageDir(), "lib", "pkgconfig")
        prefix_re = re.compile("^prefix=(.*)$", re.MULTILINE)
        newPrefix = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        if os.path.exists(pkgconfigPath):
            for pcFile in os.listdir(pkgconfigPath):
                if pcFile.endswith(".pc"):
                    path = os.path.join(pkgconfigPath, pcFile)
                    with open(path, "rt+") as f:
                        config = f.read()
                    prefix = prefix_re.findall(config)
                    if len(prefix) != 1:
                        CraftCore.log.error(f"Failed to patch {path}")
                        return False
                    prefix = prefix[0]
                    CraftCore.log.info(f"Patching {path}, replacing {prefix} with {newPrefix}")
                    config = config.replace(prefix, newPrefix)
                    with open(path, "wt+") as f:
                        f.write(config)
        return True
