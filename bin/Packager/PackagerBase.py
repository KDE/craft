#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

import datetime
import json
import glob
from pathlib import Path

from CraftBase import *

from Utils import CraftHash
from Utils.CraftManifest import *

from CraftDebug import deprecated


class PackagerBase(CraftBase):
    """ provides a generic interface for packagers and implements basic package creating stuff """

    @InitGuard.init_once
    def __init__(self):
        CraftBase.__init__(self)
        self.whitelist_file = []
        self.blacklist_file = []
        self.defines = {}
        self.ignoredPackages = []

    def setDefaults(self, defines: {str:str}) -> {str:str}:
        defines = dict(defines)
        defines.setdefault("setupname", os.path.join(self.packageDestinationDir(), self.binaryArchiveName(includeRevision=True, fileType="")))
        defines.setdefault("shortcuts", "")
        defines.setdefault("architecture", CraftCore.compiler.architecture)
        defines.setdefault("company", "KDE e.V.")
        defines.setdefault("productname", self.subinfo.displayName)
        defines.setdefault("display_name", self.subinfo.displayName)
        defines.setdefault("description", self.subinfo.description)
        defines.setdefault("icon", os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craft.ico"))
        defines.setdefault("icon_png", os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craftyBENDER.png"))
        defines.setdefault("icon_png_44", defines["icon_png"])
        defines.setdefault("license", "")
        defines.setdefault("version", self.sourceRevision() if self.subinfo.hasSvnTarget() else self.version)
        defines.setdefault("website",
                           self.subinfo.webpage if self.subinfo.webpage else "https://community.kde.org/Craft")

        # mac
        defines.setdefault("apppath", "")
        defines.setdefault("appname", self.package.name.lower())
        return defines

    def getMacAppPath(self, defines, lookupPath = None):
        lookPath = os.path.normpath(lookupPath if lookupPath else self.archiveDir())
        appPath = defines['apppath']
        if not appPath:
            apps = glob.glob(os.path.join(lookPath, f"**/{defines['appname']}.app"), recursive=True)
            if len(apps) != 1:
                CraftCore.log.error(f"Failed to detect {defines['appname']}.app for {self}, please provide a correct self.defines['apppath'] or a relative path to the app as self.defines['apppath']")
                return False
            appPath = apps[0]
        appPath = os.path.join(lookPath, appPath)
        return os.path.normpath(appPath)

    def preArchive(self):
        utils.abstract()

    def archiveDir(self):
        return os.path.join(self.buildRoot(), "archive")

    def archiveDebugDir(self) -> Path:
        return Path(f"{self.archiveDir()}-dbg")

    def artifactsDir(self) -> Path:
        return Path(self.buildRoot()) / "artifacts"

    # """ create a package """
    def createPackage(self):
        utils.abstract()

    def _generateManifest(self, destDir, archiveName, manifestLocation=None, manifestUrls=None):
        if not manifestLocation:
            manifestLocation = destDir
        manifestLocation = os.path.join(manifestLocation, "manifest.json")
        archiveFile = os.path.join(destDir, archiveName)

        name = archiveName if not os.path.isabs(archiveName) else os.path.relpath(archiveName, destDir)

        manifest = CraftManifest.load(manifestLocation, urls=manifestUrls)
        entry = manifest.get(str(self))
        entry.addFile(name, CraftHash.digestFile(archiveFile, CraftHash.HashAlgorithm.SHA256), version=self.version, config=self.subinfo.options.dynamic)

        manifest.dump(manifestLocation)

    @property
    def archiveExtension(self):
        extension = "." + CraftCore.settings.get("Packager", "7ZipArchiveType", "7z")
        if extension == ".7z" and CraftCore.compiler.isUnix:
            if self.package.path == "dev-utils/7zip" or not CraftCore.cache.findApplication("7za"):
                extension = ".tar.xz"
            else:
                extension = ".tar.7z"
        return extension

    def _createArchive(self, archiveName, sourceDir, destDir, createDigests=True) -> bool:
        archiveName = str((Path(destDir) / archiveName))
        if not utils.compress(archiveName, sourceDir):
            return False

        if createDigests:
            if CraftCore.settings.getboolean("Packager", "CreateCache") and CraftCore.settings.get("Packager", "PackageType") == "SevenZipPackager":
                if CraftCore.settings.getboolean("ContinuousIntegration", "UpdateRepository", False):
                    manifestUrls = [self.cacheRepositoryUrls()[0]]
                else:
                    CraftCore.log.warning(f"Creating new cache, if you want to extend an existing cache, set \"[ContinuousIntegration]UpdateRepository = True\"")
                    manifestUrls = None
                self._generateManifest(destDir, archiveName, manifestLocation=self.cacheLocation(),
                                       manifestUrls=manifestUrls)
            else:
                self._generateManifest(destDir, archiveName)
                CraftHash.createDigestFiles(archiveName)
        return True

    def addExecutableFilter(self, pattern : str):
        pass