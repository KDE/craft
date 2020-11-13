# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
# Copyright 2009 Ralf Habacker <ralf.habacker@freenet.de>
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


""" \package BuildSystemBase"""
import glob
import io
import multiprocessing
import os
import re
import subprocess
from pathlib import Path

from CraftBase import *
from CraftOS.osutils import OsUtils
from Utils import CodeSign
from Utils.Arguments import Arguments


class BuildSystemBase(CraftBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    PatchableFile = {".service", ".pc", ".pri", ".prl", ".cmake", ".conf", ".sh", ".bat", ".cmd", ".ini", ".pl", ".pm", ".la", ".py"}

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
            if self.supportsNinja and CraftCore.settings.getboolean("Compile", "UseNinja", False) and CraftCore.cache.findApplication("ninja"):
                return "ninja"
            if ("Compile", "MakeProgram") in CraftCore.settings:
                makeProgram = CraftCore.settings.get("Compile", "MakeProgram")
                CraftCore.log.debug(f"set custom make program: {makeProgram}")
                if CraftCore.cache.findApplication(makeProgram):
                    return makeProgram
                else:
                    CraftCore.log.warning(f"Failed to find {CraftCore.settings.get('Compile', 'MakeProgram')}")
        elif not self.subinfo.options.make.supportsMultijob:
            if "MAKE" in os.environ:
                del os.environ["MAKE"]

        if OsUtils.isWin():
            if CraftCore.compiler.isMSVC() or CraftCore.compiler.isIntel():
                if self.subinfo.options.make.supportsMultijob:
                    return "jom"
                else:
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
        defines = Arguments(defines)
        defines += self.subinfo.options.configure.args

        if self.supportsCCACHE and CraftCore.cache.findApplication("ccache"):
            defines += self.ccacheOptions()
        if CraftCore.compiler.isClang() and self.supportsClang:
            defines += self.clangOptions()
        return defines

    def makeOptions(self, args):
        """return options for make command line"""
        defines = []
        if self.subinfo.options.make.ignoreErrors:
            defines.append("-i")
        makeProgram = self.makeProgram
        if makeProgram == "ninja":
            if CraftCore.debug.verbose() > 0:
                defines.append("-v")
        else:
            if CraftCore.debug.verbose() > 0:
                defines += ["VERBOSE=1", "V=1"]

        if self.subinfo.options.make.supportsMultijob and makeProgram != "nmake" :
            if makeProgram not in {"ninja", "jom"} or ("Compile", "Jobs") in CraftCore.settings:
                defines += ["-j", str(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count()))]

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

    def patchInstallPrefix(self, files: [str], oldPaths: [Path] = None, newPath: Path = Path(CraftCore.standardDirs.craftRoot())) -> bool:
        if not isinstance(oldPaths, list):
            oldPaths = [oldPaths]
        elif not oldPaths:
            oldPaths = [self.subinfo.buildPrefix]

        oldPaths = [Path(x).as_posix() for x in oldPaths]
        newValue = Path(newPath).as_posix().encode()
        for fileName in files:
            if not os.path.exists(fileName):
                CraftCore.log.warning(f"File {fileName} not found.")
                return False
            with open(fileName, "rb") as f:
                content = f.read()
            dirty = False
            for oldPath in oldPaths:
                assert os.path.isabs(oldPath)
                # allow front and back slashes
                oldPathPat = oldPath.replace("/", r"[/\\]+")
                # capture firs seperator
                oldPathPat = oldPathPat.replace(r"[/\\]+", r"(/+|\\+)", 1)
                oldPathPat = f"({oldPathPat})"
                oldPathPat = re.compile(oldPathPat.encode())
                for match in set(oldPathPat.findall(content)):
                    dirty = True
                    oldPath = match[0]
                    newPath = newValue.replace(b"/", match[1])
                    if oldPath != newPath:
                        CraftCore.log.info(f"Patching {fileName}: replacing {oldPath} with {newPath}")
                        content = content.replace(oldPath, newPath)
                    else:
                        CraftCore.log.debug(f"Skip Patching {fileName}:  prefix is unchanged {newPath}")
            if dirty:
                with utils.makeTemporaryWritable(fileName):
                    with open(fileName, "wb") as f:
                        f.write(content)
        return True

    def internalPostInstall(self):
        if not super().internalPostInstall():
            return False
        # fix absolute symlinks
        for sym in utils.filterDirectoryContent(self.installDir(), lambda x, root: x.is_symlink(), lambda x, root: True, allowBadSymlinks=True):
            target = Path(os.readlink(sym))
            if target.is_absolute():
                sym = Path(sym)
                target = Path(self.imageDir()) / target.relative_to(CraftCore.standardDirs.craftRoot())
                sym.unlink()
                # we can't use relative_to here
                sym.symlink_to(os.path.relpath(target, sym.parent))


        # a post install routine to fix the prefix (make things relocatable)
        newPrefix = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        oldPrefixes = [self.subinfo.buildPrefix]
        if CraftCore.compiler.isWindows:
            oldPrefixes += [OsUtils.toMSysPath(self.subinfo.buildPrefix)]

        files = utils.filterDirectoryContent(self.installDir(),
                                             whitelist=lambda x, root: Path(x).suffix in BuildSystemBase.PatchableFile,
                                             blacklist=lambda x, root: True)

        if not self.patchInstallPrefix(files, oldPrefixes, newPrefix):
            return False

        binaryFiles = list(utils.filterDirectoryContent(self.installDir(), lambda x, root: utils.isBinary(x.path), lambda x, root: True))
        if (CraftCore.compiler.isMacOS
                and os.path.isdir(self.installDir())):
            for f in binaryFiles:
                if os.path.islink(f):
                    continue
                # replace the old prefix or add it if missing
                craft_rpath = os.path.join(newPrefix, "lib")
                if not utils.system(["install_name_tool", "-rpath", os.path.join(self.subinfo.buildPrefix, "lib"), craft_rpath, f], logCommand=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
                    CraftCore.log.info(f"Adding rpath {craft_rpath} to {f}")
                    utils.system(["install_name_tool", "-add_rpath", craft_rpath, f], logCommand=False)

                # update prefix
                if self.subinfo.buildPrefix != newPrefix:
                    if os.path.splitext(f)[1] in {".dylib", ".so"}:
                        # fix dylib id
                        with io.StringIO() as log:
                            utils.system(["otool", "-D", f], stdout=log, logCommand=False)
                            oldId = log.getvalue().strip().split("\n")
                        # the first line is the file name
                        # the second the id, if we only get one line, there is no id to fix
                        if len(oldId) == 2:
                            oldId = oldId[1].strip()
                            newId = oldId.replace(self.subinfo.buildPrefix, newPrefix)
                            if newId != oldId:
                                if not utils.system(["install_name_tool", "-id", newId, f], logCommand=False):
                                    return False

                    # fix dependencies
                    for dep in utils.getLibraryDeps(f):
                        if dep.startswith(self.subinfo.buildPrefix):
                            newDep = dep.replace(self.subinfo.buildPrefix, newPrefix)
                            if newDep != dep:
                                if not utils.system(["install_name_tool", "-change", dep, newDep, f], logCommand=False):
                                    return False

        # Install pdb files on MSVC if they are not found next to the dll
        # skip if we are a release build or from cache
        if not self.subinfo.isCachedBuild:
            if self.buildType() in {"RelWithDebInfo", "Debug"}:
                if CraftCore.compiler.isMSVC():
                    for f in binaryFiles:
                        if not os.path.exists(f"{os.path.splitext(f)[0]}.pdb"):
                            pdb = utils.getPDBForBinary(f)
                            if not pdb:
                                CraftCore.log.warning(f"Could not find a PDB for {f}")
                                continue
                            if not os.path.exists(pdb):
                                CraftCore.log.warning(f"PDB {pdb} for {f} does not exist")
                                continue
                            pdbDestination = os.path.join(os.path.dirname(f), os.path.basename(pdb))

                            CraftCore.log.info(f"Install pdb: {pdbDestination} for {os.path.basename(f)}")
                            utils.copyFile(pdb, pdbDestination, linkOnly=False)
                else:
                    if not self.subinfo.options.package.disableStriping:
                        for f in binaryFiles:
                            utils.strip(f)

            # sign the binaries if we can
            if CraftCore.compiler.isWindows and CraftCore.settings.getboolean("CodeSigning", "SignCache", False):
                if not CodeSign.signWindows(binaryFiles):
                    return False
        return True
