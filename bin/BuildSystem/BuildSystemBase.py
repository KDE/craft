#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

""" \package BuildSystemBase"""
import multiprocessing
import os

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
    def makeProgram(self):
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
                return "nmake /NOLOGO"
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

    def makeOptions(self, defines=""):
        """return options for make command line"""
        if self.subinfo.options.make.ignoreErrors:
            defines += " -i"
        if self.subinfo.options.make.makeOptions:
            defines += f" {self.subinfo.options.make.makeOptions}"
        if self.makeProgram in ["make", "gmake", "mingw32-make"]:
            defines += f" -j{ multiprocessing.cpu_count()}"
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

    def install(self):

        # create post (un)install scripts
        if OsUtils.isWin():
            scriptExt = ".cmd"
        elif OsUtils.isUnix():
            scriptExt = ".sh"
        for pkgtype in ['bin', 'lib', 'doc', 'src', 'dbg']:
            script = os.path.join(self.packageDir(), "post-install-%s.%s") % (pkgtype, scriptExt)
            scriptName = "post-install-%s-%s.%s" % (self.package, pkgtype, scriptExt)
            # are there any cases there installDir should be honored ?
            destscript = os.path.join(self.imageDir(), "manifest", scriptName)
            if not os.path.exists(os.path.join(self.imageDir(), "manifest")):
                utils.createDir(os.path.join(self.imageDir(), "manifest"))
            if os.path.exists(script):
                utils.copyFile(script, destscript)
            script = os.path.join(self.packageDir(), "post-uninstall-%s.%s") % (pkgtype, scriptExt)
            scriptName = "post-uninstall-%s-%s.%s" % (self.package, pkgtype, scriptExt)
            # are there any cases there installDir should be honored ?
            destscript = os.path.join(self.imageDir(), "manifest", scriptName)
            if not os.path.exists(os.path.join(self.imageDir(), "manifest")):
                utils.createDir(os.path.join(self.imageDir(), "manifest"))
            if os.path.exists(script):
                utils.copyFile(script, destscript)
        return True

    def unittest(self):
        """running unittests"""
        return True

    def ccacheOptions(self):
        return ""

    def clangOptions(self):
        return ""

    def _fixInstallPrefix(self):
        CraftCore.log.debug(f"Begin: fixInstallPrefix {self}")
        def stripPath(path):
            rootPath = os.path.splitdrive(path)[1]
            if rootPath.startswith(os.path.sep):
                rootPath = rootPath[1:]
            return rootPath
        badPrefix = os.path.join(self.installDir(), stripPath(CraftStandardDirs.craftRoot()))

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

        CraftCore.log.debug(f"End: fixInstallPrefix {self}")
        return True
