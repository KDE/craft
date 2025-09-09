#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

import abc
import glob
import os
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftBase import CraftBase, InitGuard
from CraftCore import CraftCore
from Utils import CraftHash
from Utils.CraftManifest import CraftManifest, FileType


class PackagerBase(CraftBase):
    """provides a generic interface for packagers and implements basic package creating stuff"""

    @InitGuard.init_once
    def __init__(self, package: CraftPackageObject):
        CraftBase.__init__(self, package)
        self.whitelist_file = []
        self.blacklist_file = []
        self.defines = {}
        self.ignoredPackages = []
        self._manifest = None
        self._currentManifestEnty = None

    def setDefaults(self, defines: set[str, str]) -> set[str, str]:
        defines = dict(defines)
        defines.setdefault(
            "setupname",
            self.packageDestinationDir() / self.binaryArchiveName(includeRevision=True, fileType=""),
        )
        defines.setdefault("shortcuts", "")
        defines.setdefault("company", "KDE e.V.")
        defines.setdefault("productname", self.subinfo.displayName)
        defines.setdefault("display_name", self.subinfo.displayName)
        defines.setdefault("description", self.subinfo.description)
        defines.setdefault(
            "icon",
            CraftCore.standardDirs.craftBin() / "data/icons/craft.ico",
        )
        defines.setdefault(
            "icon_png",
            CraftCore.standardDirs.craftBin() / "data/icons/craftyBENDER.png",
        )
        defines.setdefault("icon_png_44", defines["icon_png"])
        defines.setdefault("license", "")
        defines.setdefault("readme", "")
        defines.setdefault(
            "version",
            self.sourceRevision() if self.subinfo.hasSvnTarget() else self.version,
        )
        defines.setdefault(
            "website",
            self.subinfo.webpage if self.subinfo.webpage else "https://community.kde.org/Craft",
        )

        # mac
        defines.setdefault("apppath", "")
        defines.setdefault("appname", self.package.name.lower())
        return defines

    def getMacAppPath(self, defines, lookupPath=None) -> Path:
        lookPath = Path(lookupPath if lookupPath else self.archiveDir())
        appPath = defines["apppath"]
        if not appPath:
            apps = glob.glob(str(lookPath / f"**/{defines['appname']}.app"), recursive=True)
            if len(apps) != 1:
                CraftCore.log.error(
                    f"Failed to detect {defines['appname']}.app for {self}, please provide a correct self.defines['apppath'] or a relative path to the app as self.defines['apppath']"
                )
                return None
            appPath = apps[0]
        return lookPath / appPath

    @abc.abstractmethod
    def preArchive(self):
        pass

    def archiveDir(self):
        return self.buildRoot() / "archive"

    def archiveDebugDir(self) -> Path:
        return Path(f"{self.archiveDir()}-dbg")

    def artifactsDir(self) -> Path:
        return Path(self.buildRoot()) / "artifacts"

    # """ create a package """
    @abc.abstractmethod
    def createPackage(self):
        pass

    def _generateManifest(
        self,
        destDir,
        archiveName: Path,
        manifestLocation=None,
        manifestUrls=None,
        fileType: FileType = FileType.Binary,
    ):
        if not manifestLocation:
            manifestLocation = destDir
        manifestLocation = os.path.join(manifestLocation, "manifest.json")
        archiveFile = os.path.join(destDir, archiveName)

        name = archiveName if not os.path.isabs(archiveName) else os.path.relpath(archiveName, destDir)
        if not self._manifest:
            self._manifest = CraftManifest.load(manifestLocation, urls=manifestUrls)
        if not self._currentManifestEnty:
            self._currentManifestEnty = self._manifest.get(str(self)).addBuild(self.version, self.subinfo.options.dynamic, revision=self.sourceRevision())
        self._currentManifestEnty.addFile(
            fileType,
            name,
            CraftHash.digestFile(archiveFile, CraftHash.HashAlgorithm.SHA256),
        )

        self._manifest.dump(manifestLocation)

    @property
    def archiveExtension(self):
        extension = "." + CraftCore.settings.get("Packager", "7ZipArchiveType", "7z")
        if extension == ".7z" and not CraftCore.compiler.platform.isWindows:
            extension = ".tar.7z"
        return extension

    def _createArchive(
        self,
        archiveName,
        sourceDir,
        destDir,
        createDigests=True,
        fileType: FileType = FileType.Binary,
    ) -> bool:
        archiveName = Path(destDir) / archiveName

        if not utils.compress(archiveName, sourceDir):
            return False

        if createDigests:
            self._generateManifest(destDir, archiveName, fileType=fileType)
            CraftHash.createDigestFiles(archiveName)
        return True

    def addExecutableFilter(self, pattern: str):
        pass
