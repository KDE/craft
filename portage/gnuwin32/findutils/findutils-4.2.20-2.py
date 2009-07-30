import base
import info

## \todo  manifest file from package is empty -> add a switch to force manifest generating 

SRC_URI = """
http://www.winkde.org/pub/kde/ports/win32/repository/gnuwin32/findutils-4.2.20-2-bin.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.2.20-2'] = SRC_URI
        self.defaultTarget = '4.2.20-2'
        self.targetMergePath['4.2.20-2'] = "dev-utils";

from Source.ArchiveSource import *
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *

class Package(PackageBase, ArchiveSource, BinaryBuildSystem):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        # the binary package contains an empty manifest file for the bin package
        # let emerge create it unconditional
        self.forceCreateManifestFiles  = True
        # no packager required 

if __name__ == '__main__':
    Package().execute()
