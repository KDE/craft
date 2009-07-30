import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/coreutils-5.3.0-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/coreutils-5.3.0-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.3.0'] = SRC_URI
        self.defaultTarget = '5.3.0'
        self.targetMergePath['5.3.0'] = "dev-utils";

from Source.ArchiveSource import *
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *

class Package(PackageBase, ArchiveSource, BinaryBuildSystem):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        self.forceCreateManifestFiles = True
        # no packager required 

if __name__ == '__main__':
    Package().execute()
