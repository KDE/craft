#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
from Package.PackageBase import *

class InternalPackageBase(PackageBase):
    """
     provides a generic interface for packages which are used internal by the emerge system
    """

    def __init__(self):
        PackageBase.__init__(self)
        return None

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
        print("%s %s " % (self.category, self.package))
        portage.addInstalled( self.category, self.package, self.version, self._installedDBPrefix("Release") )
        portage.addInstalled( self.category, self.package, self.version, self._installedDBPrefix("RelWithDebInfo") )
        portage.addInstalled( self.category, self.package, self.version, self._installedDBPrefix("Debug") )
        portage.addInstalled( self.category, self.package, self.version, self._installedDBPrefix() )
        return True

    def unmerge(self):
        portage.remInstalled( self.category, self.package, self.version, self._installedDBPrefix("Release") )
        portage.remInstalled( self.category, self.package, self.version, self._installedDBPrefix("RelWithDebInfo") )
        portage.remInstalled( self.category, self.package, self.version, self._installedDBPrefix("Debug") )
        portage.remInstalled( self.category, self.package, self.version, self._installedDBPrefix() )
        return True
