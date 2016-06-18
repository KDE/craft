#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

from EmergeBase import *

class PackagerBase(EmergeBase):
    """ provides a generic interface for packagers and implements basic package creating stuff """
    def __init__(self):
        EmergeBase.__init__(self)
        self.whitelist_file = None
        self.blacklist_file = None
        self.defines = {}
        self.ignoredPackages = []

    def preArchive(self):
        utils.abstract()

    def archiveDir(self):
        return os.path.join( self.buildRoot(), "archive" )

    def getPackageVersion(self):
        """ return version information for the currently used package"""
        if self.subinfo.options.package.version != None:
            pkgVersion = self.subinfo.options.package.version
        elif self.subinfo.hasSvnTarget():
            pkgVersion = self.source.sourceVersion()
        else:
            pkgVersion = self.subinfo.buildTarget

        pkgNotesVersion = pkgVersion

        if ("General","EMERGE_PKGPATCHLVL") in emergeSettings and emergeSettings.get("General","EMERGE_PKGPATCHLVL") != "":
            pkgVersion += "-" + emergeSettings.get("General","EMERGE_PKGPATCHLVL")

        return [pkgVersion, pkgNotesVersion]

    #""" create a package """
    def createPackage(self):
        utils.abstract()
