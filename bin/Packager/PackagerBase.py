# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

from EmergeBase import *

class PackagerBase(EmergeBase):
    """ provides a generic interface for packagers and implements basic package creating stuff """
    def __init__(self):
        EmergeBase.__init__(self)
    
    def getPackageVersion(self):
        """ return version information for the currently used package"""
        if self.subinfo.options.package.version <> None:
            pkgVersion = self.subinfo.options.package.version
            pkgNotesVersion = pkgVersion
        elif self.subinfo.buildTarget == "gitHEAD" or self.subinfo.buildTarget == "svnHEAD":
            pkgVersion = str( datetime.date.today() ).replace('-', '')
            pkgNotesVersion = pkgVersion
        else:
            pkgVersion = self.subinfo.buildTarget
            pkgNotesVersion = pkgVersion

        if "EMERGE_PKGPATCHLVL" in os.environ:
            pkgVersion += "-" + os.environ["EMERGE_PKGPATCHLVL"]
        return [pkgVersion, pkgNotesVersion]
    
    #""" create a package """
    def createPackage(self): abstract()

    # for compatibility 
    def make_package(self):
        return self.createPackage()



