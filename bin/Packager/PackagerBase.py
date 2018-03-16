#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

import datetime
import json

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

    def preArchive(self):
        utils.abstract()

    def archiveDir(self):
        return os.path.join(self.buildRoot(), "archive")

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
        entry.addFile(name, CraftHash.digestFile(archiveFile, CraftHash.HashAlgorithm.SHA256), version=self.version)

        manifest.dump(manifestLocation)

    @property
    def shortcuts(self) -> []:
        """ Return a list of shortcuts we want installe"""
        out = []
        if "shortcuts" in self.defines:
            out  += self.defines["shortcuts"]
        return out

