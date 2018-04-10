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
                #convert to forward path sep
                line = line.replace(r"\\", "/")
                tmp = f"^{line}$"
                re.compile(tmp)  # for debug
                regex.append(tmp)
                CraftCore.log.debug(f"{line} added to {targetName} as {tmp}")
            except re.error:
                CraftCore.log.critical(f"{tmp} is not a valid regexp")
    return re.compile(f"({'|'.join(regex)})", re.IGNORECASE)


class PackagerLists(object):
    """ This class provides some staticmethods that can be used as pre defined black or whitelists """

    @staticmethod
    def runtimeBlacklist():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "applications_blacklist.txt")

    @staticmethod
    def defaultWhitelist():
        return [re.compile(".*")]

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
                    self.read_whitelist(entry)
        return self._whitelist

    @property
    def blacklist(self):
        if not self._blacklist:
            for entry in self.blacklist_file:
                CraftCore.log.debug("reading blacklist: %s" % entry)
                if callable(entry):
                    if entry == PackagerLists.runtimeBlacklist:
                        CraftCore.log.warn("Compat mode for PackagerLists.runtimeBlacklist -- please just use self.blacklist_file.append(\"myblacklist.txt\") instead of self.blacklist_file = [...]")
                        self.read_blacklist(entry())
                        continue

                    for line in entry():
                        self._blacklist.append(line)
                else:
                    self.read_blacklist(entry)
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
            if isinstance(x, SourceOnlyPackageBase):
                CraftCore.log.debug(f"Ignoring package it is source only: {x}")
                continue

            _package = x.instance

            imageDirs.append((x.instance.imageDir(), x.subinfo.options.package.disableStriping))
            # this loop collects the files from all image directories
            CraftCore.log.debug(f"__getImageDirectories: package: {x}, version: {x.version}")

        if self.__deployQtSdk:
            imageDirs.append((self.__qtSdkDir, False))

        return imageDirs

    def read_whitelist(self, fname):
        if not os.path.isabs(fname):
            fname = os.path.join(self.packageDir(), fname)
        """ Read regular expressions from fname """
        self._whitelist.append(toRegExp(fname, "whitelist"))

    def read_blacklist(self, fname):
        if not os.path.isabs(fname):
            fname = os.path.join(self.packageDir(), fname)
        """ Read regular expressions from fname """
        self._blacklist.append(toRegExp(fname, "blacklist"))

    def whitelisted(self, pathname):
        """ return True if pathname is included in the pattern, and False if not """
        for pattern in self.whitelist:
            if pattern.search(pathname):
                return True
        return False

    def blacklisted(self, filename):
        """ return False if file is not blacklisted, and True if it is blacklisted """
        for pattern in self.blacklist:
            if pattern.search(filename):
                CraftCore.log.debug(f"{filename} is blacklisted: {pattern.pattern}")
                return True
        return False

    def _filterQtBuildType(self, filename):
        if not self.__deployQtSdk:
            return True
        filename = OsUtils.toNativePath(filename)
        if self.__qtSdkDir not in filename:
            return True

        if filename.endswith(".dll") or filename.endswith(".exe"):
            if not CraftCore.cache.findApplication("clrphtester"):
                raise BlueprintException("Deploying a QtSdk depends on dev-util/dependencies", CraftPackageObject.get("dev-util/dependencies"))
            _, imports = CraftCore.cache.getCommandOutput("clrphtester", f"-imports {filename}")
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

    def traverse(self, directory, whitelist=lambda f: True, blacklist=lambda g: False):
        """
            Traverse through a directory tree and return every
            filename that the function whitelist returns as true and
            which do not match blacklist entries
        """
        directory = OsUtils.toUnixPath(directory)
        if blacklist(directory):
            return
        if not directory.endswith("/"):
            directory += "/"
        dirs = [directory]
        while dirs:
            path = dirs.pop()
            for f in os.listdir(path):
                f = OsUtils.toUnixPath(os.path.join(path, f))
                z = f.replace(directory, "")
                if blacklist(z):
                    continue
                if os.path.isdir(f):
                    dirs.append(f)
                elif os.path.isfile(f) and whitelist(z):
                    if self._filterQtBuildType(f):
                        yield f

    def copyFiles(self, srcDir, destDir, dontStrip) -> bool:
        """
            Copy the binaries for the Package from srcDir to the imageDir
            directory
        """
        srcDir = OsUtils.toUnixPath(srcDir)
        destDir = OsUtils.toUnixPath(destDir)
        if not destDir.endswith("/"):
            destDir += "/"
        CraftCore.log.debug("Copying %s -> %s" % (srcDir, destDir))

        for entry in self.traverse(srcDir, self.whitelisted, self.blacklisted):
            entry_target = OsUtils.toNativePath(entry.replace(srcDir, destDir))
            if not utils.copyFile(entry, entry_target, linkOnly=False):
                return False
            if not dontStrip:
                if OsUtils.isWin():
                    if entry_target.endswith((".dll", ".exe")):
                        self.strip(entry_target)
                elif OsUtils.isUnix():
                    if not os.path.islink(entry_target) and ".so" in entry_target or os.access(entry_target, os.X_OK):
                        self.strip(entry_target)
        return True

    def internalCreatePackage(self) -> bool:
        """ create a package """

        archiveDir = self.archiveDir()

        CraftCore.log.debug("cleaning package dir: %s" % archiveDir)
        utils.cleanDirectory(archiveDir)
        for directory, strip in self.__getImageDirectories():
            imageDir = archiveDir
            if os.path.exists(directory):
                if not self.copyFiles(directory, imageDir, strip):
                    return False
            else:
                CraftCore.log.critical("image directory %s does not exist!" % directory)
                return False

        if not utils.createDir(archiveDir):
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

        if CraftCore.settings.getboolean("CodeSigning", "Enabled", False):
            files = []
            if CraftCore.compiler.isWindows:
                for pattern in ["**/*.dll", "**/*.exe"]:
                    files.extend(glob.glob(os.path.join(archiveDir, pattern), recursive=True))
            if not utils.sign(files):
                return False
        return True

    def preArchive(self):
        return True
