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

import inspect
import os
import re
from pathlib import Path
from typing import List

import utils
from Blueprints.CraftDependencyPackage import CraftDependencyPackage, DependencyType
from Blueprints.CraftPackageObject import BlueprintException, CraftPackageObject
from CraftBase import InitGuard
from CraftCore import CraftCore
from Package.SourceOnlyPackageBase import SourceOnlyPackageBase
from Packager.PackagerBase import PackagerBase
from Utils import CodeSign
from Utils.CraftManifest import FileType


def toRegExp(fname, targetName) -> re:
    """Read regular expressions from fname"""
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
                tmp = f"^{line}$"
                re.compile(tmp)  # for debug
                regex.append(tmp)
                CraftCore.log.debug(f"{line} added to {targetName} as {tmp}")
            except re.error as e:
                raise Exception(f"{tmp} is not a valid regular expression: {e}")
    return re.compile(f"({'|'.join(regex)})", re.IGNORECASE)


class PackagerLists(object):
    """This class provides some staticmethods that can be used as pre defined black or whitelists"""

    @staticmethod
    def runtimeBlacklist():
        bls = [
            "applications_blacklist.txt",
            f"applications_blacklist_{CraftCore.compiler.platform.name.lower()}.txt",
        ]
        return filter(
            lambda x: x.exists(),
            [(Path(__file__).absolute().parent / "blacklists" / x) for x in bls],
        )

    @staticmethod
    def defaultWhitelist():
        return [re.compile("^$")]

    @staticmethod
    def defaultBlacklist():
        return [toRegExp(x, x.name) for x in PackagerLists.runtimeBlacklist()]


class CollectionPackagerBase(PackagerBase):
    @InitGuard.init_once
    def __init__(self, package: CraftPackageObject, whitelists=None, blacklists=None):
        PackagerBase.__init__(self, package)
        if not whitelists:
            whitelists = [PackagerLists.defaultWhitelist]
        if not blacklists:
            blacklists = [self.defaultBlacklist]
        if not self.whitelist_file:
            self.whitelist_file = whitelists
        if not self.blacklist_file:
            self.blacklist_file = blacklists
        self._whitelist = []
        self._whitelist_filters = set()
        self._blacklist = []
        self._blacklist_filters = set()
        self.scriptname = None

    def runtimeBlacklist(self):
        bls = [
            Path(__file__).absolute().parent / "blacklists" / "applications_blacklist.txt",
            Path(__file__).absolute().parent / "blacklists" / f"applications_blacklist_{CraftCore.compiler.platform.name.lower()}.txt",
        ]
        if self.sourceDir():
            bls.append(Path(self.sourceDir()) / ".craftignore")
        return [path for path in bls if path.exists()]

    def defaultBlacklist(self):
        return [toRegExp(x, x.name) for x in self.runtimeBlacklist()]

    def addBlacklistFilter(self, x):
        assert callable(x) and len(inspect.signature(x).parameters) == 2
        self._blacklist_filters.add(x)

    def addExecutableFilter(self, pattern: str):
        # TODO: move to parent?
        self.addBlacklistFilter(
            lambda fileName, root: utils.regexFileFilter(fileName, root, [re.compile(pattern, re.IGNORECASE)])
            and utils.isExecuatable(fileName, includeShellScripts=True)
        )

    def addWhitelistFilter(self, x):
        assert callable(x) and len(inspect.signature(x).parameters) == 2
        self._whitelist_filters.add(x)

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
                    if entry == self.runtimeBlacklist:
                        CraftCore.log.warn(
                            'Compat mode for PackagerLists.runtimeBlacklist -- please just use self.blacklist_file.append("myblacklist.txt") instead of self.blacklist_file = [...]'
                        )
                        self._blacklist += self.defaultBlacklist()
                        continue

                    for line in entry():
                        self._blacklist.append(line)
                else:
                    self._blacklist.append(self.read_blacklist(entry))
        return self._blacklist

    def __getImageDirectories(self):
        """return the image directories where the files are stored"""
        imageDirs = []
        depList = CraftDependencyPackage(self.package).getDependencies(
            depType=DependencyType.Runtime | DependencyType.Packaging,
            ignoredPackages=self.ignoredPackages,
        )

        for x in depList:
            _package = x.instance
            if isinstance(_package, SourceOnlyPackageBase):
                CraftCore.log.debug(f"Ignoring package it is source only: {x}")
                continue
            imageDirs.append(x.instance)
            # this loop collects the files from all image directories
            CraftCore.log.debug(f"__getImageDirectories: package: {x}, version: {x.version}")
        return imageDirs

    def read_whitelist(self, fname: str) -> re:
        if not os.path.isabs(fname):
            fname = os.path.join(self.blueprintDir(), fname)
        """ Read regular expressions from fname """
        try:
            return toRegExp(fname, "whitelist")
        except Exception as e:
            raise BlueprintException(str(e), self.package)

    def read_blacklist(self, fname: str) -> re:
        if not os.path.isabs(fname):
            fname = os.path.join(self.blueprintDir(), fname)
        """ Read regular expressions from fname """
        try:
            return toRegExp(fname, "blacklist")
        except Exception as e:
            raise BlueprintException(str(e), self.package)

    def whitelisted(self, filename: os.DirEntry, root: str, whiteList: [re] = None) -> bool:
        """return True if pathname is included in the pattern, and False if not"""
        if whiteList is None:
            whiteList = self.whitelist
        return self.blacklisted(filename, root=root, blackList=whiteList, message="whitelisted")

    def blacklisted(
        self,
        filename: os.DirEntry,
        root: str,
        blackList: [re] = None,
        message: str = "blacklisted",
    ) -> bool:
        """return False if file is not blacklisted, and True if it is blacklisted"""
        if blackList is None:
            blackList = self.blacklist
        CraftCore.log.debug(f"Start filtering: {message}")
        _blacklists = set([lambda filename, root: utils.regexFileFilter(filename, root, blackList)])
        if message == "blacklisted":
            _blacklists.update(self._blacklist_filters)
        elif message == "whitelisted":
            _blacklists.update(self._whitelist_filters)
        for b in _blacklists:
            if b(filename, root):
                return True
        return False

    def copyFiles(self, srcDir: Path, destDir: Path, filesToSign: List[Path]) -> bool:
        """
        Copy the binaries for the Package from srcDir to the imageDir
        directory
        """
        CraftCore.log.debug("Copying %s -> %s" % (srcDir, destDir))

        # Only sign all files on Windows. On MacOS we recursively sign the whole .app Folder
        doSign = CraftCore.compiler.isWindows and CraftCore.settings.getboolean("CodeSigning", "Enabled", False)
        if doSign and CraftCore.settings.getboolean("CodeSigning", "SignCache", False):
            # files from the cache are already signed, but files from this package need to be signed
            doSign = os.path.samefile(srcDir, self.imageDir())

        for entry in utils.filterDirectoryContent(srcDir, self.whitelisted, self.blacklisted, handleAppBundleAsFile=True):
            entry_target = os.path.join(destDir, os.path.relpath(entry, srcDir))
            if os.path.isfile(entry) or os.path.islink(entry):
                if not utils.copyFile(entry, entry_target, linkOnly=False):
                    return False
                if utils.isBinary(entry_target):
                    if doSign:
                        filesToSign.append(entry_target)
            else:
                # .app or .dSYM
                assert CraftCore.compiler.isMacOS
                if not utils.copyDir(entry, entry_target, linkOnly=False):
                    return False

        return True

    def internalCreatePackage(self, defines) -> bool:
        """create a package"""

        packageSymbols = CraftCore.settings.getboolean("Packager", "PackageDebugSymbols", False)
        archiveDir = self.archiveDir()

        CraftCore.log.debug("cleaning package dir: %s" % archiveDir)
        utils.cleanDirectory(archiveDir)
        if packageSymbols:
            utils.cleanDirectory(self.archiveDebugDir())

        filesToSign = []

        for package in self.__getImageDirectories():
            if package.imageDir().exists():
                if not self.copyFiles(package.imageDir(), archiveDir, filesToSign):
                    return False
            else:
                CraftCore.log.critical("image directory %s does not exist!" % package.imageDir())
                return False
            if packageSymbols:
                if package.symbolsImageDir().exists():
                    if not self.copyFiles(package.symbolsImageDir(), self.archiveDebugDir(), filesToSign):
                        return False
                else:
                    CraftCore.log.warning("symbols directory %s does not exist!" % package.symbolsImageDir())

        if filesToSign:
            if not CodeSign.signWindows(filesToSign):
                return False

        # TODO: find a better name for the hooks
        if not self.preArchiveMove():
            return False
        pathsToMoveToBinPath = []
        if self.subinfo.options.package.movePluginsToBin:
            # Qt expects plugins and qml files below bin, on the target system
            pathsToMoveToBinPath += [
                os.path.join(archiveDir, "plugins"),
                os.path.join(archiveDir, "qml"),
            ]
        binPath = os.path.join(archiveDir, "bin")
        for path in pathsToMoveToBinPath:
            if os.path.isdir(path):
                if not utils.mergeTree(path, binPath):
                    return False

        if self.subinfo.options.package.moveTranslationsToBin:
            # Qt expects translations directory below bin, on the target system
            translationsPath = os.path.join(archiveDir, "translations")
            if os.path.isdir(translationsPath):
                if not utils.mergeTree(translationsPath, os.path.join(binPath, "translations")):
                    return False

        if not self.preArchive():
            return False

        # package symbols if the dir isn't empty
        if packageSymbols and os.listdir(self.archiveDebugDir()):
            dbgName = Path("{0}-dbg{1}".format(*os.path.splitext(defines["setupname"])))
            if not CraftCore.compiler.isWindows:
                dbgName = dbgName.with_suffix(".tar.7z")
            else:
                dbgName = dbgName.with_suffix(".7z")
            if dbgName.exists():
                dbgName.unlink()
            if not self._createArchive(
                dbgName,
                self.archiveDebugDir(),
                self.packageDestinationDir(),
                fileType=FileType.Debug,
            ):
                return False

        return True

    def preArchive(self):
        return True

    def preArchiveMove(self):
        return True
