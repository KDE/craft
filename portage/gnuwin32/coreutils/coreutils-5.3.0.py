import info

## \todo the dep files will let into have dll's installed multiple times 
SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/coreutils-5.3.0-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/coreutils-5.3.0-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.3.0'] = SRC_URI
        self.defaultTarget = '5.3.0'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
