#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

from CraftBase import *


class PackagerBase(CraftBase):
    """ provides a generic interface for packagers and implements basic package creating stuff """

    @InitGuard.init_once
    def __init__(self):
        CraftBase.__init__(self)
        self.whitelist_file = None
        self.blacklist_file = None
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

        if ("General", "EMERGE_PKGPATCHLVL") in craftSettings and craftSettings.get("General",
                                                                                    "EMERGE_PKGPATCHLVL") != "":
            pkgVersion += "-" + craftSettings.get("General", "EMERGE_PKGPATCHLVL")

        return [pkgVersion, pkgNotesVersion]

    # """ create a package """
    def createPackage(self):
        utils.abstract()
