from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.BuildSystemBase import *
from Packager.PackagerBase import *


class SourceOnlyPackageBase( PackageBase, MultiSource, BuildSystemBase, PackagerBase ):
    """provides a base class for source dependency packages"""
    def __init__( self ):
        craftDebug.log.debug("SourceOnlyPackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        BuildSystemBase.__init__(self, "")
        PackagerBase.__init__(self)

# from BuildSystemBase:
    def configure( self ):
        return True

    def install( self ):
        if installdb.isInstalled(self.category, self.package):
            for p in installdb.getInstalledPackages(self.category, self.package):
                p.uninstall()
        installdb.addInstalled(self.category, self.package, self.version, revision=self.sourceRevision())
        return True

    def uninstall( self ):
        return True

    def runTests( self ):
        return True

    def make( self ):
        return True

# from PackagerBase:
    def createPackage( self ):
        return True