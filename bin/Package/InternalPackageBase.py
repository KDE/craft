#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
from Package.PackageBase import *


class InternalPackageBase(PackageBase):
    """
     provides a generic interface for packages which are used internal by the craft system
    """

    def __init__(self):
        PackageBase.__init__(self)

    def fetch(self):
        return True

    def unpack(self):
        return True

    def compile(self):
        return True

    def cleanImage(self):
        return True

    def install(self):
        return True

    def manifest(self):
        return True

    def qmerge(self):
        installdb.addInstalled(self.category, self.package, self.version)
        installdb.addInstalled(self.category, self.package, self.version)
        installdb.addInstalled(self.category, self.package, self.version)
        installdb.addInstalled(self.category, self.package, self.version)
        return True

    def unmerge(self):
        installdb.getInstalledPackages(self.category, self.package)
        installdb.getInstalledPackages(self.category, self.package)
        installdb.getInstalledPackages(self.category, self.package)
        installdb.getInstalledPackages(self.category, self.package)
        return True
