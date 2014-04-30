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
        installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix("Release") )
        installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix("RelWithDebInfo") )
        installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix("Debug") )
        installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix() )
        return True

    def unmerge(self):
        installdb.remInstalled( self.category, self.package, self._installedDBPrefix( "Release" ) )
        installdb.remInstalled( self.category, self.package, self._installedDBPrefix( "RelWithDebInfo" ) )
        installdb.remInstalled( self.category, self.package, self._installedDBPrefix( "Debug" ) )
        installdb.remInstalled( self.category, self.package, self._installedDBPrefix( ) )
        return True
