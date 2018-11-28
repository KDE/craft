#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

""" \package BuildSystemBase"""
import glob
import io
import multiprocessing
import os
import re
import subprocess

from CraftBase import *
from CraftOS.osutils import OsUtils


class BuildSystemBase(CraftBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    debug = True

    def __init__(self, typeName=""):
        """constructor"""
        CraftBase.__init__(self)
        self.supportsNinja = False
        self.supportsCCACHE = CraftCore.settings.getboolean("Compile", "UseCCache", False) and CraftCore.compiler.isGCCLike()
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
        defines = []
        if self.subinfo.options.make.ignoreErrors:
            defines.append("-i")
        if self.makeProgram == "ninja":
            if CraftCore.debug.verbose() > 0:
                defines.append("-v")
        else:
            if self.subinfo.options.make.supportsMultijob:
                defines.append(f"-j{multiprocessing.cpu_count()}")
            if CraftCore.debug.verbose() > 0:
                defines += ["VERBOSE=1", "V=1"]
        if args:
            defines.append(args)
        return " ".join(defines)

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



    # TODO: port oldPath to regexp to match path with \ and /
    def patchInstallPrefix(self, files : [str], oldPaths : [str]=None, newPath : str=CraftCore.standardDirs.craftRoot()) -> bool:
        if isinstance(oldPaths, str):
            oldPaths = [oldPaths]
        elif not oldPaths:
            oldPaths = [self.subinfo.buildPrefix]
        newPathWin = OsUtils.toNativePath(newPath)
        newPathUnix = OsUtils.toUnixPath(newPath)
        newPath = newPathUnix
        for fileName in files:
            if not os.path.exists(fileName):
                CraftCore.log.warning(f"File {fileName} not found.")
                return False
            with open(fileName, "rb") as f:
                content = f.read()
            dirty = False
            for oldPath in oldPaths:
                assert os.path.isabs(oldPath)
                if CraftCore.compiler.isWindows:
                    _, ext = os.path.splitext(fileName)
                    # keep unix path sep or use unix path sep for specific type
                    # prl and pri files might use \\\\ as sep which can be replaced by a / but not by a single \\
                    if oldPath[2] == "/" or ext in {".prl", ".pri"}:
                        newPath = newPathUnix
                    else:
                        # keep windows sep
                        newPath = newPathWin

                oldPathBinary = oldPath.encode()
                if oldPath != newPath and oldPathBinary in content:
                    dirty = True
                    CraftCore.log.info(f"Patching {fileName}: replacing {oldPath} with {newPath}")
                    content = content.replace(oldPathBinary, newPath.encode())
            if dirty:
                with utils.makeWritable(fileName):
                    with open(fileName, "wb") as f:
                        f.write(content)
        return True

    def internalPostInstall(self):
        if not super().internalPostInstall():
            return False
        # a post install routine to fix the prefix (make things relocatable)
        newPrefix = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        oldPrefixes = [self.subinfo.buildPrefix]
        if CraftCore.compiler.isWindows:
            oldPrefixes += [self.subinfo.buildPrefix.replace("\\", "\\\\") ,OsUtils.toUnixPath(self.subinfo.buildPrefix), OsUtils.toMSysPath(self.subinfo.buildPrefix)]

        pattern = [re.compile("^.*(pc|pri|prl|cmake|bat|cmd|ini|pl)$")]
        files = utils.filterDirectoryContent(self.installDir(),
                                             whitelist=lambda x, root: utils.regexFileFilter(x, root, pattern),
                                             blacklist=lambda x, root: True)

        if not self.patchInstallPrefix(files, oldPrefixes, newPrefix):
            return False

        if (CraftCore.compiler.isMacOS
                and os.path.isdir(self.installDir())):
            files = utils.filterDirectoryContent(self.installDir(), lambda x, root: utils.isBinary(x.path), lambda x, root: True)
            for f in files:
                if os.path.islink(f):
                    continue
                _, ext = os.path.splitext(f)
                if ext in {".dylib", ".so"}:
                    # fix dylib id
                    with io.StringIO() as log:
                        utils.system(["otool", "-D", f], stdout=log)
                        oldId = log.getvalue().strip().split("\n")
                    # the first line is the file name
                    # the second the id, if we only get one line, there is no id to fix
                    if len(oldId) == 2:
                        oldId = oldId[1].strip()
                        newId = oldId.replace(self.subinfo.buildPrefix, newPrefix)
                        # TODO: meh, maybe there is a better way
                        newId = newId.replace("@rpath", os.path.join(newPrefix, "lib"))
                        if newId != oldId:
                            if not utils.system(["install_name_tool", "-id", newId, f]):
                                return False
                else:
                    # add rpath
                    # TODO: only call add rpath if its not set yet, calling it twice causes an error
                    utils.system(["install_name_tool", "-add_rpath", os.path.join(newPrefix, "lib"), f])

                # fix dependencies
                for dep in utils.getLibraryDeps(f):
                    if dep.startswith(self.subinfo.buildPrefix):
                        newDep = dep.replace(self.subinfo.buildPrefix, newPrefix)
                        if not utils.system(["install_name_tool", "-change", dep, newDep, f]):
                            return False

        # Install pdb files on MSVC if they are not found next to the dll
        if CraftCore.compiler.isMSVC and (self.buildType() == "RelWithDebInfo" or self.buildType() == "Debug") and  CraftCore.cache.findApplication("peparser"):
            files = utils.filterDirectoryContent(self.installDir(), lambda x, root: utils.isBinary(x.path),
                                                 lambda x, root: True)

            regexp = re.compile('{.*} (.*)')
            exclude = re.compile(r'icudt[0-9]*.dll')
            for f in files:
                if not os.path.exists(f"{os.path.splitext(f)[0]}.pdb"):
                    peparserOutput = CraftCore.cache.getCommandOutput("peparser", f"--pdb {f}")[1].strip()
                    pdbs = regexp.findall(peparserOutput)

                    if not exclude.match(os.path.basename(f)):
                        assert len(pdbs) > 0, f"No pdb file available: {f}"

                    for pdb in pdbs:
                        pdbDestination = os.path.join(os.path.dirname(f), os.path.basename(pdb))

                        CraftCore.log.info(f"Install pdb: {pdbDestination} for {os.path.basename(f)}")
                        utils.copyFile(pdb, pdbDestination, linkOnly=False)

        return True
