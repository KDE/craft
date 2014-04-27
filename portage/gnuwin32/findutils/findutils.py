import info


SRC_URI = """
http://downloads.sourceforge.net/project/gnuwin32/findutils/4.2.20-2/findutils-4.2.20-2-bin.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.2.20-2'] = SRC_URI
        self.targetDigests['4.2.20-2'] = '69ea9bdff90bbe3ee7e30d23058b12ece8f403a2'
        self.defaultTarget = '4.2.20-2'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"


if __name__ == '__main__':
    Package().execute()
