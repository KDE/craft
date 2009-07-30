import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/sed-4.1.5-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/sed-4.1.5-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.1.5'] = SRC_URI
        self.defaultTarget = '4.1.5'
        self.targetMergePath['4.1.5'] = "dev-utils";
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

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
