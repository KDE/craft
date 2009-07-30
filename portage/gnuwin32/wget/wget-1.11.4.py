import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/wget-%s-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/wget-%s-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        for t in ( '1.10.1', '1.11.4' ):
          self.targets[ t ] = SRC_URI % ( t, t )
        self.defaultTarget = '1.11.4'
        self.targetMergePath['1.11.4'] = "dev-utils";

from Source.ArchiveSource import *
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *

class Package(PackageBase, ArchiveSource, BinaryBuildSystem):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        # no packager required 

if __name__ == '__main__':
    Package().execute()
