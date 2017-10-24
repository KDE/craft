#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

import datetime
import json

from CraftBase import *

from Utils import CraftHash


class PackagerBase(CraftBase):
    """ provides a generic interface for packagers and implements basic package creating stuff """

    @InitGuard.init_once
    def __init__(self):
        CraftBase.__init__(self)
        self.whitelist_file = []
        self.blacklist_file = []
        self.defines = {}
        self.ignoredPackages = []

    def preArchive(self):
        utils.abstract()

    def archiveDir(self):
        return os.path.join(self.buildRoot(), "archive")

    def getPackageVersion(self):
        """ return version information for the currently used package"""
        if self.subinfo.options.package.version != None:
            pkgVersion = self.subinfo.options.package.version
        elif self.subinfo.hasSvnTarget():
            pkgVersion = self.sourceVersion()
        else:
            pkgVersion = self.subinfo.buildTarget

        pkgNotesVersion = pkgVersion
        return [pkgVersion, pkgNotesVersion]

    # """ create a package """
    def createPackage(self):
        utils.abstract()


    def _generateManifest(self, destDir, archiveName, manifestLocation=None):
        if not manifestLocation:
            manifestLocation = destDir
        cacheFilePath = os.path.join(manifestLocation, "manifest.json")
        cache = {}

        if ("ContinuousIntegration", "RepositoryUrl") in CraftCore.settings and not os.path.isfile(cacheFilePath):
            url = CraftCore.settings.get("ContinuousIntegration", "RepositoryUrl")
            if not url.endswith("/"):
                url += "/"
            utils.getFile(f"{url}manifest.json", manifestLocation)

        if os.path.isfile(cacheFilePath):
            with open(cacheFilePath, "rt+") as cacheFile:
                cache = json.load(cacheFile)

        cache["Date"] = str(datetime.date.today())
        if "APPVEYOR_BUILD_VERSION" in os.environ:
            cache["APPVEYOR_BUILD_VERSION"] = os.environ["APPVEYOR_BUILD_VERSION"]

        archiveFile = os.path.join(destDir, archiveName)
        if not str(self) in cache:
            cache[str(self)] = {}
        cache[str(self)][archiveName] = {"checksum": CraftHash.digestFile(archiveFile, CraftHash.HashAlgorithm.SHA256)}

        with open(cacheFilePath, "wt+") as cacheFile:
            json.dump(cache, cacheFile, sort_keys=True, indent=2)
