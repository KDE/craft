# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
# copyright (c) 2010-2011 Patrick Spendrin <ps_ml@gmx.de>
# copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
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

import types
import glob

from Packager.PackagerBase import *
from Blueprints.CraftDependencyPackage import DependencyType, CraftDependencyPackage
from Blueprints.CraftPackageObject import *
from Package.SourceOnlyPackageBase import *


def toRegExp(fname, targetName) -> re:
    """ Read regular expressions from fname """
    assert os.path.isabs(fname)

    if not os.path.isfile(fname):
        CraftCore.log.critical("%s not found at: %s" % (targetName.capitalize(), os.path.abspath(fname)))
    regex = []
    with open(fname, "rt+") as f:
        for line in f:
            # Cleanup white spaces / line endings
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                # accept forward and backward slashes
                line = line.replace("/", r"[/\\]")
                tmp = f"^{line}$"
                re.compile(tmp)  # for debug
                regex.append(tmp)
                CraftCore.log.debug(f"{line} added to {targetName} as {tmp}")
            except re.error as e:
                raise Exception(f"{tmp} is not a valid regular expression: {e}")
    return re.compile(f"({'|'.join(regex)})", re.IGNORECASE)


class PackagerLists(object):
    """ This class provides some staticmethods that can be used as pre defined black or whitelists """

    @staticmethod
    def runtimeBlacklist():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "applications_blacklist.txt")

    @staticmethod
    def defaultWhitelist():
        return [re.compile("^$")]

    @staticmethod
    def defaultBlacklist():
        return [toRegExp(PackagerLists.runtimeBlacklist(), "blacklist")]


class CollectionPackagerBase(PackagerBase):
    reMsvcDebugRt = re.compile(r"VCRUNTIME.*D\.DLL", re.IGNORECASE)

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        PackagerBase.__init__(self)
        if not whitelists:
            whitelists = [PackagerLists.defaultWhitelist]
        if not blacklists:
            blacklists = [PackagerLists.defaultBlacklist]
        if not self.whitelist_file:
            self.whitelist_file = whitelists
        if not self.blacklist_file:
            self.blacklist_file = blacklists
        self._whitelist = []
        self._blacklist = []
        self.scriptname = None

        self.__deployQtSdk = (OsUtils.isWin() and
                             CraftCore.settings.getboolean("QtSDK", "Enabled", False) and
                             CraftCore.settings.getboolean("QtSDK","PackageQtSDK",True))
        self.__qtSdkDir = OsUtils.toNativePath(os.path.join(CraftCore.settings.get("QtSDK", "Path"),
                                                            CraftCore.settings.get("QtSDK", "Version"),
                                                            CraftCore.settings.get("QtSDK", "Compiler"))) if self.__deployQtSdk else None

    @property
    def whitelist(self):
        if not self._whitelist:
            for entry in self.whitelist_file:
                CraftCore.log.debug("reading whitelist: %s" % entry)
                if callable(entry):
                    for line in entry():
                        self._whitelist.append(line)
                else:
                    self._whitelist.append(self.read_whitelist(entry))
        return self._whitelist

    @property
    def blacklist(self):
        if not self._blacklist:
            for entry in self.blacklist_file:
                CraftCore.log.debug("reading blacklist: %s" % entry)
                if callable(entry):
                    if entry == PackagerLists.runtimeBlacklist:
                        CraftCore.log.warn("Compat mode for PackagerLists.runtimeBlacklist -- please just use self.blacklist_file.append(\"myblacklist.txt\") instead of self.blacklist_file = [...]")
                        self._blacklist.append(self.read_blacklist(entry()))
                        continue

                    for line in entry():
                        self._blacklist.append(line)
                else:
                    self._blacklist.append(self.read_blacklist(entry))
        return self._blacklist

    def __imageDirPattern(self, package, buildTarget):
        """ return base directory name for package related image directory """
        directory = "image"

        if package.subinfo.options.useBuildType == True:
            directory += '-' + package.buildType()
        directory += '-' + buildTarget
        return directory

    def __getImageDirectories(self):
        """ return the image directories where the files are stored """
        imageDirs = []
        depList = CraftDependencyPackage(self.package).getDependencies(depType=DependencyType.Runtime|DependencyType.Packaging,
                                                                       ignoredPackages=self.ignoredPackages)

        for x in depList:
            _package = x.instance
            if isinstance(_package, SourceOnlyPackageBase):
                CraftCore.log.debug(f"Ignoring package it is source only: {x}")
                continue
            imageDirs.append((x.instance.imageDir(), x.subinfo.options.package.disableStriping))
            # this loop collects the files from all image directories
            CraftCore.log.debug(f"__getImageDirectories: package: {x}, version: {x.version}")

        if self.__deployQtSdk:
            imageDirs.append((self.__qtSdkDir, False))

        return imageDirs

    def read_whitelist(self, fname : str) -> re:
        if not os.path.isabs(fname):
            fname = os.path.join(self.packageDir(), fname)
        """ Read regular expressions from fname """
        try:
          return toRegExp(fname, "whitelist")
        except Exception as e:
          raise BlueprintException(str(e), self.package)

    def read_blacklist(self, fname : str) -> re:
        if not os.path.isabs(fname):
            fname = os.path.join(self.packageDir(), fname)
        """ Read regular expressions from fname """
        try:
          return toRegExp(fname, "blacklist")
        except Exception as e:
          raise BlueprintException(str(e), self.package)

    def whitelisted(self, filename : os.DirEntry, root : str, whiteList : [re]=None) -> bool:
        """ return True if pathname is included in the pattern, and False if not """
        if whiteList is None:
            whiteList = self.whitelist
        return self.blacklisted(filename, root=root, blackList=whiteList, message="whitelisted")

    def blacklisted(self, filename : os.DirEntry, root : str, blackList : [re]=None, message : str="blacklisted") -> bool:
        """ return False if file is not blacklisted, and True if it is blacklisted """
        if blackList is None:
            blackList = self.blacklist
        CraftCore.log.debug(f"Start filtering: {message}")
        return utils.regexFileFilter(filename, root, blackList)

    def _filterQtBuildType(self, filename):
        if not self.__deployQtSdk:
            return True
        filename = OsUtils.toNativePath(filename)
        if self.__qtSdkDir not in filename:
            return True

        if utils.isBinary(filename):
            if not CraftCore.cache.findApplication("dependencies"):
                raise BlueprintException("Deploying a QtSdk depends on dev-util/dependencies", CraftPackageObject.get("dev-util/dependencies"))
            _, imports = CraftCore.cache.getCommandOutput("dependencies", f"-imports {filename}")
            rt = CollectionPackagerBase.reMsvcDebugRt.findall(imports)
            out = False
            if self.buildType() == "Debug":
                out = rt is not []
            else:
                out = not rt
            if not out:
                CraftCore.log.debug(f"Skipp {filename} as it has the wrong build type: {rt}")
            return out
        return True

    def copyFiles(self, srcDir, destDir) -> bool:
        """
            Copy the binaries for the Package from srcDir to the imageDir
            directory
        """
        CraftCore.log.debug("Copying %s -> %s" % (srcDir, destDir))

        filesToSign = []
        doSign = CraftCore.compiler.isWindows and CraftCore.settings.getboolean("CodeSigning", "Enabled", False)
        if doSign and CraftCore.settings.getboolean("CodeSigning", "SignCache", False):
            # files from the cache are already signed
            doSign = os.path.samefile(srcDir, self.imageDir())

        for entry in utils.filterDirectoryContent(srcDir, self.whitelisted, self.blacklisted):
            if not self._filterQtBuildType(entry):
                continue
            entry_target = os.path.join(destDir, os.path.relpath(entry, srcDir))
            if not utils.copyFile(entry, entry_target, linkOnly=False):
                return False
            if utils.isBinary(entry_target):
                if doSign:
                    filesToSign.append(entry_target)
        if filesToSign:
            utils.sign(filesToSign)
        return True

    def internalCreatePackage(self, defines=None, seperateSymbolFiles=False, packageSymbols=True) -> bool:
        """ create a package """

        seperateSymbolFiles = seperateSymbolFiles and CraftCore.settings.getboolean("Packager", "PackageDebugSymbols", False)
        archiveDir = self.archiveDir()

        if CraftCore.compiler.isMacOS:
            symbolSuffix = ".dSYM"
            symbolPattern = r".*\{0}/.*".format(symbolSuffix)
        else:
            if CraftCore.compiler.isMSVC():
                symbolSuffix = ".pdb"
            else:
                symbolSuffix = ".sym"
            symbolPattern = r".*\{0}".format(symbolSuffix)
        symbolPattern = re.compile(symbolPattern)

        if not seperateSymbolFiles:
            self.blacklist.append(symbolPattern)


        CraftCore.log.debug("cleaning package dir: %s" % archiveDir)
        utils.cleanDirectory(archiveDir)
        if seperateSymbolFiles:
            utils.cleanDirectory(self.archiveDebugDir())

        for directory, strip in self.__getImageDirectories():
            if os.path.exists(directory):
                if not self.copyFiles(directory, archiveDir):
                    return False
            else:
                CraftCore.log.critical("image directory %s does not exist!" % directory)
                return False

        if self.subinfo.options.package.movePluginsToBin:
            # Qt expects plugins and qml files below bin, on the target sytsem
            binPath = os.path.join(archiveDir, "bin")
            for path in [os.path.join(archiveDir, "plugins"), os.path.join(archiveDir, "qml")]:
                if os.path.isdir(path):
                    if not utils.mergeTree(path, binPath):
                        return False

        if not self.preArchive():
            return False

        if seperateSymbolFiles:
            CraftCore.log.info(f"Move symbols to {self.archiveDebugDir()}")
            utils.cleanDirectory(self.archiveDebugDir())
            for sym in utils.filterDirectoryContent(archiveDir,
                                                    whitelist=lambda x, root: utils.isBinary(x.path),
                                                    blacklist=lambda x, root: True):
                sym = Path(sym).with_suffix(symbolSuffix)
                if sym.exists():
                    dest = Path(self.archiveDebugDir()) / os.path.relpath(sym, archiveDir)
                    CraftCore.log.info(f"Move symbols: {sym} {dest}")
                    if not (utils.createDir(dest.parent) and utils.moveFile(sym, dest)):
                        return False

            CraftCore.log.info("Remove unused symbols")
            for sym in utils.filterDirectoryContent(archiveDir,
                                                    whitelist=lambda x, root: utils.regexFileFilter(x, root, [symbolPattern]),
                                                    blacklist=lambda x, root: True):
                CraftCore.log.info(f"Delete symbols: {sym}")
                if not utils.deleteFile(sym):
                    return False

            if packageSymbols and os.path.exists(self.archiveDebugDir()):
                dbgName = Path("{0}-dbg{1}".format(*os.path.splitext(defines["setupname"])))
                if dbgName.exists():
                    dbgName.unlink()
                if not self._createArchive(dbgName, self.archiveDebugDir(), self.packageDestinationDir()):
                    return False

        return True

    def preArchive(self):
        return True
