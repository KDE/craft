import base
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/diffutils-2.8.7-1-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/diffutils-2.8.7-1-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.8.7-1'] = SRC_URI
        self.defaultTarget = '2.8.7-1'
        self.targetMergePath['2.8.7-1'] = "dev-utils";
    
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
